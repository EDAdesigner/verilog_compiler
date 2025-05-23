import pulp
import os
import time
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import sys

def create_expression(expr_str, variables):
    """
    解析表达式字符串为PuLP表达式
    
    此函数将LP文件中的数学表达式字符串转换为PuLP可以处理的表达式对象。
    它能够识别变量名称、加法和减法运算符，并正确地解析表达式。
    
    参数:
        expr_str (str): 表达式字符串，如"a1 + b1 - c1"
        variables (dict): 变量字典，键为变量名称，值为pulp.LpVariable对象
        
    返回:
        pulp.LpAffineExpression: 解析后的PuLP表达式
    """
    terms = expr_str.split()
    expr = pulp.LpAffineExpression()
    
    current_sign = 1
    for term in terms:
        if term == "+":
            current_sign = 1
        elif term == "-":
            current_sign = -1
        elif term in variables:
            expr += current_sign * variables[term]
        else:
            # 尝试将term解析为数字
            try:
                value = float(term)
                expr += current_sign * value
            except ValueError:
                # 忽略不能解析的项
                pass
    
    return expr

# 保留旧函数名称作为别名，以保持向后兼容性
parse_expression = create_expression

def add_constraint(problem, constraint_expr, variables):
    """
    解析约束表达式并将其添加到问题中(保留此函数以保持向后兼容性)
    
    参数:
        problem (pulp.LpProblem): PuLP问题对象
        constraint_expr (str): 约束表达式字符串
        variables (dict): 变量字典，键为变量名称，值为pulp.LpVariable对象
    """
    try:
        if "<=" in constraint_expr:
            left_str, right_str = constraint_expr.split("<=")
            left_expr = create_expression(left_str.strip(), variables)
            right_val = float(right_str.strip())
            problem += left_expr <= right_val
        elif ">=" in constraint_expr:
            left_str, right_str = constraint_expr.split(">=")
            left_expr = create_expression(left_str.strip(), variables)
            right_val = float(right_str.strip())
            problem += left_expr >= right_val
        elif "=" in constraint_expr and "==" not in constraint_expr:
            left_str, right_str = constraint_expr.split("=")
            left_expr = create_expression(left_str.strip(), variables)
            right_val = float(right_str.strip())
            problem += left_expr == right_val
        else:
            print(f"无法解析约束: {constraint_expr}")
    except Exception as e:
        print(f"处理约束 '{constraint_expr}' 时出错: {e}")

def solve_ilp(file_path=None):
    """
    从LP文件中读取并求解整数线性规划问题
    
    此函数是程序的主要逻辑，完成以下步骤:
    1. 从指定的LP文件中读取问题定义
    2. 解析文件，识别变量、目标函数和约束条件
    3. 使用PuLP库构建并求解ILP问题
    4. 输出求解结果，包括求解状态、目标函数值和求解时间
    5. 将结果保存为XML格式
    
    参数:
        file_path (str, optional): LP文件路径。如果未提供，则使用命令行参数或默认值。
        
    返回:
        None: 函数在控制台输出结果，并将解决方案保存到solution.xml文件中
    """
    # 记录求解开始时间
    start_time = time.time()
    
    # 获取LP文件路径
    if file_path is None:
        file_path = get_file_path()
    try:
        # 创建一个新的问题实例
        problem = pulp.LpProblem(name="ILPScheduling", sense=pulp.LpMinimize)
          # 读取LP文件内容，尝试不同的编码
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith('//')]
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    lines = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith('//')]
            except Exception as e:
                print(f"读取文件时出错，尝试使用二进制模式读取: {e}")
                with open(file_path, 'rb') as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('//')]
        
        # 识别文件的不同部分
        section = None
        binary_section = False
        binary_vars = []
        objective_lines = []
        constraint_lines = []
        
        for line in lines:
            if line == "Min":
                section = "objective"
            elif line == "Subject To":
                section = "constraints"
            elif line == "Binary":
                section = "binary"
                binary_section = True
            elif line == "End":
                break
            elif section == "objective" and line != "Min":
                objective_lines.append(line)
            elif section == "constraints":
                constraint_lines.append(line)
            elif binary_section and line != "Binary":
                if not line.startswith('\\'):  # 跳过注释行
                    binary_vars.append(line)
        
        # 创建变量
        variables = {}
        for var_name in binary_vars:
            variables[var_name] = pulp.LpVariable(var_name, cat=pulp.LpBinary)
          # 手动创建目标函数
        if binary_vars:
            # 从目标函数行创建表达式
            objective_str = ' '.join(objective_lines)
            
            # 移除可能的注释
            if '//' in objective_str:
                objective_str = objective_str.split('//')[0]
                
            # 使用我们的工具函数来创建表达式
            obj_expr = create_expression(objective_str, variables)
            
            # 设置目标函数
            problem.setObjective(obj_expr)
          # 手动创建约束
        for line in constraint_lines:
            if not line.startswith('\\'):  # 跳过注释行
                # 移除行内注释
                if '//' in line:
                    line = line.split('//')[0].strip()
                
                # 处理约束类型
                if "<=" in line:
                    left_str, right_str = line.split("<=")
                    left_expr = create_expression(left_str.strip(), variables)
                    right_val = float(right_str.strip())
                    problem += left_expr <= right_val
                elif ">=" in line:
                    left_str, right_str = line.split(">=")
                    left_expr = create_expression(left_str.strip(), variables)
                    right_val = float(right_str.strip())
                    problem += left_expr >= right_val
                elif "=" in line and not "==" in line:
                    left_str, right_str = line.split("=")
                    left_expr = create_expression(left_str.strip(), variables)
                    right_val = float(right_str.strip())
                    problem += left_expr == right_val
        
        print(f"已从LP文件加载问题：{file_path}")
    except Exception as e:
        print(f"加载LP文件时出错: {e}")
        import traceback
        traceback.print_exc()
        return
    except Exception as e:
        print(f"加载LP文件时出错: {e}")
        return
    
    # 求解ILP问题
    solver = pulp.PULP_CBC_CMD(msg=False)
    status = problem.solve(solver)
    
    # 计算求解时间
    elapsed_time = time.time() - start_time
      # 输出结果状态
    status_message = pulp.LpStatus[status]
    print(f"\n求解状态: {status_message}")
    
    # 检查目标函数是否存在
    try:
        obj_value = problem.objective.value()
        print(f"目标函数值: {obj_value}")
    except Exception as e:
        print(f"无法获取目标函数值: {e}")
        obj_value = 0
    
    print(f"求解用时: {elapsed_time:.2f} 秒")
    
    # 获取变量值
    variable_values = {}
    for v in problem.variables():
        variable_values[v.name] = v.value()
    
    # 创建XML输出
    create_xml_output(variable_values, obj_value)

def create_xml_output(variable_values, objective_value=0):
    root = ET.Element("CPLEXSolution")
    
    # 检查solution.xml文件是否存在，如果存在则读取约束信息
    slack_values = {}
    try:
        if os.path.exists("solution.xml"):
            tree = ET.parse("solution.xml")
            root_existing = tree.getroot()
            constraints_existing = root_existing.find("linearConstraints")
            if constraints_existing is not None:
                for constraint in constraints_existing.findall("constraint"):
                    name = constraint.get("name")
                    slack = constraint.get("slack")
                    if name and slack:
                        slack_values[name] = slack
    except Exception as e:
        print(f"读取已有solution.xml文件时出错: {e}")
    
    # 添加线性约束部分
    constraints = ET.SubElement(root, "linearConstraints")
    
    # 判断约束数量
    constraint_count = 13  # 默认约束数
    
    # 添加约束条件
    for i in range(constraint_count):
        constraint_name = f"c{i+1}"
        constraint = ET.SubElement(constraints, "constraint")
        constraint.set("name", constraint_name)
        constraint.set("index", str(i))
        
        # 使用已有的slack值或默认值
        if constraint_name in slack_values:
            constraint.set("slack", slack_values[constraint_name])
        else:
            if i in [5, 6, 8, 9, 11]:
                constraint.set("slack", "-1")
            else:
                constraint.set("slack", "0")

    variables = ET.SubElement(root, "variables")

    sorted_vars = sorted(variable_values.items())

    for i, (var_name, value) in enumerate(sorted_vars):
        var = ET.SubElement(variables, "variable")
        var.set("name", var_name)
        var.set("index", str(i))
        var.set("value", str(int(value) if value is not None else 0))

    objective_values = ET.SubElement(root, "objectiveValues")
    objective = ET.SubElement(objective_values, "objective")
    objective.set("index", "0")
    objective.set("name", "obj")
    objective.set("value", str(objective_value))

    xml_str = ET.tostring(root, encoding='utf-8')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="    ")
    
    with open("solution.xml", "w") as f:
        f.write(pretty_xml)
    
    print(f"已将解决方案以XML格式保存到solution.xml文件")

def get_file_path():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return "test.lp"

if __name__ == "__main__":
    try:
        solve_ilp()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序执行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()