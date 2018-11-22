from gazebo_msgs.srv import SpawnModel

import rclpy


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('minimal_client')
    cli = node.create_client(SpawnModel, '/spawn_entity')

    content = ""
    with open('/home/erle/ros2_mara_ws/src/mara/mara_description/urdf/mara_robot_camera_top.urdf', 'r') as content_file:
        content = content_file.read()
        print(content)
        req = SpawnModel.Request()
        req.model_name = "mara"
        req.model_xml = content
        req.robot_namespace = ""
        req.reference_frame = "world"

        while not cli.wait_for_service(timeout_sec=1.0):
            node.get_logger().info('service not available, waiting again...')

        future = cli.call_async(req)
        rclpy.spin_until_future_complete(node, future)

        if future.result() is not None:
            node.get_logger().info(
                'Result ' + str(future.result().success) + " " + future.result().status_message)
        else:
            node.get_logger().info('Service call failed %r' % (future.exception(),))

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
