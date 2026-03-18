import os
from pathlib import Path
import subprocess
import argparse

def append_trans_ctr(allocated_plan):
    brk_ctr = 0
    code_segs = allocated_plan.split("\n\n")
    for cd in code_segs:
        if "def" not in cd and "threading.Thread" not in cd and "join" not in cd and cd.strip().endswith(")"):
            brk_ctr += 1
    print("No Breaks: ", brk_ctr)
    return brk_ctr

def compile_exec_file(expt_name, backend="aithor"):
    log_path = os.getcwd() + "/logs/" + expt_name
    executable_plan = ""
    
    # Select templates based on backend
    if backend == "ros2":
        connect_dir = "ros2_connect"
        import_suffix = "_ros2"
        connect_suffix = "" # ros2_connect.py
        end_suffix = "_ros2"
    else:
        connect_dir = "aithor_connect"
        import_suffix = "_aux_fn"
        connect_suffix = "" # aithor_connect.py
        end_suffix = ""

    # 1. append the imports to the file
    import_path = os.getcwd() + f"/data/{connect_dir}/imports{import_suffix}.py"
    import_file = Path(import_path).read_text()
    executable_plan += (import_file + "\n")
    
    # 2. append the list of robots and ground truth from log file
    log_file_path = log_path + "/log.txt"
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            log_data = log_file.readlines()
        
        # Find robots line
        robots_line = None
        for line in log_data:
            if "robots = " in line:
                robots_line = line.strip()
                break
        
        if robots_line:
            executable_plan += (robots_line + "\n")
        else:
            executable_plan += ("robots = [{'name': 'robot1', 'skills': ['GoToObject', 'PickupObject', 'PutObject'], 'mass': 100}]\n")
        
        # Find ground truth line
        gt_line = None
        for line in log_data:
            if "ground_truth = " in line:
                gt_line = line.strip()
                break
        if gt_line:
            executable_plan += (gt_line + "\n")
        else:
            executable_plan += ("ground_truth = []\n")
    else:
        executable_plan += ("robots = [{'name': 'robot1'}]\nground_truth = []\n")

    executable_plan += ("floor_no = 1\nno_trans_gt = 0\nmax_trans = 10\n\n")
    
    # 3. append the connector and helper fns
    connector_filename = "ros2_connect.py" if backend == "ros2" else "aithor_connect.py"
    connector_path = os.getcwd() + f"/data/{connect_dir}/{connector_filename}"
    connector_file = Path(connector_path).read_text()
    executable_plan += (connector_file + "\n")
    
    # 4. append the allocated plan
    code_plan_path = log_path + "/code_plan.py"
    if os.path.exists(code_plan_path):
        allocated_plan = Path(code_plan_path).read_text()
        
        # Replace empty robots list with actual robots from log file
        if 'robots_line' in locals() and robots_line:
            allocated_plan = allocated_plan.replace("robots = []", robots_line.strip())
            allocated_plan = allocated_plan.replace("robots = ['robot1']", robots_line.strip())
            allocated_plan = allocated_plan.replace("robots = ['Robot2']", robots_line.strip())
        
        brks = append_trans_ctr(allocated_plan)
        executable_plan += (allocated_plan + "\n")
        executable_plan += ("no_trans = " + str(brks) + "\n")
    else:
        executable_plan += "no_trans = 0\n"

    # 5. append the task thread termination
    terminate_path = os.getcwd() + f"/data/{connect_dir}/end_thread{end_suffix}.py"
    terminate_plan = Path(terminate_path).read_text()
    executable_plan += (terminate_plan + "\n")

    output_file = f"{log_path}/executable_plan_{backend}.py"
    with open(output_file, 'w') as d:
        d.write(executable_plan)
        
    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", type=str, required=True, help="Experiment log name")
    parser.add_argument("--backend", type=str, default="aithor", choices=["aithor", "ros2"], help="Execution backend")
    args = parser.parse_args()

    expt_name = args.command
    print(f"Compiling for backend: {args.backend}")
    exec_file = compile_exec_file(expt_name, args.backend)

    if args.backend == "aithor":
        subprocess.run(["python3", exec_file])
    else:
        print(f"Generated ROS2 execution script: {exec_file}")
        print("Note: Run in a ROS2-enabled environment with: python3 [file]")