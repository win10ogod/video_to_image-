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

# video_extractor_gui_enhanced v2
允許您選擇視頻文件、輸出目錄，並通過單擊相應的按鈕執行各種操作，例如幀提取、音頻提取、視頻合成以及合併視頻和音頻。

# 依賴安裝方法:
pip install opencv-python
pip install tqdm
pip install moviepy

# 可選但有用的依賴項
您可以moviepy通過以下方式安裝所有依賴項：

pip install moviepy[optional]


# 使用方法:
python video_extractor_gui_enhanced v2.py

# video_extractor_gui_accelerated v2
video_extractor_gui_enhanced v2的增強版增加了為視頻處理任務選擇 CPU 或 GPU 加速的選項。torch.cuda.is_available()該程序使用庫中的函數檢查 GPU 是否可用torch。如果 GPU 可用，程序可以利用它進行更快的處理。可以從 GUI 的下拉菜單中選擇加速選項。

# 下載方法


# 使用方法:
使用.exe文件

# 依賴安裝方法:
pip install opencv-python
pip install tqdm
pip install moviepy
安裝 PyTorch
PyTorch的官網
https://pytorch.org/get-started/locally/
