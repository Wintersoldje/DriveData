from grabscreen import grab_screen
from getkeys import key_check
import os
import time
import cv2
from _datetime import datetime
import sys
import pygame

'''
데이터 수집 모듈
- 영상
- 주행데이터(휠 각도, 엑셀 페달, 브레이크 페달

** 수집 후 data_run_v6_view.py로 보면서 직접 주행상황 태깅할 것!
'''

## 기본설정
# 저장 폴더명 설정
save_folder_name = '20_07_20-2'
download_path = os.getcwd() + '\\download\\' + save_folder_name
# print(download_path)
if not os.path.isdir(download_path):
    print("@ make download directory")
    os.mkdir(download_path)

# 조이스틱 설정
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
joy_name = joystick.get_name()
print("joystick name : {0}, num of axis : {1}".format(joy_name, joystick.get_numaxes()))

# 윈도우 설정
screen_width = 1920
screen_height = 1080
resize_width = 960
resize_height = 540

# 조이스틱 output 형식으로 변환
def joystick_to_output():
    '''

    Convert joystick data to array
    [wheel angle, accelerator, brake]

    :param joystick:
    :return output:
    '''

    pygame.event.pump()

    # raw value
    angle = joystick.get_axis(0)
    accelerator = joystick.get_axis(2)
    brake = joystick.get_axis(3)
    # clutch = joystick.get_axis(1)

    # fix value
    # angle = round(joystick.get_axis(0) * 100, 3)
    # accelerator = round((1 - joystick.get_axis(2)) * 50, 3)
    # brake = round((1 - joystick.get_axis(3)) * 50, 3)
    # clutch = round((1 - joystick.get_axis(1)) * 50, 3)

    output = [0,0,0]

    output[0] = angle
    output[1] = accelerator
    output[2] = brake

    return output

#  데이터수집(영상, 조이스틱입력)
def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False
    while (True):
        if not paused:
            prev_time = time.time()

            # screen_width X screen_height windowed mode
            screen = grab_screen(region=(0, 0, screen_width-1, screen_height-1))
            # screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            # screen = cv2.resize(screen, (resize_width, resize_height))

            # resize to something a bit more acceptable for a CNN
            output = joystick_to_output()

            save_time = '\\{:%H_%M_%S_%f}'.format(datetime.now())
            save_img_path = download_path + save_time + ".jpg"
            save_joystick_path = download_path + save_time + ".txt"
            cv2.imwrite(save_img_path, screen)
            f = open(save_joystick_path, 'w')
            f.write(str(output))
            f.close()

            print(save_time)
            print(output)

            # print(training_data)

            # 시간확인
            cur_time = time.time()
            sec = cur_time - prev_time
            prev_time = cur_time
            fps = 1 / (sec)
            # print("Time {0}".format(sec))
            print("Time {0} , Estimated fps {1}".format(sec, fps))

        # 일시정지 및 정지
        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
        elif 'K' in keys:
            sys.exit()

main()






