import json
import os
import time

LOCK_FILE = "warehouse_locks.json"

def initialize_locks(resources):
    with open(LOCK_FILE, 'w') as f:
        json.dump({res: None for res in resources}, f)

def reserve_resource(robot_name, resource_id):
    while True:
        try:
            with open(LOCK_FILE, 'r+') as f:
                locks = json.load(f)
                if locks.get(resource_id) is None:
                    locks[resource_id] = robot_name
                    f.seek(0)
                    json.dump(locks, f)
                    f.truncate()
                    print(f"[{robot_name}] Reserved {resource_id}")
                    return True
                elif locks.get(resource_id) == robot_name:
                    return True # Already reserved
        except Exception:
            pass
        print(f"[{robot_name}] Waiting for {resource_id}...")
        time.sleep(1)

def release_resource(robot_name, resource_id):
    try:
        with open(LOCK_FILE, 'r+') as f:
            locks = json.load(f)
            if locks.get(resource_id) == robot_name:
                locks[resource_id] = None
                f.seek(0)
                json.dump(locks, f)
                f.truncate()
                print(f"[{robot_name}] Released {resource_id}")
                return True
    except Exception:
        pass
    return False
