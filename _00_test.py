# @FileName :_00_test.py
# @Time :2025/4/21 下午3:09
# @Author : SCUT hm



import subprocess

def rend():
    # 定义BlenderProc脚本路径
    blenderproc_script = r"D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Render\render_custom_templates.py"
    output_dir= r"D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\outputs"
    cad_path = r"D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\obj_000005.ply"

    cmd=f"python -m blenderproc run {blenderproc_script} --output_dir {output_dir} --cad_path {cad_path}"

    try:
        # 执行命令
        result = subprocess.run(cmd, check=True)
        print("执行成功！")
        print("输出：", result.stdout)
    except subprocess.CalledProcessError as e:
        print("执行失败！错误信息：")
        print(e.stderr)

def SAM():
    # --segmentor_model
    # sam - -output_dir
    # D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM - 6
    # D\SAM - 6
    # D\Data\Example\outputs - -cad_path
    # D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM - 6
    # D\SAM - 6
    # D\Data\Example\obj_000005.ply - -rgb_path
    # D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM - 6
    # D\SAM - 6
    # D\Data\Example\rgb.png - -depth_path
    # D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM - 6
    # D\SAM - 6
    # D\Data\Example\depth.png - -cam_path
    # D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM - 6
    # D\SAM - 6
    # D\Data\Example\camera.json

    py_file=r"D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Instance_Segmentation_Model\run_inference_custom.py"

    segmentor_model = "sam"
    output_dir = r"D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\outputs"
    cad_path = r"D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\obj_000005.ply"
    rgb_path = r"D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\rgb.png"
    depth_path = r"D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\depth.png"
    cam_path = r"D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\camera.json"
    cmd = f"python {py_file} --segmentor_model {segmentor_model} --output_dir {output_dir} --cad_path {cad_path} --rgb_path {rgb_path} --depth_path {depth_path} --cam_path {cam_path}"

    try:
        # 执行命令
        result = subprocess.run(cmd, check=True)
        print("执行成功！")
        print("输出：", result.stdout)
    except subprocess.CalledProcessError as e:
        print("执行失败！错误信息：")
        print(e.stderr)



if __name__ == "__main__":
    # rend()
    SAM()