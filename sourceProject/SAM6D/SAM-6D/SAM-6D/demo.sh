# Render CAD templates

set CAD_PATH=D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\obj_000005.ply
set RGB_PATH=D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\rgb.png
set DEPTH_PATH=D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\depth.png
set CAMERA_PATH=D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\camera.json
set OUTPUT_DIR=D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\outputs


cd Render
#blenderproc run render_custom_templates.py --output_dir $OUTPUT_DIR --cad_path $CAD_PATH #--colorize True
blenderproc run render_custom_templates.py --output_dir D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\outputs --cad_path D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\obj_000005.ply #--colorize True


# Run instance segmentation model
set SEGMENTOR_MODEL=sam

cd ../Instance_Segmentation_Model
#python run_inference_custom.py --segmentor_model $SEGMENTOR_MODEL --output_dir $OUTPUT_DIR --cad_path $CAD_PATH --rgb_path $RGB_PATH --depth_path $DEPTH_PATH --cam_path $CAMERA_PATH
python run_inference_custom.py --segmentor_model sam --output_dir D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\outputs --cad_path D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\obj_000005.ply --rgb_path D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\rgb.png --depth_path D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\depth.png --cam_path D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\camera.json


# Run pose estimation model
set SEG_PATH=$OUTPUT_DIR/sam6d_results/detection_ism.json

cd ../Pose_Estimation_Model
#python run_inference_custom.py --output_dir $OUTPUT_DIR --cad_path $CAD_PATH --rgb_path $RGB_PATH --depth_path $DEPTH_PATH --cam_path $CAMERA_PATH --seg_path $SEG_PATH
python run_inference_custom.py --output_dir D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\outputs --cad_path D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\obj_000005.ply --rgb_path D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\rgb.png --depth_path D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\depth.png --cam_path D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\camera.json --seg_path D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\outputs\sam6d_results\detection_ism.json

