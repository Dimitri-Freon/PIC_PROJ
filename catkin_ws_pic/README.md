
# Requirement: 
Install zed-ros-wrapper zed-ros-examples follow tutorial 1
Install open3D
# ROS1 Noetic
# To run : 
# Build package (terminal 1)
cd ~/catkin_ws_pic
catkin_make
source ./devel/setup.bash
# T2 launch camera
roslaunch zed_wrapper zed2i.launch

rosrun pc_register pc_merge.py
roslaunch pc_display display.launch









# Les remarques diverses


# run zed-ros in a second terminal (cd ~/catkin_ws_pic)
  # Launching with recorded SVO video
  roslaunch zed_wrapper zed2i.launch svo_file:=/home/ruan/Desktop/svo_file/28.svo
  # or
  # Launching Cam
  roslaunch zed_wrapper zed2i.launch

  roslaunch zed_wrapper zed2i.launch cam_pose_z:=1 cam_pitch:=0.733
  roslaunch zed_wrapper zed2i.launch svo_file:=/home/ruan/Desktop/svo_file/28.svo cam_pose_z:=1 cam_pitch:=0.733


# run node (terminal 1)
  rosrun pc_register pc_merge.py

# the node publish topic : /pc_affiche
self.pub = rospy.Publisher('/pc_affiche', PointCloud2, queue_size=10)
# see site below for conversiion open3d - PointCloud2 , 
# conversion.py is use in node script pc_merge.py, from package catkin_ws_pic/src/pc_register/scripts/pc_conversion
https://github.com/IASRobolab/o3d_ros_point_cloud_converter/blob/master/o3d_ros_point_cloud_converter/conversion.py
# To see the result of merged pc (not real time)
 open the file example_result.pcd with point cloud viewer

#
ruan@ruan:~/catkin_ws_pic$ roslaunch pc_display display.launch





# Tutorial 1
# Install zed-ros-wrapper
$ cd ~/catkin_ws/src
$ git clone --recursive https://github.com/stereolabs/zed-ros-wrapper.git # skip this step
$ cd ../
$ rosdep install --from-paths src --ignore-src -r -y
$ catkin_make -DCMAKE_BUILD_TYPE=Release
$ source ./devel/setup.bash
# Install zed-ros-examples
$ cd ~/catkin_ws/src
$ git clone https://github.com/stereolabs/zed-ros-examples.git  # skip this step
$ cd ../
$ rosdep install --from-paths src --ignore-src -r -y
$ catkin_make -DCMAKE_BUILD_TYPE=Release
$ source ./devel/setup.bash


# Launching with recorded SVO video
roslaunch zed_wrapper zed2i.launch svo_file:=/home/ruan/Desktop/svo_file/28.svo
# Launching Cam
roslaunch zed_wrapper zed2i.launch

# Displaying ZED data
roslaunch zed_display_rviz display_zed2i.launch

# Topic Registered color point cloud
rostopic info /zed2i/zed_node/point_cloud/cloud_registered
/zed2i/zed_node/point_cloud/cloud_registered

# Create Package
cd ~/catkin_ws/src
catkin_create_pkg pc_register std_msgs rospy roscpp

# pc_register/src/pc_merge.py
# Add the following to your CMakeLists.txt
catkin_install_python(PROGRAMS src/pc_merge.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

catkin_install_python(PROGRAMS scripts/talker.py scripts/listener.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


# Compile Package 
cd ~/catkin_ws
catkin_make

# Compile certain packages
catkin_make -DCATKIN_WHITELIST_PACKAGES="package1;package2"
cd ~/catkin_ws
catkin_make -DCATKIN_WHITELIST_PACKAGES=”pc_register”

# 在一个新的Terminal中运行roscore后，再试一下运行
source ./devel/setup.bash
rosrun pc_register pc_merge.py

# 如果想恢复编译所有软件包，在终端中输入如下命令 recover package builed 
catkin_make -DCATKIN_WHITELIST_PACKAGES=""

# type rostopic /point_cloud/cloud_registered topic information
ruan@ruan:~/catkin_ws_pic$ rostopic info /zed2i/zed_node/point_cloud/cloud_registered
Type: sensor_msgs/PointCloud2

Publishers: 
 * /zed2i/zed_node (http://ruan:43985/)






# ROS中PointCloud转换为PointCloud2类型, TRANSFORM pointcloud open3D and PointCloud2 ROS
# conversion.py
convertPointCloudToPointCloud2
https://github.com/felixchenfy/open3d_ros_pointcloud_conversion 
new: https://github.com/IASRobolab/o3d_ros_point_cloud_converter/blob/master/o3d_ros_point_cloud_converter/conversion.py


# open3d.geometry.PointCloud
http://www.open3d.org/docs/0.6.0/python_api/open3d.geometry.PointCloud.html

