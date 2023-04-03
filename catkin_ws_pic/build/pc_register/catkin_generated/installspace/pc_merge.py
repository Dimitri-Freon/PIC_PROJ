#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from geometry_msgs.msg import PoseStamped
import open3d
#import lib_cloud_conversion_between_Open3D_and_ROS.convertCloudFromRosToOpen3d as convertCloudFromRosToOpen3d
from pc_conversion.lib_cloud_conversion import convertCloudFromRosToOpen3d
from pc_conversion.lib_cloud_conversion import convertCloudFromOpen3dToRos
from pc_conversion.conversion import convert_cloud_from_ros_to_o3d
from pc_conversion.conversion import convert_cloud_from_o3d_to_ros

import message_filters
import tf
import tf.transformations as transformations
from tf.transformations import quaternion_matrix

import numpy as np
import copy


def MsgToPose(msg):
        """
        Parse the ROS message to a 4x4 pose format
        @param msg The ros message containing a pose
        @return A 4x4 transformation matrix containing the pose
        as read from the message
        """
        #Get translation and rotation (from Euler angles)
        pose = quaternion_matrix(np.array([msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w]))
    
        pose[0,3] = msg.pose.position.x
        pose[1,3] = msg.pose.position.y
        pose[2,3] = msg.pose.position.z
        
        return pose

class pc_process():
    def __init__(self):
        s1 = message_filters.Subscriber("/zed2i/zed_node/point_cloud/cloud_registered", PointCloud2)
        s2 =message_filters.Subscriber("/zed2i/zed_node/pose", PoseStamped)
        #rospy.Subscriber('/zed2i/zed_node/point_cloud/cloud_registered', PointCloud2, self.callback_process_pointcloud)
        #rospy.Subscriber('/zed2i/zed_node/pose', PoseStamped, self.callback_process_pointcloud)
        s = message_filters.ApproximateTimeSynchronizer([s1, s2], 10, 1, allow_headerless=True)
        s.registerCallback(self.callback_process_pointcloud)

        self.pub = rospy.Publisher('/pc_affiche', PointCloud2, queue_size=3)
        self.pc_affiche = PointCloud2()
        

        self.pc_coordinate_original = open3d.geometry.PointCloud() # store the merge pcs under original coord
        self.pc_coordinate_cam = open3d.geometry.PointCloud()
        #self.T_last = transformations.identity_matrix() # store the trans matrix of last frame

        # Def bbox
        self.bbox = open3d.geometry.AxisAlignedBoundingBox(min_bound = np.array([-3,-3,-2]), max_bound = np.array([3,3,3]))
        self.numframe = 0
        #self.voxel_size = 0.2

        
  

    def callback_process_pointcloud(self, data1 , data2):

        T = MsgToPose(data2) # Homo transformation matrix 4*4 , actual frame to original coordinate
        

        assert isinstance(data1, PointCloud2)
        print(data1.row_step)
        received_open3d_cloud = convert_cloud_from_ros_to_o3d(data1) # conversion PointCloud2 -- > open3d.geometry.PointCloud()
 
            
        received_open3d_cloud = received_open3d_cloud.random_down_sample(sampling_ratio = 0.8)
        #received_open3d_cloud.estimate_normals()
        
        # transform actual pc to original coordinate, append(merge) to the self.pc_coordinate_original
        #self.pc_coordinate_original = self.pc_coordinate_original + received_open3d_cloud.transform(T)

        threshold = 0.05
        
        if self.pc_coordinate_original.has_points():
            ### icp
            #icp = open3d.pipelines.registration.registration_icp(received_open3d_cloud, self.pc_coordinate_original, threshold, T, open3d.pipelines.registration.TransformationEstimationPointToPoint())
            #T = icp.transformation
            ###
            self.pc_coordinate_original = self.pc_coordinate_original + received_open3d_cloud.transform(T)
            
        else:
            self.pc_coordinate_original = received_open3d_cloud.transform(T)

        

        # Crop the pc ( Transform back to cam coord )
        T_inv = transformations.inverse_matrix(T) # use to transfer actual frame(cam coordinate) to original coordinate
        self.pc_coordinate_original.transform(T_inv)
        self.pc_coordinate_original = self.pc_coordinate_original.crop(self.bbox)
        # Downsample the point cloud with a voxel 
        self.pc_coordinate_original = self.pc_coordinate_original.voxel_down_sample(voxel_size= 0.023)
        #self.pc_coordinate_original = self.pc_coordinate_original.random_down_sample(sampling_ratio = 0.5)

        self.pc_coordinate_original.remove_non_finite_points()
        print(self.pc_coordinate_original.__sizeof__())
        print(np.shape(self.pc_coordinate_original.colors))
        
        self.pc_coordinate_cam = copy.deepcopy(self.pc_coordinate_original)
        a = transformations.euler_matrix(0, 0.733, 0, axes='sxyz')
        self.pc_coordinate_cam = self.pc_coordinate_cam.rotate(a[0:3,0:3])

        # Transform back to original coord
        self.pc_coordinate_original.transform(T)


    
        open3d.io.write_point_cloud("copy_of_fragment.pcd", self.pc_coordinate_cam)
        print("renouveler",self.numframe)
        self.numframe = self.numframe + 1

        self.pc_affiche = convert_cloud_from_o3d_to_ros(self.pc_coordinate_cam)
        self.pc_coordinate_cam.clear()
        if np.shape(self.pc_coordinate_original.colors)[0] > 30000:
            self.pc_coordinate_original = self.pc_coordinate_original.random_down_sample(sampling_ratio = 0.7)
        self.pub.publish(self.pc_affiche)
        #self.pub.publish(data1)
        
        


if __name__ == '__main__':
    rospy.init_node('pc_processor', anonymous=True)
    try:
        pc_process()
    except rospy.ROSInterruptException:
        pass
    rospy.spin()





