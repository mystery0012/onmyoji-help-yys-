import logging
import time  # 用于模拟处理时间
from func import img,move_click

img_path ='picture\\huntu.png'

# 配置日志记录器
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别，可以设置为 DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S',  # 设置日期和时间格式
    filename='log.txt',  # 设置日志文件名
    filemode='w'  # 设置文件模式，'w' 表示写模式（每次运行程序会覆盖文件），'a' 表示追加模式
)

# 配置日志记录
# 一个标志变量，用于演示在满足特定条件时添加日志（这里以识别到特定图片为例）
specific_image_recognized = False
#标志，用于程序的进行
#查找窗口‘阴阳师—网易游戏’
image_ary = [
    'picture//huntu.png',
    'picture//jiangli.png'
]
# 要管理的value值

def main():
    global  value
    while True:
        # 提示用户输入攻打次数，并提供默认值100次
        attack_times_input = input("请输入攻打次数（默认100次，输入'restart'重启，输入's'键退出）：")
        # 检查用户是否希望重启程序
        if attack_times_input.lower() == 'restart':
            print("程序将重启...")
            continue  # 重启循环，相当于“重启程序”
        if attack_times_input.lower() == 's':
            print("程序将退出...")
            break  # 退出循环，相当于“退出程序”
        try:
            attack_times = int(attack_times_input)
            value = attack_times
        except ValueError:
            attack_times = 100
            value = attack_times
            print(f"未输入有效数字，使用默认值：{attack_times}次")

        while value>0:

            print(f"攻打次数为：{value}次")
            # 模拟图片识别过程
            # 遍历图片路径列表并调用 img.recognize_image 函数
            for image_path in image_ary:
                is_recognized, width, height = img.recognize_image(image_path)
                if is_recognized:  # 只有当图片被识别时才打印宽度和高度
                    print(f"Image: {image_path}")
                    print(f"Width: {width}, Height: {height}\n")
                    center_x = width[0] + (height[0] - width[0]) // 2
                    center_y = width[1] + (height[1] - width[1]) // 2
                    move_click.move_click(center_x,center_y)
                    print('移动并双击')
                    if image_path == 'picture//jiangli.png':
                        value -= 1
                        print(f"识别领取奖励，value值减一，当前value为：{value}")
                        time.sleep(1)
                    else:
                        print(f"识别到开始，value不变，当前value为：{value}")
                    specific_image_recognized = True
                else:
                    # 可选：如果需要，可以在这里添加日志或执行其他操作
                    logging.info(f"图像 {image_path} 未被识别，将被跳过.")
                    print(f"图像 {image_path} 未被识别，将被跳过.")
                    continue  # 使用 continue 跳过当前循环迭代，继续下一个图片
                # 在循环结束后，如果识别到了特定图片，记录日志
                if specific_image_recognized:
                    logging.info("识别出特定图像.")
                else:
                    logging.info("未识别出特定图像.")
        print(f'value值为{value},请重新设置次数.')


        time.sleep(1)  # 延迟1秒


# 启动键盘监听线程

# 运行主程序
if __name__ == "__main__":
    main()
    # 如果程序因为value减到零而退出，我们可以在这里添加一些额外的逻辑，
    # 比如保存状态到一个文件，或者简单地重新调用这个脚本以模拟“重启”
    # 但由于这是一个示例，我们将省略这些步骤
    #os.execv(os.path.abspath(__file__), sys.argv)  # 重新调用当前脚本（模拟重启）