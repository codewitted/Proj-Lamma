
print("Initializing ROS2 Execution Bridge...")
rclpy.init()

class RobotExecutor(Node):
    def __init__(self):
        super().__init__('robot_executor')
        self.nav_clients = {}
        for robot in robots:
            name = robot['name']
            self.nav_clients[name] = ActionClient(self, NavigateToPose, f'/{name}/navigate_to_pose')
            self.get_logger().info(f'Setup Nav2 client for {name}')

executor_node = RobotExecutor()

def spin_ros():
    rclpy.spin(executor_node)

ros_thread = threading.Thread(target=spin_ros, daemon=True)
ros_thread.start()

def GoToLocation(robot_name, target_pose):
    print(f"[{robot_name}] Navigating to {target_pose}...")
    client = executor_node.nav_clients[robot_name]
    if not client.wait_for_server(timeout_sec=5.0):
        print(f"Error: Nav2 server for {robot_name} not available")
        return False
    
    goal_msg = NavigateToPose.Goal()
    goal_msg.pose.header.frame_id = 'map'
    goal_msg.pose.pose.position.x = target_pose[0]
    goal_msg.pose.pose.position.y = target_pose[1]
    # Simplified orientation
    goal_msg.pose.pose.orientation.w = 1.0
    
    send_goal_future = client.send_goal_async(goal_msg)
    # In a real system, we'd wait for result. For MVP, we'll block.
    while not send_goal_future.done():
        time.sleep(0.1)
    
    goal_handle = send_goal_future.result()
    if not goal_handle.accepted:
        print(f"Goal rejected for {robot_name}")
        return False
        
    result_future = goal_handle.get_result_async()
    while not result_future.done():
        time.sleep(0.1)
    
    print(f"[{robot_name}] Reached Goal.")
    return True

# Map existing AI2Thor action names to ROS2 equivalents for compatibility
def GoToObject(robot, dest_obj):
    # In real ROS2, we'd look up the object coordinates in a TF or database
    # For now, just a placeholder coordinate
    target_pose = [0.0, 0.0] 
    return GoToLocation(robot['name'], target_pose)

def PickupObject(robot, pick_obj):
    print(f"[{robot['name']}] Picking up {pick_obj} (ROS2 Action placeholder)")
    time.sleep(1)


from scripts.resource_manager import reserve_resource, release_resource

def reserve_aisle(robot, aisle):
    print(f"[{robot['name']}] Requesting reservation for {aisle}...")
    return reserve_resource(robot['name'], aisle)

def release_aisle(robot, aisle):
    print(f"[{robot['name']}] Requesting release for {aisle}...")
    return release_resource(robot['name'], aisle)

def PutObject(robot, put_obj, recp):
    print(f"[{robot['name']}] Putting {put_obj} on {recp} (ROS2 Action placeholder)")
    time.sleep(1)
