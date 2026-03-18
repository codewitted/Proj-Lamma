import threading
import time
from scripts.resource_manager import initialize_locks, reserve_resource, release_resource

def robot_task(robot_name, aisle):
    print(f"[{robot_name}] Starting task...")
    if reserve_resource(robot_name, aisle):
        print(f"[{robot_name}] Working in {aisle}...")
        time.sleep(2)
        release_resource(robot_name, aisle)
    print(f"[{robot_name}] Task finished.")

if __name__ == "__main__":
    initialize_locks(["aisle_1", "aisle_2"])
    
    # Simulate two robots competing for aisle_1
    t1 = threading.Thread(target=robot_task, args=("Robot_1", "aisle_1"))
    t2 = threading.Thread(target=robot_task, args=("Robot_2", "aisle_1"))
    
    t1.start()
    time.sleep(0.5) # Ensure Robot 1 gets it first
    t2.start()
    
    t1.join()
    t2.join()
    print("Contention test complete.")
