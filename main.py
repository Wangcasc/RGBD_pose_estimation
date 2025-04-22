# @FileName :main.py
# @Time :2025/4/8 上午10:48
# @Author : SCUT Lu

#系统
import os
import sys

#pyqt
from PyQt5 import  QtWidgets
from PyQt5.Qt import *

#UI
from UI.HM_UI import Ui_Main #UI界面，使用QtDesigner设计

# multiprocessing多进程
from multiprocessing import Pipe, Process, Event,Manager
from process.cameraProcess import run_camera

# style 样式
from qt_material import apply_stylesheet

# opencv
import cv2

import subprocess

class Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.init_UI()



        # 显示
        self.timer_imshow = QTimer(self)
        self.timer_imshow.timeout.connect(self.show_img)
        self.timer_imshow.start(10) # 100ms刷新一次


        # pushButton_path链接到选择路径函数
        self.ui.pushButton_path.clicked.connect(self.select_path)
        # pushButton_model链接到选择模型函数
        self.ui.pushButton_model.clicked.connect(self.select_model)
        self.cad_path = None



        # pushButton_camera链接到相机函数
        self.ui.pushButton_camera.clicked.connect(self.camera)
        self.camera_process = None # 相机进程
        self.cameraOpen = False # 相机是否打开
        self.parent_conn, self.child_conn = Pipe()
        self.stop_event = Event()
        self.NS = Manager().Namespace()  # 共享内存

        # pushButton_shoot链接到拍照函数
        self.ui.pushButton_shoot.clicked.connect(self.shoot)



    def init_UI(self):


        self.default_things_path = os.path.join(os.getcwd(), "things")  # 默认路径

        self.ui.label_img.setScaledContents(True) # 设置图片自适应
        self.ui.label_img.setPixmap(QPixmap("UI/imgs/no_img.jpg")) # 设置默认图片

        self.ui.label_img_RGB.setScaledContents(True) # 设置图片自适应
        self.ui.label_img_RGB.setPixmap(QPixmap("UI/imgs/no_img.jpg")) # 设置默认图片

        self.ui.label_img_Depth.setScaledContents(True) # 设置图片自适应
        self.ui.label_img_Depth.setPixmap(QPixmap("UI/imgs/no_img.jpg")) # 设置默认图片

        self.ui.label_img_Seg.setScaledContents(True) # 设置图片自适应
        self.ui.label_img_Seg.setPixmap(QPixmap("UI/imgs/no_img.jpg")) # 设置默认图片

        self.ui.label_img_Pose.setScaledContents(True) # 设置图片自适应
        self.ui.label_img_Pose.setPixmap(QPixmap("UI/imgs/no_img.jpg")) # 设置默认图片

        self.output_path ="outputs"


    def select_path(self):
        # 设置默认路径
        default_path = self.default_things_path
        # 如果默认路径不存在，使用当前工作目录
        if not os.path.exists(default_path):
            default_path = os.getcwd()
        # 打开文件选择对话框
        folder = QFileDialog.getExistingDirectory(self, "选择模型库路径",default_path)
        if folder:
            self.ui.textBrowser_path.setText(folder)
            self.default_things_path = folder  # 更新默认路径
        else:
            QMessageBox.warning(self, "警告", "未选择任何路径！")
            self.default_things_path = os.getcwd()  # 如果没有选择路径，使用当前工作目录

    def select_model(self):
        # 设置默认路径
        default_root = self.default_things_path
        default_path = os.path.join(default_root, "samples")

        # 如果默认路径不存在，使用当前工作目录
        if not os.path.exists(default_path):
            default_path = os.getcwd()
        # 打开文件选择对话框
        file, _ = QFileDialog.getOpenFileName(self, "选择模型文件", default_path, "Model Files (*.ply)")
        if file:
            self.ui.textBrowser_model.setText(file)
            # self.default_things_path = os.path.dirname(file)
            self.cad_path = file
            cad_model_name = file.split("/")[-1].split(".")[0] #
            print("cad_model_name:",cad_model_name)
            # 新建一个名字为cad_model_name的文件夹
            folder_path = os.path.join(self.output_path, cad_model_name)
            if not os.path.exists(folder_path): #没有这个文件夹，意味着这个cadmodel没有渲染过
                os.makedirs(folder_path)
                self.rend(folder_path) #渲染
                self.SAM(folder_path)
            else:
                # 提示文件夹已存在
                QMessageBox.warning(self, "警告", "该模型已经完成渲染！")
                self.ui.textBrowser_model.setText("")


    def rend(self,folder_path):
        # 定义BlenderProc脚本路径
        blenderproc_script = r"D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Render\render_custom_templates.py"
        output_dir = folder_path
        cad_path = self.cad_path

        cmd = f"python -m blenderproc run {blenderproc_script} --output_dir {output_dir} --cad_path {cad_path}"

        try:
            # 执行命令
            # 阻塞用户按键，等待执行完成
            self.ui.toolBox.setEnabled(False)  # 禁用按钮
            QMessageBox.information(self, "提示", "开始渲染！请稍候...")
            result = subprocess.run(cmd, check=True)
            print("执行成功！")
            print("输出：", result.stdout)
            # 输出在日志框中
            self.ui.textBrowser_log.append("执行成功！")
            self.ui.textBrowser_log.append("输出：%s" % result.stdout)
            # 提示渲染完成
            QMessageBox.information(self, "提示", "渲染完成！")
            # 恢复按钮
            self.ui.toolBox.setEnabled(True)  # 恢复按钮
        except subprocess.CalledProcessError as e:
            print("执行失败！错误信息：")
            print(e.stderr)

    def SAM(self,folder_path):

        py_file = r"D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Instance_Segmentation_Model\run_inference_custom.py"

        segmentor_model = "sam"
        output_dir = folder_path
        # r"D:\wxl\pycharmProject\RGBD_POSE_ESTIMATION\sourceProject\SAM6D\SAM-6D\SAM-6D\Data\Example\obj_000005.ply"
        cad_path =  self.cad_path
        cad_model_name = cad_path.split("/")[-1]
        rgb_path = self.cad_path.replace(cad_model_name, "rgb.png")
        depth_path = self.cad_path.replace(cad_model_name, "depth.png")
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

    def camera(self):
        if self.cameraOpen==False:
            # 开启相机进程
            print("开启相机进程")
            # 禁用按钮
            self.ui.pushButton_camera.setEnabled(False)
            # 创建管道
            self.parent_conn, self.child_conn = Pipe()
            self.stop_event = Event()
            self.NS = Manager().Namespace()  # 共享内存

            # 输出在日志框中
            self.ui.textBrowser_log.append("开启相机进程")
            self.cameraOpen = True

            self.NS.record_save = False # 记录保存
            self.NS.frameRates = 0

            self.camera_process = Process(target=run_camera, args=(self.child_conn, self.stop_event,self.NS))
            self.camera_process.start()

            self.ui.pushButton_camera.setText("关闭相机")
            # self.ui.pushButton_camera.setStyleSheet("background-color: rgb(255, 0, 0);") # 设置按钮颜色为红色
            # 设置按钮文字颜色为红色
            self.ui.pushButton_camera.setStyleSheet("color: rgb(255, 0, 0);")
            self.ui.pushButton_camera.setEnabled(True) # 重新启用按钮
        else:
            # 关闭相机进程
            print("关闭相机进程")
            # 输出在日志框中
            self.ui.textBrowser_log.append("关闭相机进程")
            # 禁用按钮
            self.ui.pushButton_camera.setEnabled(False)


            self.cameraOpen = False
            # 等待相机进程结束
            self.parent_conn.close() # 关闭管道，防止卡死 非常重要
            self.stop_event.set()
            self.camera_process.join()
            self.ui.pushButton_camera.setText("打开相机")
            # 设置按钮文字颜色为绿色
            self.ui.pushButton_camera.setStyleSheet("color: rgb(0, 255, 0);")
            self.ui.label_img.setPixmap(QPixmap("UI/imgs/no_img.jpg"))  # 设置默认图片
            self.ui.pushButton_camera.setEnabled(True) # 重新启用按钮

    def show_img(self):
        try:
            if self.parent_conn.poll(): # 如果有数据
                frame = self.parent_conn.recv() # 接收数据
                if isinstance(frame, str): # 如果是字符串，说明相机关闭
                    print(frame)
                    self.ui.textBrowser_log.append(frame)
                    return
                else:
                    # 显示图片
                    qimg = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(qimg)
                    self.ui.label_img.setPixmap(pixmap)
        except Exception as e:
            print("Warnnig:", e)
            # self.ui.textBrowser_log.append("Error: %s" % e)
            return

    def closeEvent(self, event):
        # self.timer_imshow.stop()
        #关闭管道，防止卡死
        self.parent_conn.close()
        #设置停止事件
        self.stop_event.set()

        # 等待相机进程结束
        if self.camera_process is not None:
            self.camera_process.join()
        event.accept()

    def shoot(self):
        # 拍照
        if self.cameraOpen == True:
            print("拍摄")
            # 输出在日志框中
            self.ui.textBrowser_log.append("拍摄")
            # self.NS.record_save = True
            img= self.parent_conn.recv()

            # 显示图片
            qimg = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.ui.label_img_RGB.setPixmap(pixmap)

            img= cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            # 根据时间戳命名图片
            # 获取当前时间
            current_time = QDateTime.currentDateTime()
            # 格式化时间
            time_str = current_time.toString("yyyyMMdd_hhmmss")
            # 根据时间创建文件夹
            folder_path = os.path.join(self.output_path, time_str)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            # 保存图片
            img_path = os.path.join(folder_path, "img.png")
            cv2.imwrite(img_path, img)




        else:
            # 提示相机未打开
            print("相机未打开")
            # 输出在日志框中
            self.ui.textBrowser_log.append("相机未打开")
            #
            QMessageBox.warning(None, "提示", "请先打开相机")


            # 暂停相机传输

if __name__ == "__main__":
    # 加上下面这行 就可解决部分分辨率下 控件、文字显示不完整问题
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)

    # 设置主题
    # 暗黑色主题
    # apply_stylesheet(app,theme='dark_teal.xml', extra=extra)
    apply_stylesheet(app,theme='dark_pink.xml')

    # 浅色主题
    # apply_stylesheet(app,theme='light_blue.xml')

    window = Main_Window()
    window.show()
    sys.exit(app.exec_())