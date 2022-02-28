def register_one_rgbd_pair1(s, t, color_files, depth_files, intrinsic,
                           with_opencv, config):
    source_rgbd_image = read_rgbd_image(color_files[s], depth_files[s], True,
                                        config)
    target_rgbd_image = read_rgbd_image(color_files[t], depth_files[t], True,
                                        config)

    option = o3d.pipelines.odometry.OdometryOption()
    option.max_depth_diff = config["max_depth_diff"]
    if abs(s - t) != 1:
        if with_opencv:
            success_5pt, odo_init = pose_estimation(source_rgbd_image,
                                                    target_rgbd_image,
                                                    intrinsic, False)
            if success_5pt:
                [success, trans, info
                ] = o3d.pipelines.odometry.compute_rgbd_odometry(
                    source_rgbd_image, target_rgbd_image, intrinsic, odo_init,
                    o3d.pipelines.odometry.RGBDOdometryJacobianFromHybridTerm(),
                    option)
                return [success, trans, info]
        return [False, np.identity(4), np.identity(6)]
    else:
        odo_init = np.identity(4)
        [success, trans, info] = o3d.pipelines.odometry.compute_rgbd_odometry(
            source_rgbd_image, target_rgbd_image, intrinsic, odo_init,
            o3d.pipelines.odometry.RGBDOdometryJacobianFromHybridTerm(), option)
        return [success, trans, info]

#############################################################################
############# support functions for register_one_rgbd_pair ##################
#############################################################################
def get_pose_difference(s,t, config):
    #takes two poses pose_files[s], pose_files[t] and returns the vector path 
    # between the two

    #load s and t 
    #print("test get pose difference {}".format(config["path_dataset"] + "pose/"+str(s).zfill(5) + ".npy"))
    pose_source = np.load(config["path_dataset"] + "pose/"+str(s).zfill(5) + ".npy")
    pose_target = np.load(config["path_dataset"] + "pose/"+str(t).zfill(5) + ".npy")
    #print(pose_source)
    
    #print(np.matmul(np.linalg.inv(pose_source),pose_target))
    return np.matmul(pose_target,np.linalg.inv(pose_source))

#############################################################################
############# New version of register_one_rgbd_pair #########################
#############################################################################
#soft inserting of  pose estimates
def register_one_rgbd_pair2(s, t, color_files, depth_files, intrinsic,
                           with_opencv, config):
    source_rgbd_image = read_rgbd_image(color_files[s], depth_files[s], True,
                                        config)
    target_rgbd_image = read_rgbd_image(color_files[t], depth_files[t], True,
                                        config)
    

    option = o3d.pipelines.odometry.OdometryOption()
    option.max_depth_diff = config["max_depth_diff"]
    if abs(s - t) != 1:
        if with_opencv:
            success_5pt, odo_init = pose_estimation(source_rgbd_image,
                                                    target_rgbd_image,
                                                    intrinsic, False)
            if success_5pt:
                [success, trans, info
                ] = o3d.pipelines.odometry.compute_rgbd_odometry(
                    source_rgbd_image, target_rgbd_image, intrinsic, odo_init,
                    o3d.pipelines.odometry.RGBDOdometryJacobianFromHybridTerm(),
                    option)
                return [success, trans, info]
        return [False, np.identity(4), np.identity(6)]
    else:
        odo_init = get_pose_difference(s,t,config)
        [success, trans, info] = o3d.pipelines.odometry.compute_rgbd_odometry(
            source_rgbd_image, target_rgbd_image, intrinsic, odo_init,
            o3d.pipelines.odometry.RGBDOdometryJacobianFromHybridTerm(), option)
        return [success, trans, info]


# hard inserting of pose estimates
def register_one_rgbd_pair3(s, t, color_files, depth_files, intrinsic,
                           with_opencv, config):
    source_rgbd_image = read_rgbd_image(color_files[s], depth_files[s], True,
                                        config)
    target_rgbd_image = read_rgbd_image(color_files[t], depth_files[t], True,
                                        config)
    
    option = o3d.pipelines.odometry.OdometryOption()
    option.max_depth_diff = config["max_depth_diff"]
    
    odo_init = get_pose_difference(s,t,config)
    [success, trans, info] = o3d.pipelines.odometry.compute_rgbd_odometry(
        source_rgbd_image, target_rgbd_image, intrinsic, odo_init,
        o3d.pipelines.odometry.RGBDOdometryJacobianFromHybridTerm(), option)
    return [success, trans, info]

#python run_system.py D:\git\reconstructor\tmp\t11_1_single\config.json --make --register --refine --integrate

#python run_system.py D:\git\reconstructor\tmp\t11\config.json --integrate