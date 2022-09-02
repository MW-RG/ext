import cv2
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import messagebox
global path
path = ''
'''기능 추가'''
# 기능1 : 디렉토리 선택
def select_directory():
    try:
        foldername = askdirectory(initialdir="./")
        if foldername:
            listbox1.delete(0, "end")
            listbox1.insert(0, foldername)
        fullpath = foldername.split('/')
        global path
        path = './' + fullpath[-1] + '/'
    except:
        messagebox.showerror("Error", "오류가 발생했습니다.")

# 기능3: 프레임 추출
def run_extract():
    global path
    files = os.listdir(path)
    for f in files:
        filedir = path
        filename = f
        cap = cv2.VideoCapture(filedir + filename)

        fps = cap.get(cv2.CAP_PROP_FPS)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(fps)
        secperframe = 2

        # 프레임을 저장할 디렉토리를 생성
        try:
            if not os.path.exists(filename[:-4]):
                os.makedirs(filename[:-4])
        except OSError:
            print('Error: Creating directory. ' + filename[:-4])

        if cap.isOpened():
            current_frame = 0
            while True:
                ret, frame = cap.read()
                if current_frame % (round(fps) / secperframe) == 0:
                    name = f'./{filename[:-4]}/{filename[:-4]}_f{current_frame}.jpg'
                    print(f"Creating file… {name}")

                    if length >= current_frame:
                        cv2.imwrite(name, frame)
                    else:
                        break

                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                current_frame += 1
            cap.release()
            cv2.destroyAllWindows()

root = tk.Tk()
root.title('blackbox frame capture')
root.minsize(400, 300)  # 최소 사이즈

'''1. 프레임 생성'''
# 상단 프레임 (LabelFrame)
frm1 = tk.LabelFrame(root, text="준비", pady=15, padx=15)   # pad 내부
frm1.grid(row=0, column=0, pady=10, padx=10, sticky="nswe") # pad 내부
root.columnconfigure(0, weight=1)   # 프레임 (0,0)은 크기에 맞춰 늘어나도록
root.rowconfigure(0, weight=1)
# 하단 프레임 (Frame)
frm2 = tk.Frame(root, pady=10)
frm2.grid(row=1, column=0, pady=10)

'''2. 요소 생성'''
# 레이블
lbl1 = tk.Label(frm1, text='폴더 선택')
# 리스트박스
listbox1 = tk.Listbox(frm1, width=40, height=1)
# 버튼
btn1 = tk.Button(frm1, text="추가하기", width=8, command=select_directory)
btn0 = tk.Button(frm2, text="프레임 추출하기", width=8, command=run_extract)

'''3. 요소 배치'''
# 상단 프레임
lbl1.grid(row=0, column=0, sticky="e")
listbox1.grid(row=0, column=1, columnspan=2, sticky="we")
btn1.grid(row=0, column=3)
# 상단프레임 grid (2,1)은 창 크기에 맞춰 늘어나도록
frm1.rowconfigure(2, weight=1)
frm1.columnconfigure(1, weight=1)
# 하단 프레임
btn0.pack()

'''실행'''
root.mainloop()