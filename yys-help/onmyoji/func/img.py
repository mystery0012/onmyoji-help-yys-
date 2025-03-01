import cv2
import pyautogui
from PyQt5.QtWidgets import QApplication
import win32gui
import sys
from func import hwnd
import numpy as np
from config import CONFIG
import logging

def shoot():
    """截图函数"""
    handle = hwnd.return_handle()
    if handle != 0:
        try:
            # 获取窗口位置
            x, y = hwnd.get_window_position(handle)
            logging.info(f"准备截图，窗口位置: ({x}, {y})")
            
            app = QApplication(sys.argv)
            screen = QApplication.primaryScreen()
            img = screen.grabWindow(handle).toImage()
            img.save(CONFIG['IMAGE_PATHS']['SCREENSHOT'])
            logging.info("截图保存成功")
            print("保存图片")
        except Exception as e:
            logging.error(f"截图过程发生错误: {str(e)}")
    else:
        logging.error("未找到窗口，无法截图")
        print("未找到窗口")

def recognize_image(target_image_path):
    """图像识别函数"""
    try:
        confidence = CONFIG['IMAGE_RECOGNITION']['CONFIDENCE']
        grayscale = CONFIG['IMAGE_RECOGNITION']['GRAYSCALE']
        
        # 获取窗口位置
        handle = hwnd.return_handle()
        if handle == 0:
            logging.error("未找到窗口，无法进行图像识别")
            return False, None, None
            
        x, y = hwnd.get_window_position(handle)
        logging.info(f"开始图像识别，窗口位置: ({x}, {y})")

        # 加载模板图像为灰度图
        target_img = cv2.imread(target_image_path, 0)
        if target_img is None:
            logging.error(f"无法加载图像: {target_image_path}")
            return False, None, None

        # 截取屏幕图像并转换为灰度图
        screen_img = pyautogui.screenshot()
        screen_img_bgr = cv2.cvtColor(np.array(screen_img), cv2.COLOR_RGB2BGR)
        screen_gray = cv2.cvtColor(screen_img_bgr, cv2.COLOR_BGR2GRAY)

        # 使用模板匹配算法
        result = cv2.matchTemplate(screen_gray, target_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 设置匹配阈值
        threshold = confidence
        if max_val >= threshold:
            # 获取匹配位置的左上角和右下角坐标
            top_left = max_loc
            bottom_right = (top_left[0] + target_img.shape[1], top_left[1] + target_img.shape[0])

            logging.info(f"图像识别成功，匹配度: {max_val:.2f}")
            logging.debug(f"匹配位置 - 左上角: {top_left}, 右下角: {bottom_right}")
            
            return True, top_left, bottom_right
        else:
            logging.debug(f"未找到匹配图像，最大匹配度: {max_val:.2f}")
            return False, None, None
            
    except Exception as e:
        logging.error(f"图像识别过程发生错误: {str(e)}")
        return False, None, None

def capture_screenshot():
    """捕获屏幕截图"""
    try:
        # 获取窗口位置
        handle = hwnd.return_handle()
        x, y = hwnd.get_window_position(handle)
        logging.info(f"准备捕获屏幕，窗口位置: ({x}, {y})")
        
        # 使用pyautogui捕获屏幕截图
        screenshot = pyautogui.screenshot()
        # 将Pillow图像对象转换为OpenCV图像格式（BGR）
        open_cv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        logging.info("屏幕捕获成功")
        return open_cv_image
        
    except Exception as e:
        logging.error(f"捕获屏幕时发生错误: {str(e)}")
        return None



