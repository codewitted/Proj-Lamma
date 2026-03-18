
print("Shutting down ROS2 Execution Bridge...")
task_over = True
time.sleep(2)
rclpy.shutdown()
print("Execution Complete.")
