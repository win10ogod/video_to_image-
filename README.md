# video_to_image-
使用 OpenCV 庫從視頻中提取幀，並提供帶有進度條的友好命令行界面

# 依賴安裝方法:
pip install opencv-python
pip install tqdm

# 使用方法:
python video_to_image.py /path/to/video_file.mp4 /path/to/output_directory
替換/path/to/video_file.mp4為視頻文件的絕對路徑，以及/path/to/output_directory要保存提取的幀的目錄的絕對路徑。

# video_extractor_gui
包含圖形用戶界面+時間段指定

# 使用方法:
python video_extractor_gui.py


# video_extractor_gui_accelerated
在此版本中，進行了以下增強：

添加了使用下拉菜單在 GPU 和 CPU 加速之間進行選擇的選項。
新增視頻文件丟失、視頻文件打開失敗、開始時間超過視頻時長等情況的錯誤處理。
如果選擇了 GPU 加速但沒有可用的 GPU 設備，則顯示警告消息。
當選擇 CPU 加速時，添加了一個預覽窗口以在提取過程中實時顯示幀。
添加了一個完成消息框以顯示提取的幀總數。

# 注意：GPU 加速需要支持 CUDA 的 GPU 和安裝必要的庫。

# 使用方法:
python video_extractor_gui_accelerated.py

