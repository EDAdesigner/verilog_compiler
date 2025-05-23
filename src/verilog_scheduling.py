#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from verilog_parser import VerilogParser

def verilog_to_blif(input_file, output_file=None):
    """
    将Verilog文件转换为BLIF格式
    
    参数:
        input_file: 输入的Verilog文件路径
        output_file: 输出的BLIF文件路径，默认为与输入文件同名但扩展名为.blif
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            verilog_code = f.read()
    except Exception as e:
        print(f"错误: 无法读取文件 '{input_file}': {e}")
        return False

    # 解析Verilog代码
    parser = VerilogParser()
    module = parser.parse(verilog_code)

    if module is None:
        print("解析失败，请检查Verilog代码语法")
        return False

    # 生成BLIF内容
    blif_content = generate_blif(module)

    # 确定输出文件路径
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.blif'

    # 写入BLIF文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(blif_content)
        print(f"成功生成BLIF文件: {output_file}")
    except Exception as e:
        print(f"错误: 无法写入BLIF文件 '{output_file}': {e}")
        return False

    return True

def generate_blif(module):
    """
    根据解析后的模块对象生成BLIF格式内容
    """
    blif_lines = []
    blif_lines.append(f".model {module.name}")
    blif_lines.append(".inputs " + " ".join(module.inputs))
    blif_lines.append(".outputs " + " ".join(module.outputs))
    blif_lines.append(".names " + " ".join(module.wires))

    # 处理门级实例化
    for gate in module.gates:
        blif_lines.append(f".gate {gate.gate_type} " + " ".join(gate.inputs) + " " + gate.output)

    # 处理赋值语句
    for assign in module.assigns:
        blif_lines.append(f".names {assign.left} {assign.right}")

    blif_lines.append(".end")
    return "\n".join(blif_lines)

def list_schedule(module, resource_num=2):
    """
    ML-RCS列表调度算法实现，resource_num为每种资源的数量
    输出格式：IInput:[inputs],Output:[outputs]\nCycle 1: ...\nCycle 2: ...
    """
    # 1. 收集所有操作（assign和门）及其依赖
    # 操作节点格式：{'name':..., 'type':..., 'inputs':[], 'output':..., 'deps':set(), 'scheduled':False, 'cycle':None}
    nodes = []
    name2node = {}
    # 先处理assign
    for assign in module.assigns:
        # 递归解析表达式树，拆分为基本操作
        def parse_expr(expr, out_name):
            if isinstance(expr, str):
                return []
            if isinstance(expr, dict):
                op_type = expr['op']
                if op_type in ['+', '-', '&', '|', '^']:
                    left = expr['left']
                    right = expr['right']
                    left_name = left if isinstance(left, str) else f"tmp_{len(nodes)}_l"
                    right_name = right if isinstance(right, str) else f"tmp_{len(nodes)}_r"
                    # 递归处理左右
                    nodes_l = parse_expr(left, left_name)
                    nodes_r = parse_expr(right, right_name)
                    node = {'name': out_name, 'type': op_type, 'inputs':[left_name, right_name], 'output':out_name, 'deps':set([left_name, right_name]), 'scheduled':False, 'cycle':None}
                    nodes_l.extend(nodes_r)
                    nodes_l.append(node)
                    name2node[out_name] = node
                    return nodes_l
                elif op_type == '~':
                    right = expr['right']
                    right_name = right if isinstance(right, str) else f"tmp_{len(nodes)}_r"
                    nodes_r = parse_expr(right, right_name)
                    node = {'name': out_name, 'type': 'NOT', 'inputs':[right_name], 'output':out_name, 'deps':set([right_name]), 'scheduled':False, 'cycle':None}
                    nodes_r.append(node)
                    name2node[out_name] = node
                    return nodes_r
                elif op_type == '?:':
                    # 三元暂不支持
                    return []
            return []
        nodes.extend(parse_expr(assign.right, assign.left))
    # 处理门级实例化
    for gate in module.gates:
        node = {'name': gate.name, 'type': gate.gate_type, 'inputs':gate.inputs, 'output':gate.output, 'deps':set(gate.inputs), 'scheduled':False, 'cycle':None}
        nodes.append(node)
        name2node[gate.output] = node
    # 2. 建立依赖关系
    # 只保留依赖于其他操作输出的依赖
    outputs = set([n['output'] for n in nodes])
    for n in nodes:
        n['deps'] = set([d for d in n['deps'] if d in outputs])
    # 3. 列表调度
    schedule = []
    cycle = 1
    unscheduled = set(range(len(nodes)))
    while unscheduled:
        ready = [i for i in unscheduled if all(name2node.get(d, {'scheduled':True})['scheduled'] for d in nodes[i]['deps'])]
        # 按资源数分组
        this_cycle = []
        used = 0
        for idx in ready:
            if used >= resource_num:
                break
            this_cycle.append(idx)
            used += 1
        # 标记调度
        for idx in this_cycle:
            nodes[idx]['scheduled'] = True
            nodes[idx]['cycle'] = cycle
            unscheduled.remove(idx)
        schedule.append(this_cycle)
        cycle += 1
    # 4. 输出
    print(f"IInput:{module.inputs},Output:{module.outputs}")
    for i, cyc in enumerate(schedule):
        if not cyc:
            print(f"Cycle {i+1}:")
            continue
        ops = []
        for idx in cyc:
            n = nodes[idx]
            op_type = n['type']
            if op_type == '+': op_type = 'ADD'
            elif op_type == '-': op_type = 'SUB'
            elif op_type == '&': op_type = 'AND'
            elif op_type == '|': op_type = 'OR'
            elif op_type == '^': op_type = 'XOR'
            ops.append(f"{n['name']}({op_type})")
        print(f"Cycle {i+1}: {', '.join(ops)}")

def asap_schedule(nodes):
    """ASAP调度，返回每个操作的最早调度周期asap_time"""
    name2node = {n['name']: n for n in nodes}
    for n in nodes:
        n['asap'] = None
    # 入度为0的节点（无依赖）
    ready = [n for n in nodes if not n['deps']]
    for n in ready:
        n['asap'] = 0
    scheduled = set(n['name'] for n in ready)
    while len(scheduled) < len(nodes):
        for n in nodes:
            if n['asap'] is not None:
                continue
            if all(name2node[d]['asap'] is not None for d in n['deps']):
                n['asap'] = max([name2node[d]['asap'] for d in n['deps']] or [0]) + 1
                scheduled.add(n['name'])
    return {n['name']: n['asap'] for n in nodes}

def alap_schedule(nodes, max_cycle):
    """ALAP调度，返回每个操作的最晚调度周期alap_time，max_cycle为ASAP最大周期"""
    name2node = {n['name']: n for n in nodes}
    for n in nodes:
        n['alap'] = None
    # 出度为0的节点（无被依赖）
    outputs = set(n['name'] for n in nodes)
    for n in nodes:
        for d in n['deps']:
            outputs.discard(d)
    ready = [name2node[name] for name in outputs]
    for n in ready:
        n['alap'] = max_cycle
    scheduled = set(n['name'] for n in ready)
    while len(scheduled) < len(nodes):
        for n in nodes:
            if n['alap'] is not None:
                continue
            # 所有后继都已调度
            succs = [m for m in nodes if n['name'] in m['deps']]
            if all(s['alap'] is not None for s in succs):
                n['alap'] = min([s['alap'] for s in succs] or [max_cycle]) - 1
                scheduled.add(n['name'])
    return {n['name']: n['alap'] for n in nodes}

def list_schedule_mr_lcs(module):
    """
    MR-LCS最小资源列表调度，输出格式如用户要求
    """
    # 1. 构建操作节点
    nodes = []
    name2node = {}
    for assign in module.assigns:
        def parse_expr(expr, out_name):
            if isinstance(expr, str):
                return []
            if isinstance(expr, dict):
                op_type = expr['op']
                if op_type in ['+', '-', '&', '|', '^']:
                    left = expr['left']
                    right = expr['right']
                    left_name = left if isinstance(left, str) else f"tmp_{len(nodes)}_l"
                    right_name = right if isinstance(right, str) else f"tmp_{len(nodes)}_r"
                    nodes_l = parse_expr(left, left_name)
                    nodes_r = parse_expr(right, right_name)
                    node = {'name': out_name, 'type': op_type, 'inputs':[left_name, right_name], 'output':out_name, 'deps':set([left_name, right_name]), 'scheduled':False, 'cycle':None}
                    nodes_l.extend(nodes_r)
                    nodes_l.append(node)
                    name2node[out_name] = node
                    return nodes_l
                elif op_type == '~':
                    right = expr['right']
                    right_name = right if isinstance(right, str) else f"tmp_{len(nodes)}_r"
                    nodes_r = parse_expr(right, right_name)
                    node = {'name': out_name, 'type': 'NOT', 'inputs':[right_name], 'output':out_name, 'deps':set([right_name]), 'scheduled':False, 'cycle':None}
                    nodes_r.append(node)
                    name2node[out_name] = node
                    return nodes_r
                elif op_type == '?:':
                    return []
            return []
        nodes.extend(parse_expr(assign.right, assign.left))
    for gate in module.gates:
        node = {'name': gate.name, 'type': gate.gate_type, 'inputs':gate.inputs, 'output':gate.output, 'deps':set(gate.inputs), 'scheduled':False, 'cycle':None}
        nodes.append(node)
        name2node[gate.output] = node
    outputs = set([n['output'] for n in nodes])
    for n in nodes:
        n['deps'] = set([d for d in n['deps'] if d in outputs])
    # 2. ASAP/ALAP
    asap = asap_schedule(nodes)
    max_cycle = max(asap.values())
    alap = alap_schedule(nodes, max_cycle)
    for n in nodes:
        n['asap'] = asap[n['name']]
        n['alap'] = alap[n['name']]
        n['slack'] = n['alap'] - n['asap']
    # 3. MR-LCS调度
    schedule = [[] for _ in range(max_cycle+1)]
    unscheduled = set(n['name'] for n in nodes)
    while unscheduled:
        # 计算slack=0的可调度操作
        ready = [n for n in nodes if n['name'] in unscheduled and n['asap'] <= n['alap'] and all(name2node.get(d, {'scheduled':True})['scheduled'] for d in n['deps'])]
        # slack=0优先
        zero_slack = [n for n in ready if n['slack']==0]
        for n in zero_slack:
            n['scheduled'] = True
            n['cycle'] = n['asap']
            schedule[n['asap']].append(n)
            unscheduled.remove(n['name'])
        # 其它可调度操作
        for n in ready:
            if n['name'] in unscheduled:
                n['scheduled'] = True
                n['cycle'] = n['asap']
                schedule[n['asap']].append(n)
                unscheduled.remove(n['name'])
    # 4. 输出
    gate_type_map = {'+':'ADD', '-':'SUB', '&':'AND', '|':'OR', '^':'XOR', 'NOT':'NOT', 'AND':'AND', 'OR':'OR', 'XOR':'XOR', 'NAND':'NAND', 'NOR':'NOR', 'XNOR':'XNOR'}
    print(f"Input: {', '.join(module.inputs)}")
    print(f"Output: {', '.join(module.outputs)}")
    print(f"Total {max_cycle+1} Cycles, 与门{sum(1 for n in nodes if gate_type_map.get(n['type'])=='AND')}个，或门{sum(1 for n in nodes if gate_type_map.get(n['type'])=='OR')}个，非门{sum(1 for n in nodes if gate_type_map.get(n['type'])=='NOT')}个")
    for i, cyc in enumerate(schedule):
        ands = [n['name'] for n in cyc if gate_type_map.get(n['type'])=='AND']
        ors = [n['name'] for n in cyc if gate_type_map.get(n['type'])=='OR']
        nots = [n['name'] for n in cyc if gate_type_map.get(n['type'])=='NOT']
        others = [n['name'] for n in cyc if gate_type_map.get(n['type']) not in ['AND','OR','NOT']]
        print(f"Cycle {i}: {{{'  '.join(ands)}}}, {{{'  '.join(ors)}}}, {{{'  '.join(nots)}}}, {{{'  '.join(others)}}}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python verilog_to_blif.py <verilog_file> [output_blif_file] [--schedule a] [--mr-lcs]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    schedule_mode = '--schedule' in sys.argv
    mr_lcs_mode = '--mr-lcs' in sys.argv
    resource_num = 2
    if schedule_mode:
        idx = sys.argv.index('--schedule')
        if len(sys.argv) > idx+1:
            resource_num = int(sys.argv[idx+1])
    parser = VerilogParser()
    with open(input_file, 'r', encoding='utf-8') as f:
        verilog_code = f.read()
    module = parser.parse(verilog_code)
    if mr_lcs_mode:
        list_schedule_mr_lcs(module)
    elif schedule_mode:
        list_schedule(module, resource_num)
    else:
        verilog_to_blif(input_file, output_file) 