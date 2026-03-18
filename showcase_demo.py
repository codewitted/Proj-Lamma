import os
import shutil
import subprocess
import time
from scripts.resource_manager import initialize_locks

def run_showcase():
    print("="*60)
    print("MSc RESEARCH SHOWCASE: HYBRID MULTI-ROBOT PLANNER")
    print("="*60)
    
    # 1. Setup Mock Logs
    expt_name = "showcase_warehouse_task"
    log_path = f"logs/{expt_name}"
    os.makedirs(log_path, exist_ok=True)
    
    print("\n[PHASE 1] PLANNING & ALLOCATION")
    print("Simulating LLM-based Warehouse PDDL Generation...")
    
    with open(f"{log_path}/log.txt", 'w') as f:
        f.write("task = Deliver kit to station 3\n")
        f.write("robots = [{'name': 'robot1'}, {'name': 'robot2'}]\n")
        f.write("ground_truth = []\n")
    
    with open(f"{log_path}/code_plan.py", 'w') as f:
        f.write("def task_cycle():\n")
        f.write("    reserve_aisle(robots[0], 'aisle_A')\n")
        f.write("    GoToLocation(robots[0]['name'], [2.5, 4.0])\n")
        f.write("    release_aisle(robots[0], 'aisle_A')\n")
    
    print("✓ PDDL Plan Generated in logs/")
    
    # 2. Setup Coordination
    print("\n[PHASE 2] MULTI-ROBOT COORDINATION")
    initialize_locks(["aisle_A", "aisle_B"])
    print("✓ Resource Manager Initialized (aisle_A, aisle_B)")

    # 3. Generate ROS2 Execution Script
    print("\n[PHASE 3] ROS2 EXECUTION BRIDGE")
    print("Compiling PDDL for ROS2/LIMO backend...")
    
    cmd = ["python3", "scripts/execute_plan.py", "--command", expt_name, "--backend", "ros2"]
    subprocess.run(cmd)
    
    expected_script = f"{log_path}/executable_plan_ros2.py"
    if os.path.exists(expected_script):
        print(f"✓ ROS2 Script Compiled: {expected_script}")
    
    print("\n" + "="*60)
    print("SHOWCASE COMPLETE: Ready for deployment to LIMO/Gazebo.")
    print("="*60)

if __name__ == "__main__":
    run_showcase()
