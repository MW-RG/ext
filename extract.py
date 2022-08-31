import cv2
import os

print(cv2.__version__)

filedir = './blackbox/'
filename = '00001_갈림길야간맑음11111.avi'
cap = cv2.VideoCapture(filedir + filename)

fps = cap.get(cv2.CAP_PROP_FPS)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(fps)
secperframe = 3

#프레임을 저장할 디렉토리를 생성
try:
    if not os.path.exists(filename[:-4]):
        os.makedirs(filename[:-4])
except OSError:
    print ('Error: Creating directory. ' + filename[:-4])

if cap.isOpened():
    current_frame = 0
    while True:
        ret, frame = cap.read()
        if current_frame % (round(fps) / secperframe) == 0:
            name = f'./{filename[:-4]}/frame{current_frame}.jpg'
            print(f"Creating file… {name}")

            if length >= current_frame :
                cv2.imwrite(name, frame)
            else:
                break

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        current_frame += 1
    cap.release()
    cv2.destroyAllWindows()