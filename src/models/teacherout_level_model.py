# src/models/teacherout_level_model.py

class TeacheroutModel:
    def __init__(self):
        self.clicks = 0  # 記錄飯糰點擊次數
        self.success_clicks = 15  # 完成任務需要的點擊次數

    def increase_clicks(self):
        """
        每次點擊飯糰時增加點擊次數
        """
        self.clicks += 1
        print(f"當前飯糰點擊次數: {self.clicks}")

    def check_game_status(self):
        """
        檢查是否完成任務（點擊幾次飯糰）
        """
        return self.clicks >= self.success_clicks
   
    
