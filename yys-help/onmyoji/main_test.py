import logging
import time
from func import check, img, log, move_click, hwnd
import sys
from datetime import datetime
from config import CONFIG
import os
from func import progress
from func.control import create_controller
from func.progress import create_progress_tracker

def perform_image_recognition(image_path, value, time_data=None):
    """执行图像识别和点击操作"""
    try:
        is_recognized, width, height = img.recognize_image(image_path)
        if is_recognized:
            logging.info(f"成功识别图像: {image_path}")
            
            try:
                # 计算点击位置
                center_x = width[0] + (height[0] - width[0]) // 2
                center_y = width[1] + (height[1] - width[1]) // 2
                
                # 执行点击
                if move_click.move_click(center_x, center_y):
                    logging.info(f"成功点击位置: ({center_x}, {center_y})")
                    
                    # 处理魂土图片识别后的等待
                    if image_path == CONFIG['IMAGE_PATHS']['HUNTU']:
                        # 如果还没有记录魂土时间，说明是第一次
                        if time_data and not time_data.get('huntu_time'):
                            time_data['huntu_time'] = datetime.now()
                            logging.info(f"记录首次魂土时间: {time_data['huntu_time']}")
                            wait_time = 20  # 第一次默认等待20秒
                        else:
                            # 使用已经计算好的等待时间
                            wait_time = time_data.get('wait_time', 20)
                            logging.info(f"使用计算后的等待时间: {wait_time}秒")
                        
                        logging.info(f"识别到魂土图片，等待{wait_time}秒")
                        progress._clear_line()  # 清除当前进度显示
                        print(f"\n识别到魂土图片")
                        print(f"等待{wait_time}秒...")
                        time.sleep(wait_time)
                        progress.restore_display()  # 恢复进度显示
                    
                    # 处理奖励图片识别
                    if image_path == CONFIG['IMAGE_PATHS']['JIANGLI']:
                        # 如果有魂土时间记录但还没有计算等待时间
                        if time_data and time_data.get('huntu_time') and not time_data.get('wait_time'):
                            current_time = datetime.now()
                            time_diff = (current_time - time_data['huntu_time']).total_seconds()
                            # 限制等待时间在15-25秒之间
                            time_data['wait_time'] = max(15, min(int(time_diff), 25))
                            logging.info(f"首次时间差: {time_diff}秒")
                            logging.info(f"设置后续等待时间为: {time_data['wait_time']}秒")
                            print(f"\n根据首次时间差设置等待时间: {time_data['wait_time']}秒")
                        value -= 1
                        logging.info(f"识别到奖励，剩余次数: {value}")
                    return True, value
                else:
                    logging.error("点击操作失败")
                    return False, value
                    
            except Exception as e:
                logging.error(f"执行点击操作时发生错误: {str(e)}")
                return False, value
        else:
            logging.debug(f"未识别到图像: {image_path}")
            return False, value
            
    except Exception as e:
        logging.error(f"图像识别过程发生错误: {str(e)}")
        return False, value



#主函数
def main():
    setup_logging()
    print("\n=== 阴阳师自动化脚本启动 ===")
    print("按 F9 暂停/继续")
    print("按 ESC 退出程序")
    print("----------------------------")
    
    logging.info("程序启动")
    
    # 创建控制器
    controller = create_controller()
    
    try:
        while controller.is_running():
            # 检查是否暂停
            controller.wait_if_paused()
            
            if not check.check_game_window():
                print("\n等待游戏窗口...")
                time.sleep(5)
                continue
                
            # 获取用户输入
            attack_times_input = input("\n请输入攻打次数（默认100次，输入'restart'重启，输入's'键退出）：")
            action, value = check.process_user_input(attack_times_input)
            
            if action == 'exit':
                print("\n程序正在退出...")
                break
            elif action == 'restart':
                print("\n程序重新启动...")
                continue
            elif action == 'error':
                print("\n输入错误，请重试...")
                time.sleep(1)
                continue
                
            # 创建进度追踪器
            progress = create_progress_tracker()
            
            # 主循环
            if action == 'value' and value > 0:
                print(f"\n开始执行，计划攻打 {value} 次")
                progress.start(value)
                
                # 创建字典来存储时间数据
                time_data = {}
                
                while value > 0 and controller.is_running():
                    try:
                        controller.wait_if_paused()
                        progress.update(value)
                        
                        for image_path in CONFIG['IMAGE_PATHS'].values():
                            controller.wait_if_paused()
                            success, value = perform_image_recognition(image_path, value, time_data)
                            if not success:
                                time.sleep(CONFIG['DELAYS']['LOOP_DELAY'])
                                
                    except Exception as e:
                        logging.error(f"主循环中发生错误: {str(e)}")
                        time.sleep(1)
                        
            logging.info("当前循环完成")
            
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        logging.info("程序被用户中断")
    except Exception as e:
        print(f"\n程序发生错误: {str(e)}")
        logging.critical(f"程序发生严重错误: {str(e)}")
    finally:
        controller.stop()
        print("\n=== 程序已结束 ===")
        logging.info("程序结束")

def setup_logging():
    """设置日志系统"""
    log_config = CONFIG['LOGGING']
    if not os.path.exists(log_config['FILE_PATH']):
        os.makedirs(log_config['FILE_PATH'])
    
    log_filename = os.path.join(
        log_config['FILE_PATH'],
        datetime.now().strftime(log_config['FILE_NAME_FORMAT'])
    )
    
    # 只配置文件处理器，不配置控制台处理器
    logging.basicConfig(
        level=getattr(logging, log_config['LEVEL']),
        format=log_config['FORMAT'],
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8')
            # 移除 logging.StreamHandler(sys.stdout)
        ]
    )

if __name__ == "__main__":
    main()