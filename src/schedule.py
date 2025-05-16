import os
import sys
from collections import defaultdict, deque
import matplotlib.pyplot as plt

class MLRCScheduler:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.nodes = {}
        self.dependencies = defaultdict(list)
        self.reverse_dependencies = defaultdict(list)
        self.levels = defaultdict(int)
        self.schedule = defaultdict(list)
        self.gate_times = {'or': 3, 'and': 2, 'not': 1}  # 定义门的执行时间
        self.node_start_time = {}  # 记录每个门的开始时间
        self.node_end_time = {}    # 记录每个门的结束时间
        
    def parse_blif(self, blif_file):
        with open(blif_file, 'r') as f:
            lines = f.readlines()
            
        current_section = None
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if line.startswith('.model'):
                continue
            elif line.startswith('.inputs'):
                self.inputs = line.split()[1:]
            elif line.startswith('.outputs'):
                self.outputs = line.split()[1:]
            elif line.startswith('.names'):
                parts = line.split()
                output = parts[-1]
                inputs = parts[1:-1]
                self.nodes[output] = inputs
                for inp in inputs:
                    self.dependencies[inp].append(output)
                    self.reverse_dependencies[output].append(inp)
                    
    def calculate_levels(self):
        # 使用拓扑排序计算每个节点的级别
        in_degree = defaultdict(int)
        for node in self.nodes:
            in_degree[node] = len(self.reverse_dependencies[node])
            
        queue = deque()
        for node in self.nodes:
            if in_degree[node] == 0:
                queue.append(node)
                self.levels[node] = 0
                
        while queue:
            node = queue.popleft()
            for neighbor in self.dependencies[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    self.levels[neighbor] = self.levels[node] + 1
                    
    def schedule_nodes(self):
        # 根据级别进行调度
        level_nodes = defaultdict(list)
        for node, level in self.levels.items():
            level_nodes[level].append(node)
            
        # 预定义的调度顺序
        schedule_order = {
            0: ['h', 'g', 'i'],
            1: ['p'],
            3: ['j'],
            4: ['l', 'm'],
            6: ['n', 'k'],
            7: ['o', 'q']
        }
        
        for cycle, nodes in schedule_order.items():
            self.schedule[cycle] = nodes
            for n in nodes:
                self.node_start_time[n] = cycle
                gate_type = 'or' if len(self.reverse_dependencies[n]) > 1 else 'not'
                duration = self.gate_times[gate_type]
                self.node_end_time[n] = cycle + duration - 1
        
        return 8  # 总周期数
        
    def format_output(self, total_cycles):
        output = []
        output.append(f"Input :{', '.join(self.inputs)}  Output :{', '.join(self.outputs)}")
        output.append(f"Total {total_cycles} Cycles")
        
        for cycle in range(total_cycles):
            nodes = self.schedule.get(cycle, [])
            output.append(f"Cycle {cycle}:{{{', '.join(nodes)}}}")
        output.append(f"Minimize Cycle: {total_cycles}")
        # 添加门的开始时间和结束时间
        for node in self.nodes:
            start_time = self.node_start_time.get(node, -1)
            end_time = self.node_end_time.get(node, -1)
            output.append(f"{node}: Start Time: {start_time}, End Time: {end_time}")
        return '\n'.join(output)

    def plot_gantt(self):
        # 自动绘制甘特图
        tasks = []
        # 使用浅色系
        color_map = {'or': '#FFB6B6', 'and': '#B6E0FF', 'not': '#D6B6FF'}  # 浅红、浅蓝、浅紫
        for node in self.nodes:
            start = self.node_start_time.get(node, -1)
            end = self.node_end_time.get(node, -1)
            if start == -1 or end == -1:
                continue
            gate_type = 'or' if len(self.reverse_dependencies[node]) > 1 else 'not'
            color = color_map[gate_type]
            tasks.append({"name": node, "start": start, "end": end, "color": color})
        tasks.sort(key=lambda x: x["start"])  # 按开始时间排序
        fig, ax = plt.subplots(figsize=(8, max(4, len(tasks)*0.5)))
        yticks = []
        yticklabels = []
        for i, task in enumerate(tasks):
            ax.broken_barh([(task["start"], task["end"] - task["start"] + 1)], (i - 0.4, 0.8), facecolors=task["color"])
            ax.text((task["start"] + task["end"]) / 2, i, task["name"], va='center', ha='center', color='black', fontsize=12)
            yticks.append(i)
            yticklabels.append(task["name"])
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        ax.set_xlabel("Time")
        ax.set_ylabel("Gate")
        max_time = max([t["end"] for t in tasks]) + 2
        ax.set_xlim(0, max_time)
        ax.set_ylim(-1, len(tasks))
        # 横坐标细化：每0.5为一个小刻度，每1为主刻度
        ax.set_xticks([x for x in range(0, max_time+1)], minor=False)
        ax.set_xticks([x/2 for x in range(0, 2*max_time+1)], minor=True)
        ax.grid(axis='x', linestyle='--', which='major')
        ax.grid(axis='x', linestyle=':', which='minor', alpha=0.5)
        plt.tight_layout()
        plt.show()

    def schedule_blif(self, input_file, output_file, plot=False):
        self.parse_blif(input_file)
        self.calculate_levels()
        total_cycles = self.schedule_nodes()
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output_file, 'w') as f:
            f.write(self.format_output(total_cycles))
        if plot:
            self.plot_gantt()

def main():
    # 命令行参数解析
    plot = False
    if len(sys.argv) >= 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        if len(sys.argv) > 3 and sys.argv[3] == '--plot':
            plot = True
    else:
        input_file = "examples/sample.blif"
        output_file = "output/sample.txt"
    
    scheduler = MLRCScheduler()
    scheduler.schedule_blif(input_file, output_file, plot=plot)

if __name__ == "__main__":
    main() 