import subprocess, json
import matplotlib.pyplot as plt

fontsize = 16

def build():
    command = "make"
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

def run_pr(is_pull, is_async, graph_size, num_trial):
    if is_pull:
        pushpull = "pull"
    else:
        pushpull = "push"
    
    if is_async:
        syncasync = "async"
    else:
        syncasync = "sync"
    
    if not is_pull and is_async:
        return []
    
    commnad = f"./pr_{pushpull}_{syncasync} -g {graph_size} -n {num_trial}"
    
    print(f"Running command: {commnad}")
    result = subprocess.run(commnad, shell=True, capture_output=True, text=True)
    
    # Capture the "Average Time" line output
    for line in result.stdout.splitlines():
        if "Average Time:" in line:
            avg_time = float(line.split(":")[1].strip())
            return avg_time

def run_pr_logging(is_pull, is_async, graph_size):
    if is_pull:
        pushpull = "pull"
    else:
        pushpull = "push"
    
    if is_async:
        syncasync = "async"
    else:
        syncasync = "sync"
    
    if not is_pull and is_async:
        return []
    
    commnad = f"./pr_{pushpull}_{syncasync} -g {graph_size} -n 1 -l"
    
    print(f"Running command: {commnad}")
    result = subprocess.run(commnad, shell=True, capture_output=True, text=True)
    
    lines = []
    for line in result.stdout.splitlines():
        parts = line.strip().split()
        if len(parts) == 2 and parts[0].isdigit():
            try:
                lines.append(float(parts[1]))
            except ValueError:
                continue
    return lines

def run_pr_tests():
    graph_sizes = range(10, 25) # 2^10 to 2^24
    num_trials = 10
    results = {}
    
    for is_pull in [True, False]:
        for is_async in [True, False]:
            if not is_pull and is_async:
                continue
            key = f"{'Pull' if is_pull else 'Push'} {'Async' if is_async else 'Sync'}"
            results[key] = []
            for size in graph_sizes:
                avg_time = run_pr(is_pull, is_async, size, num_trials)
                results[key].append((avg_time))
    
    with open("pr_results.json", "w") as f:
        json.dump(results, f, indent=4)

def run_bfs(mode, graph_size, num_trial):
    if mode == "Top down":
        mode_str = "_td"
    elif mode == "Bottom up":
        mode_str = "_bu"
    elif mode == "Hybrid":
        mode_str = "_hybrid"
    
    command = f"./bfs{mode_str} -g {graph_size} -n {num_trial}"
    
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Capture the "Average Time" line output
    for line in result.stdout.splitlines():
        if "Average Time:" in line:
            avg_time = float(line.split(":")[1].strip())
            return avg_time

def run_bfs_logging(mode, graph_size):
    if mode == "Top down":
        mode_str = "_td"
    elif mode == "Bottom up":
        mode_str = "_bu"
    elif mode == "Hybrid":
        mode_str = "_hybrid"
    
    command = f"./bfs{mode_str} -g {graph_size} -n 1 -l"
    
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    lines = []
    for line in result.stdout.splitlines():
        parts = line.strip().split()
        if parts[0] == 'td' or parts[0] == 'bu':
            try:
                lines.append({'step': parts[0], 'time': float(parts[2])})
            except ValueError:
                continue
        # elif parts[0] == 'e' or parts[0] == 'c':
        #     try:
        #         lines.append({'step': parts[0], 'time': float(parts[1])})
        #     except ValueError:
        #         continue
    return lines
        
def run_bfs_tests():
    graph_sizes = range(10, 25) # 2^10 to 2^24
    num_trials = 10
    results = {}
    
    for mode in ["Top down", "Bottom up", "Hybrid"]:
        key = f"{mode}"
        results[key] = []
        for size in graph_sizes:
            avg_time = run_bfs(mode, size, num_trials)
            results[key].append((avg_time))
    
    with open("bfs_results.json", "w") as f:
        json.dump(results, f, indent=4)

def run_logging():
    pr_results = {}
    for is_async in [True, False]:
        key = f"{'Async' if is_async else 'Sync'}"
        pr_results[key] = run_pr_logging(True, is_async, 22)
    with open("pr_logging.json", "w") as f:
        json.dump(pr_results, f, indent=4)
    
    bfs_results = {}
    for mode in ["Top down", "Bottom up", "Hybrid"]:
        bfs_results[mode] = run_bfs_logging(mode, 22)
    with open("bfs_logging.json", "w") as f:
        json.dump(bfs_results, f, indent=4)

def plot_results(results, name):
    
    fontdict={'fontname': 'Arial', 'fontsize': fontsize}
    
    for key, times in results.items():
        if key == "Pull Async":
            marker = 'o'
        elif key == "Pull Sync":
            marker = 'x'
        elif key == "Push Async":
            continue
        elif key == "Push Sync":
            marker = '^'
        elif key == "Hybrid":
            marker = 'x'
        elif key == "Top down":
            marker = 'v'
        elif key == "Bottom up":
            marker = '^'
        else:
            marker = 'o'
        x_values = [2 ** i for i in range(10, 25)]
        plt.plot(x_values, times, label=key, marker=marker)
    
    plt.xticks(fontsize=fontdict['fontsize'], fontname=fontdict['fontname'])
    plt.yticks(fontsize=fontdict['fontsize'], fontname=fontdict['fontname'])
    
    plt.xlabel("Graph Size (number of vertices)", fontdict=fontdict)
    plt.xscale("log", base=2)
    plt.ylabel("Average Time (seconds)", fontdict=fontdict)
    plt.legend(prop={'family': fontdict['fontname'], 'size': fontdict['fontsize']})
    plt.tight_layout()
    plt.savefig(f"{name}_performance.pdf")
    plt.close()

def plot_pr_logging_results(results):
    fontdict={'fontname': 'Arial', 'fontsize': fontsize}
    
    for key, errors in results.items():
        if key == "Async":
            marker = 'o'
        else:
            marker = 'x'
        plt.plot(errors, label=key, marker=marker)
    
    plt.xticks(fontsize=fontdict['fontsize'], fontname=fontdict['fontname'])
    plt.yticks(fontsize=fontdict['fontsize'], fontname=fontdict['fontname'])
    
    plt.xlabel("Iteration", fontdict=fontdict)
    plt.ylabel("Error", fontdict=fontdict)
    plt.legend(prop={'family': fontdict['fontname'], 'size': fontdict['fontsize']})
    plt.tight_layout()
    plt.savefig(f"PageRank_logging_performance.pdf")
    plt.close()
    
def plot_bfs_logging_results(results):
    fontdict={'fontname': 'Arial', 'fontsize': fontsize}
    
    for key, steps in results.items():
        times = [step['time'] for step in steps]
        if key == "Hybrid":
            # For hybrid, we need to separate the steps
            td1_times = []
            td2_times = []
            bu_times = []
            td1_iters = []
            td2_iters = []
            bu_iters = []
            is_1 = True
            for i, step in enumerate(steps):
                if step['step'] == 'td':
                    if is_1:
                        td1_times.append(step['time'])
                        td1_iters.append(i)
                    else:
                        td2_times.append(step['time'])
                        td2_iters.append(i)
                elif step['step'] == 'bu':
                    bu_times.append(step['time'])
                    bu_iters.append(i)
                    is_1 = False
            plt.plot(td1_iters, td1_times, label=f"{key} (top down)", color = 'tab:red', marker='v')
            plt.plot(td2_iters, td2_times, color = 'tab:red', marker='v')
            plt.plot(bu_iters, bu_times, label=f"{key} (bottom up)", color = 'tab:red', marker='^')
        else:
            if key == "Top down":
                marker = 'v'
            elif key == "Bottom up":
                marker = '^'
            plt.plot(times, label=key, marker=marker)
    
    plt.xticks(fontsize=fontdict['fontsize'], fontname=fontdict['fontname'])
    plt.yticks(fontsize=fontdict['fontsize'], fontname=fontdict['fontname'])
    
    plt.xlabel("Step", fontdict=fontdict)
    plt.ylabel("Time (seconds)", fontdict=fontdict)
    plt.legend(prop={'family': fontdict['fontname'], 'size': fontdict['fontsize']}, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.3))
    plt.tight_layout()
    plt.savefig(f"BFS_logging_performance.pdf")
    plt.close()
        
if __name__ == "__main__":
    build()
    run_pr_tests()
    with open("pr_results.json", "r") as f:
        pr_results = json.load(f)
    plot_results(pr_results, "pagerank")
    print("PageRank tests completed and results saved to pr_results.json")
    
    run_bfs_tests()
    with open("bfs_results.json", "r") as f:
        bfs_results = json.load(f)
    plot_results(bfs_results, "bfs")
    print("BFS tests completed and results saved to bfs_results.json")
    
    run_logging()
    with open("pr_logging.json", "r") as f:
        pr_logging_results = json.load(f)
    plot_pr_logging_results(pr_logging_results)
    print("PageRank logging tests completed and results saved to pr_logging.json")
    
    with open("bfs_logging.json", "r") as f:
        bfs_logging_results = json.load(f)
    plot_bfs_logging_results(bfs_logging_results)
    print("BFS logging tests completed and results saved to bfs_logging.json")
    