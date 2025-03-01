import keyboard
import threading
import logging
import time
from config import CONFIG

class GameController:
    def __init__(self):
        self.paused = False
        self.running = True
        self.lock = threading.Lock()
        self._setup_hotkeys()
        logging.info("游戏控制器初始化完成")

    def _setup_hotkeys(self):
        """设置热键"""
        try:
            # 设置暂停/继续热键
            keyboard.add_hotkey(
                CONFIG['CONTROL']['PAUSE_KEY'], 
                self.toggle_pause,
                suppress=True
            )
            
            # 设置退出热键
            keyboard.add_hotkey(
                CONFIG['CONTROL']['EXIT_KEY'], 
                self.stop,
                suppress=True
            )
            
            logging.info(f"热键设置完成 - 暂停/继续: {CONFIG['CONTROL']['PAUSE_KEY']}, 退出: {CONFIG['CONTROL']['EXIT_KEY']}")
            
        except Exception as e:
            logging.error(f"设置热键时发生错误: {str(e)}")
            raise

    def toggle_pause(self):
        """切换暂停/继续状态"""
        with self.lock:
            self.paused = not self.paused
            status = "暂停" if self.paused else "继续"
            print(f"\n程序已{status}")
            logging.info(f"程序状态切换为: {status}")

    def stop(self):
        """停止程序"""
        with self.lock:
            self.running = False
            print("\n程序正在停止...")
            logging.info("用户触发停止命令")

    def is_paused(self):
        """检查是否处于暂停状态"""
        with self.lock:
            return self.paused

    def is_running(self):
        """检查程序是否应该继续运行"""
        with self.lock:
            return self.running

    def wait_if_paused(self):
        """如果程序暂停，等待直到继续"""
        while self.is_paused() and self.is_running():
            time.sleep(0.1)

def create_controller():
    """创建控制器实例"""
    return GameController() 