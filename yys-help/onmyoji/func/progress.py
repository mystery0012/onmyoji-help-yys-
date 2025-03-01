import sys
import time
import logging
from datetime import datetime, timedelta

class ProgressTracker:
    BAR_CHAR_FILL = '█'
    BAR_CHAR_EMPTY = '-'
    MIN_WIDTH = 20
    MAX_WIDTH = 50
    
    def __init__(self):
        self._reset_state()
    
    def _reset_state(self):
        """重置所有状态"""
        self.start_time = None
        self.total_tasks = 0
        self.current_task = 0
        self.is_active = False
        self.last_display = ''  # 添加上一次显示的内容记录
    
    def _calculate_progress(self):
        """计算进度相关数据"""
        completed = self.total_tasks - self.current_task
        progress = (completed / self.total_tasks) * 100
        elapsed_time = datetime.now() - self.start_time
        
        # 计算剩余时间（仅在未完成时计算）
        if self.current_task == 0:  # 任务完成
            remaining_time = None
        else:
            remaining_time = (
                elapsed_time / completed * self.current_task
                if completed > 0 else timedelta(0)
            )
        
        return completed, progress, elapsed_time, remaining_time
    
    def _get_bar_width(self):
        """获取进度条宽度"""
        return min(max(self.total_tasks // 2, self.MIN_WIDTH), self.MAX_WIDTH)
    
    def _create_progress_bar(self, completed):
        """创建进度条"""
        bar_width = self._get_bar_width()
        filled = int(bar_width * completed / self.total_tasks)
        return (self.BAR_CHAR_FILL * filled + 
                self.BAR_CHAR_EMPTY * (bar_width - filled))
    
    def _format_time(self, time_delta):
        """格式化时间显示"""
        return str(time_delta).split('.')[0]
    
    def _clear_line(self):
        """清除当前行"""
        print('\r' + ' ' * 100 + '\r', end='')
    
    def start(self, total):
        """开始追踪进度"""
        if total <= 0:
            return
        
        self._reset_state()
        self.start_time = datetime.now()
        self.total_tasks = total
        self.current_task = total
        self.is_active = True
        logging.info(f"开始任务追踪，总任务数: {total}")
    
    def update(self, current):
        """更新当前进度"""
        if not self.is_active:
            return
            
        self.current_task = current
        self._display_progress()
        
        if self.current_task == 0:
            self.is_active = False
            logging.info("任务完成")
    
    def restore_display(self):
        """恢复上一次的进度显示"""
        if self.last_display:
            self._clear_line()
            print(self.last_display, end='', flush=True)
    
    def _display_progress(self):
        """显示进度信息"""
        try:
            if not self.is_active or self.total_tasks <= 0:
                return
            
            completed, progress, elapsed_time, remaining_time = self._calculate_progress()
            progress_bar = self._create_progress_bar(completed)
            
            # 构建基础进度信息
            progress_info = [
                f'\r进度: [{progress_bar}] {progress:.1f}% ',
                f'[{completed}/{self.total_tasks}] ',
                f'已用时间: {self._format_time(elapsed_time)}'
            ]
            
            # 根据是否完成添加不同的时间信息
            if remaining_time is not None:
                progress_info.append(f'预计剩余: {self._format_time(remaining_time)}')
            else:
                progress_info.append(f'总用时: {self._format_time(elapsed_time)}')
            
            # 保存当前显示内容
            self.last_display = ''.join(progress_info)
            
            # 显示进度信息
            self._clear_line()
            print(self.last_display, end='' if remaining_time is not None else '\n', flush=True)
                
        except Exception as e:
            logging.error(f"显示进度时发生错误: {str(e)}")
            self.is_active = False

def create_progress_tracker():
    """创建进度追踪器实例"""
    return ProgressTracker() 