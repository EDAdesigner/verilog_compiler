import pulp
import time
import sys

GATE_DELAYS = {
    "AND": 2,
    "OR": 3,
    "NOT": 1,
    "LOGIC": 1,
}

DEFAULT_RESOURCE_COSTS = {
    "AND": 1,
    "OR": 1,
    "NOT": 1,
    "LOGIC": 1,
}

def parse_blif(blif_file_path):
    """
    Parses a BLIF file to extract model name, inputs, outputs, operations, and dependencies.
    """
    model_name = "unknown_model"
    primary_inputs = []
    primary_outputs = []
    operations = []
    dependencies = []

    try:
        with open(blif_file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"错误: BLIF文件未找到: {blif_file_path}")
        return None, [], [], [], []
    except Exception as e:
        print(f"读取BLIF文件时出错: {e}")
        return None, [], [], [], []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        parts = line.split()
        if not parts:
            continue

        if parts[0] == ".model" and len(parts) > 1:
            model_name = parts[1]
        elif parts[0] == ".inputs":
            primary_inputs.extend(parts[1:])
        elif parts[0] == ".outputs":
            primary_outputs.extend(parts[1:])
        elif parts[0] == ".names":
            if len(parts) < 2:
                print(f"警告: 无效的 .names 行: {line}")
                continue
            
            gate_op_id = parts[-1]
            gate_inputs = parts[1:-1]

            operations.append((gate_op_id, "LOGIC"))

            for in_signal in gate_inputs:
                dependencies.append((in_signal, gate_op_id))
            
        elif parts[0] == ".end":
            break

    print(f"BLIF模型 '{model_name}' 解析完成:")
    print(f"  主输入: {primary_inputs}")
    print(f"  主输出: {primary_outputs}")
    print(f"  操作 (门): {len(operations)}")
    print(f"  依赖关系: {len(dependencies)}")
    
    return model_name, primary_inputs, primary_outputs, operations, dependencies

def solve_gate_scheduling_mrlcs(blif_file_path, latency_constraint, resource_costs_override=None, gate_delays_override=None):
    """
    Solves the Minimum Resource Latency Constrained Scheduling (MR-LCS) problem for a circuit from a BLIF file.
    """
    solve_start_time = time.time()

    model_name, primary_inputs, primary_outputs, operations, dependencies = parse_blif(blif_file_path)
    if model_name is None:
        return "Error: BLIF parsing failed", None, None, None

    current_gate_delays = GATE_DELAYS.copy()
    if gate_delays_override:
        current_gate_delays.update(gate_delays_override)

    current_resource_costs = DEFAULT_RESOURCE_COSTS.copy()
    if resource_costs_override:
        current_resource_costs.update(resource_costs_override)
    
    if "LOGIC" not in current_gate_delays:
        print("错误: GATE_DELAYS 中缺少 'LOGIC' 类型的延迟定义。")
        return "Error: Missing LOGIC delay", None, None, None
    if "LOGIC" not in current_resource_costs:
        print("错误: resource_costs 中缺少 'LOGIC' 类型的成本定义。")
        return "Error: Missing LOGIC cost", None, None, None

    op_details = {} 
    for op_id, op_type in operations: 
        if op_type not in current_gate_delays:
            print(f"错误: 操作 {op_id} 具有未知的操作类型 '{op_type}' (未在门延迟中定义)。")
            return f"Error: Unknown operation type '{op_type}'", None, None, None
        op_details[op_id] = {"type": op_type, "delay": current_gate_delays[op_type]}

    for pi_name in primary_inputs:
        if pi_name not in op_details: 
            op_details[pi_name] = {"type": "PRIMARY_INPUT", "delay": 0}

    problem = pulp.LpProblem(f"GateScheduling_MR_LCS_{model_name}", pulp.LpMinimize)

    op_start_vars = {}
    for op_id in op_details:
        if op_details[op_id]["type"] == "PRIMARY_INPUT":
            continue

        op_delay = op_details[op_id]['delay']
        max_start_time = latency_constraint - op_delay
        if max_start_time < 0:
             print(f"错误: 操作 {op_id} (类型 {op_details[op_id]['type']}, 延迟 {op_delay}) 无法在总延迟 {latency_constraint} 内完成。")
             return "Error: Operation cannot fit", None, None, None
        
        possible_start_times = range(max_start_time + 1)
        op_start_vars[op_id] = pulp.LpVariable.dicts(
            f"start_{op_id}_at_t", possible_start_times, cat=pulp.LpBinary
        )
    
    gate_types_in_model = set(details['type'] for op_id, details in op_details.items() if details['type'] != "PRIMARY_INPUT")
    if not gate_types_in_model and operations:
         gate_types_in_model.add("LOGIC")


    num_resource_vars = pulp.LpVariable.dicts(
        "num_resources_of_type", list(gate_types_in_model), lowBound=0, cat=pulp.LpInteger
    )
    
    objective_sum = pulp.LpAffineExpression()
    for gate_type in gate_types_in_model:
        if gate_type in current_resource_costs:
            objective_sum += current_resource_costs[gate_type] * num_resource_vars[gate_type]
        else:
            print(f"警告: 门类型 {gate_type} 没有定义资源成本，将假定成本为0。")
    
    if not operations:
        problem += 0, "Minimize_Total_Resource_Cost"
    else:
        problem += objective_sum, "Minimize_Total_Resource_Cost"

    for op_id in op_start_vars:
        problem += pulp.lpSum(op_start_vars[op_id][t] for t in op_start_vars[op_id]) == 1, f"UniqueStartTime_For_Op_{op_id}"

    for dep_from_signal, dep_to_op_id in dependencies:
        if dep_to_op_id not in op_details or op_details[dep_to_op_id]["type"] == "PRIMARY_INPUT":
            continue
        
        if dep_to_op_id not in op_start_vars:
            print(f"警告: 依赖目标 {dep_to_op_id} 不是可调度操作，跳过依赖 {dep_from_signal} -> {dep_to_op_id}")
            continue

        start_time_expr_to = pulp.lpSum(t * op_start_vars[dep_to_op_id][t] for t in op_start_vars[dep_to_op_id])

        if dep_from_signal in primary_inputs:
            pass 
        elif dep_from_signal in op_details and op_details[dep_from_signal]["type"] != "PRIMARY_INPUT":
            if dep_from_signal not in op_start_vars :
                print(f"错误: 依赖源操作 {dep_from_signal} 没有调度变量。可能无法调度或BLIF错误。")
                continue

            delay_from = op_details[dep_from_signal]['delay']
            start_time_expr_from = pulp.lpSum(t * op_start_vars[dep_from_signal][t] for t in op_start_vars[dep_from_signal])
            problem += start_time_expr_to >= start_time_expr_from + delay_from, f"Dependency_{dep_from_signal}_to_{dep_to_op_id}"
        else:
            print(f"警告: 依赖源 {dep_from_signal} 未在操作或主输入中找到。跳过依赖 {dep_from_signal} -> {dep_to_op_id}")

    for gate_type in gate_types_in_model:
        if not gate_type in num_resource_vars: continue 
        for t_step in range(latency_constraint):
            active_ops_of_type_at_t_step = pulp.LpAffineExpression()
            for op_id, details in op_details.items():
                if details['type'] == gate_type and op_id in op_start_vars:
                    op_delay = details['delay']
                    for s_time in op_start_vars[op_id]:
                        if s_time <= t_step < s_time + op_delay:
                            active_ops_of_type_at_t_step += op_start_vars[op_id][s_time]
            problem += active_ops_of_type_at_t_step <= num_resource_vars[gate_type], f"ResourceLimit_{gate_type}_Time_{t_step}"
    
    for po_name in primary_outputs:
        if po_name in op_start_vars:
            op_id_driving_po = po_name
            op_delay_driving_po = op_details[op_id_driving_po]['delay']
            max_start_time = latency_constraint - op_delay_driving_po
            if max_start_time < 0:
                print(f"错误: 主输出 {po_name} 的驱动门 {op_id_driving_po} 无法在延迟约束 {latency_constraint} 内完成。")
                return "Error: PI to PO cannot meet latency", None, None, None
            possible_start_times = range(max_start_time + 1)
            op_start_vars[op_id_driving_po] = pulp.LpVariable.dicts(
                f"start_{op_id_driving_po}_at_t", possible_start_times, cat=pulp.LpBinary
            )
            pass # Constraint is implicitly handled
        elif po_name in primary_inputs:
            if latency_constraint < 0:
                 print(f"错误: 主输出 {po_name} (也是主输入) 无法满足延迟约束 {latency_constraint}")
                 return "Error: PI to PO cannot meet latency", None, None, None
            pass

    print(f"\n开始求解门调度 MR-LCS 问题 (模型: {model_name}, 总延迟约束: {latency_constraint})...")
    solver = pulp.PULP_CBC_CMD(msg=False)
    problem.solve(solver)
    
    solve_elapsed_time = time.time() - solve_start_time
    status_text = pulp.LpStatus[problem.status]
    print(f"求解状态: {status_text}")
    print(f"求解用时: {solve_elapsed_time:.3f} 秒")

    if problem.status == pulp.LpStatusOptimal or problem.status == pulp.LpStatusFeasible:
        final_objective_value = pulp.value(problem.objective) if problem.objective else 0.0
        print(f"目标函数值 (最小化资源成本): {final_objective_value}")

        final_schedule = {}
        for op_id in op_start_vars:
            for t, var_x_it in op_start_vars[op_id].items():
                if pulp.value(var_x_it) == 1:
                    final_schedule[op_id] = t
                    break
        
        for pi_name in primary_inputs:
            if pi_name not in final_schedule:
                final_schedule[pi_name] = 0 

        print("\n调度方案 (操作ID/信号: 类型, 延迟 -> 开始时间, 结束时间):")

        scheduled_pis = {op_id: st for op_id, st in final_schedule.items() if op_details.get(op_id, {}).get("type") == "PRIMARY_INPUT"}
        scheduled_gates = {op_id: st for op_id, st in final_schedule.items() if op_details.get(op_id, {}).get("type") != "PRIMARY_INPUT"}

        for op_id, start_t in sorted(scheduled_pis.items()):
            details = op_details[op_id]
            print(f"  PI {op_id}: {details['type']} -> 信号在时间 {start_t + details['delay']} 可用")

        for op_id, start_t in sorted(scheduled_gates.items(), key=lambda item: item[1]):
            details = op_details[op_id]
            finish_t = start_t + details['delay'] - 1
            print(f"  Gate {op_id}: {details['type']}, d={details['delay']} -> 开始: {start_t}, 结束: {finish_t}")

        final_resource_allocation = {}
        if operations :
            for gate_type in gate_types_in_model:
                 if gate_type in num_resource_vars:
                    final_resource_allocation[gate_type] = int(pulp.value(num_resource_vars[gate_type])) if num_resource_vars[gate_type] is not None and pulp.value(num_resource_vars[gate_type]) is not None else 0
            print("\n所需资源数量:")
            for gate_type, count in final_resource_allocation.items():
                print(f"  {gate_type} 门: {count}")
        else:
            print("\n模型中没有需要分配资源的逻辑门。")
            
        return status_text, final_objective_value, final_schedule, final_resource_allocation
    else:
        print("未能找到最优或可行解。")
        return status_text, None, None, None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("错误: 请提供BLIF文件的路径作为命令行参数。")
        print("用法: python src/blif_scheduler.py <path_to_blif_file> [latency_constraint]")
        print("示例: python src/blif_scheduler.py ./examples/my_circuit.blif 10")
        sys.exit(1)

    blif_file = sys.argv[1]
    latency = 10 
    if len(sys.argv) > 2:
        try:
            latency = int(sys.argv[2])
        except ValueError:
            print(f"错误: 延迟约束 '{sys.argv[2]}' 不是一个有效的整数。使用默认值 {latency}。")
    
    print(f"使用BLIF文件: {blif_file}, 延迟约束: {latency}")
       
    status, obj, schedule, resources = solve_gate_scheduling_mrlcs(blif_file, latency)

    if schedule:
        print("\n--- 调度结果 ---")
        pass 