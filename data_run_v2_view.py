from getkeys import key_check
import os
import time
import cv2
import sys

'''
기본적으로 시작 시 일반 주행상황으로 태깅이 되고 
각 주행상황에 해당하는 키를 입력 시 그것으로 태깅이 지속되니 참고할 것

[키입력] : 동작

** 태깅 할 주행상황(situation) 정리

[1] : 일반주행(normal)
[2] : 감속(deceleration)
[3] : 좌측추월(left_passing)
[4] : 우측추월(right_passing)

** 사용 관련 키 조작

[S] : 시작 
[T] : 일시정지 / 다시시작
[K] : 종료
[E] : 앞으로 한 프레임 이동
[R] : 뒤로 한 프레임 이동

'''

# 카메라 모드 설정(1 or 4)
camera_mode = 1

## 기본설정
# 불러올 폴더명 설정
load_folder_name = '19_12_04-9-2-under_1'
download_path = os.getcwd() + '\\download\\' + load_folder_name

output_txt_folder_path = download_path + "\\output_txt"
if not os.path.isdir(output_txt_folder_path):
    print("@ make output_txt_folder_path directory")
    os.mkdir(output_txt_folder_path)

output_img_folder_path = download_path + "\\output_img"
if not os.path.isdir(output_img_folder_path):
    print("@ make output_img_folder_path directory")
    os.mkdir(output_img_folder_path)

output_front_img_folder_path = output_img_folder_path + '\\front'
if not os.path.isdir(output_front_img_folder_path):
    print("@ make output_front_img_folder_path directory")
    os.mkdir(output_front_img_folder_path)

output_left_img_folder_path = output_img_folder_path + '\\left'
if not os.path.isdir(output_left_img_folder_path):
    print("@ make output_left_img_folder_path directory")
    os.mkdir(output_left_img_folder_path)

output_right_img_folder_path = output_img_folder_path + '\\right'
if not os.path.isdir(output_right_img_folder_path):
    print("@ make output_right_img_folder_path directory")
    os.mkdir(output_right_img_folder_path)

# opencv text 설정
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
location1 = (20, 50)
location2 = (20, 100)
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)
white = (255, 255, 255)
yellow = (0, 255, 255)
cyan = (255, 255, 0)
magenta = (255, 0, 255)

# 이미지 전처리 함수(이미지 잘라냄)
def image_crop(img, image_name):

    # path 설정
    front_img_path = output_front_img_folder_path + "\\" + image_name
    left_img_path = output_left_img_folder_path + "\\" + image_name
    right_img_path = output_right_img_folder_path + "\\" + image_name

    crop_img = img.copy()

    # 잘라낼 영역 [높이(행), 너비(열)]

    # 카메라 모드 1
    if camera_mode == 1:
        # 사이드 미러 크기 260 X 360
        left_img = crop_img[95:450, 25:285]
        cv2.imwrite(left_img_path, left_img)
        right_img = crop_img[95:450, 1635:1895]
        cv2.imwrite(right_img_path, right_img)

        # 프런트 이미지 크기 760 X 425
        front_img = crop_img[155:580, 640:1400]
        cv2.imwrite(front_img_path, front_img)

    # 카메라 모드 4
    else:
        # 사이드 미러 크기 260 X 360
        left_img = crop_img[95:450, 25:285]
        cv2.imwrite(left_img_path, left_img)
        right_img = crop_img[95:450, 1635:1895]
        cv2.imwrite(right_img_path, right_img)

        # 프런트 이미지 크기 760 X 425
        front_img = crop_img[450:700, :]
        cv2.imwrite(front_img_path, front_img)


# 수집한 데이터 확인 및 주행상황 태깅
def view():
    # 디렉토리에서 파일 가져와서 세팅
    file_list = os.listdir(download_path)
    file_list.sort()

    img_list = []
    txt_list = []
    for item in file_list:
        if item.find('.jpg') is not -1:
            img_list.append(item)
        elif item.find('.txt') is not -1:
            if item.find('_s') is not -1:
                continue
            else:
                txt_list.append(item)

    # print(img_list)
    # print(txt_list)

    idx = 0
    start = False
    paused = False
    moving = False
    driving_situation = 1
    while (True):
        # 키확인
        keys = key_check()

        if not start:
            print('시작하려면 S 키를 누르세요!')
            if 'S' in keys:
                start = True
                print('작업이 시작됩니다!')
                time.sleep(1)
                continue
        else:
            if 'T' in keys:
                if paused:
                    paused = False
                    print('Unpaused!')
                    time.sleep(1)
                else:
                    print('Pausing!')
                    paused = True
                    time.sleep(1)
            elif 'K' in keys:
                print('User Kill System!')
                cv2.destroyAllWindows()
                time.sleep(1)
                sys.exit()
            elif 'S' in keys:
                paused = False
                print('Start!')
                time.sleep(1)
            elif 'E' in keys:
                print('프레임 앞으로 이동')
                moving = True
                idx -= 1
                if idx < 0:
                    print('시작 프레임 입니다!')
                    idx = 0
                print("--- 키 입력 대기중 --- ")
            elif 'R' in keys:
                print('프레임 뒤로 이동')
                moving = True
                idx += 1
                # 모든 데이터 확인 시 종료
                if idx == img_list.__len__():
                    print("마지막 프레임 입니다!")
                    idx -= 1
                print("--- 키 입력 대기중 --- ")
            elif '1' in keys:
                print("주행상황 변경 : 일반주행")
                driving_situation = 1
                time.sleep(3)
                print("--- 키 입력 대기중 --- ")
            elif '2' in keys:
                print("주행상황 변경 : 감속")
                driving_situation = 2
                time.sleep(3)
                print("--- 키 입력 대기중 --- ")
            elif '3' in keys:
                print("주행상황 변경 : 좌측추월")
                driving_situation = 3
                time.sleep(3)
                print("--- 키 입력 대기중 --- ")
            elif '4' in keys:
                print("주행상황 변경 : 우측추월")
                driving_situation = 4
                time.sleep(3)
                print("--- 키 입력 대기중 --- ")


            # 진행!
            if not paused:
                # 모든 데이터 확인 시 종료
                if idx == img_list.__len__():
                    print("End!")
                    time.sleep(1)
                    sys.exit()

                # path 설정
                img_path = download_path + '\\' + str(img_list[idx])
                input_txt_path = download_path + "\\" + str(txt_list[idx])
                output_txt_path = output_txt_folder_path + '\\' + str(txt_list[idx])
                # print(output_txt_path)

                ## 주행상황
                # 값 확인 및 상황 태깅
                output_data = ''
                # 주행상황 태깅된 데이터 생성
                if not os.path.exists(output_txt_path):
                    with open(input_txt_path, 'r') as f:
                        while (True):
                            line = f.readline()
                            if not line:
                                break
                            # 문자열 파싱 후 드라이빙 데이터와 상황 태깅
                            line = line.split('[')[1].split(']')[0].split(', ')
                            for l in line:
                                output_data += str(l) + " "
                            output_data += str(driving_situation)
                            print(output_data)

                    with open(output_txt_path, 'w') as f:
                        f.write(output_data)
                # 주행상황 수정
                else:
                    with open(output_txt_path, 'r') as f:
                        while(True):
                            line = f.readline()
                            if not line:
                                break
                            print("pre  : " + str(line))
                            # 문자열 파싱 후 드라이빙 데이터와 상황 태깅(주행상황 뺴고 세 값 가져오기)
                            line = line.split(' ')
                            for jdx in range(3):
                                output_data += str(line[jdx]) + " "
                            output_data += str(driving_situation)
                            print("post : " + str(output_data))

                    with open(output_txt_path, 'w') as f:
                        f.write(output_data)


                ## 이미지 처리
                # 이미지
                img = cv2.imread(img_path)
                image_crop(img, str(img_list[idx]))
                cv2.putText(img, 'File name : {0}'.format(str(img_list[idx])), location1, font, fontScale, red)
                cv2.putText(img, 'Situation : {0}'.format(str(driving_situation)), location2, font, fontScale, red)
                cv2.imshow('view', img)

                if cv2.waitKey(25) & 0xFF == ord('k'):
                    cv2.destroyAllWindows()
                    break

                idx += 1
            else:
                # 프레임 이동
                if moving:
                    # path 설정
                    img_path = download_path + '\\' + str(img_list[idx])
                    input_txt_path = download_path + "\\" + str(txt_list[idx])
                    output_txt_path = output_txt_folder_path + '\\' + str(txt_list[idx])
                    # print(output_txt_path)

                    ## 주행상황
                    # 값 확인 및 상황 태깅
                    output_data = ''
                    # 주행상황 태깅된 데이터 생성
                    if not os.path.exists(output_txt_path):
                        with open(input_txt_path, 'r') as f:
                            while (True):
                                line = f.readline()
                                if not line:
                                    break
                                # 문자열 파싱 후 드라이빙 데이터와 상황 태깅
                                line = line.split('[')[1].split(']')[0].split(', ')
                                for l in line:
                                    output_data += str(l) + " "
                                output_data += str(driving_situation)
                                print(output_data)

                        with open(output_txt_path, 'w') as f:
                            f.write(output_data)
                    # 주행상황 수정
                    else:
                        with open(output_txt_path, 'r') as f:
                            while (True):
                                line = f.readline()
                                if not line:
                                    break
                                print("pre  : " + str(line))
                                # 문자열 파싱 후 드라이빙 데이터와 상황 태깅(주행상황 뺴고 세 값 가져오기)
                                line = line.split(' ')
                                for jdx in range(3):
                                    output_data += str(line[jdx]) + " "
                                output_data += str(driving_situation)
                                print("post : " + str(output_data))

                        with open(output_txt_path, 'w') as f:
                            f.write(output_data)

                    ## 이미지처리
                    # 이미지 불러와서 확인
                    img = cv2.imread(img_path)
                    image_crop(img, str(img_list[idx]))
                    cv2.putText(img, 'File name : {0}'.format(str(img_list[idx])), location1, font, fontScale, red)
                    cv2.putText(img, 'Situation : {0}'.format(str(driving_situation)), location2, font, fontScale, red)
                    cv2.imshow('view', img)

                    if cv2.waitKey(25) & 0xFF == ord('k'):
                        cv2.destroyAllWindows()
                        break

                    moving = False

# 학습데이터(상황 태깅한 데이터와 전처리 된 이미지) 확인
def check_view_trainig():

    print('카메라모드와 폴더명을 확인하세요!')
    print('current camera mod : {0}'.format(camera_mode))
    print("5초뒤 시작")
    time.sleep(5)

    # 디렉토리에서 파일 가져와서 세팅
    front_img_dir = download_path + '\\output_img\\front'
    left_img_dir = download_path + '\\output_img\\left'
    right_img_dir = download_path + '\\output_img\\right'
    txt_dir = download_path + '\\output_txt'
    front_img_list = os.listdir(front_img_dir)
    left_img_list = os.listdir(left_img_dir)
    right_img_list = os.listdir(right_img_dir)
    txt_list = os.listdir(txt_dir)

    # print(front_img_list)
    # print(left_img_list)
    # print(right_img_list)
    # print(txt_list)
    # print(front_img_list.__len__())
    # print(left_img_list.__len__())
    # print(right_img_list.__len__())
    # print(txt_list.__len__())

    # if not txt_list.__len__() == front_img_list.__len__():
    #     print("파일 갯수 불일치!")
    #     sys.exit()

    for idx in range(0, txt_list.__len__()):
        front_img_path = front_img_dir + '\\{0}'.format(front_img_list[idx])
        left_img_path = left_img_dir + '\\{0}'.format(left_img_list[idx])
        right_img_path = right_img_dir + '\\{0}'.format(right_img_list[idx])
        txt_path = txt_dir + '\\{0}'.format(txt_list[idx])

        front_img = cv2.imread(front_img_path)
        left_img = cv2.imread(left_img_path)
        right_img = cv2.imread(right_img_path)

        driving_situation = 0
        with open(txt_path, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                print(line)
                line = line.split(' ')
                driving_situation = line[3]

        cv2.putText(front_img, 'File name : {0}'.format(str(front_img_list[idx])), location1, font, fontScale, red)
        cv2.putText(front_img, 'Situation : {0}'.format(str(driving_situation)), location2, font, fontScale, red)

        cv2.imshow('front', front_img)
        cv2.imshow('left', left_img)
        cv2.imshow('right', right_img)

        if camera_mode == 1:
            cv2.moveWindow('front', 270, 0)
            cv2.moveWindow('left', 0, 0)
            cv2.moveWindow('right', 1040, 0)
        else:
            cv2.moveWindow('front', 0, 360)
            cv2.moveWindow('left', 0, 0)
            cv2.moveWindow('right', 1650, 0)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

# 원본데이터 확인
def check_view_original():
    # 디렉토리에서 파일 가져와서 세팅
    file_list = os.listdir(download_path)
    file_list.sort()

    img_list = []
    txt_list = []
    for item in file_list:
        if item.find('.jpg') is not -1:
            img_list.append(item)
        elif item.find('.txt') is not -1:
            txt_list.append(item)

    # print(img_list)
    # print(txt_list)
    # print(img_list.__len__())
    # print(txt_list.__len__())
    # time.sleep(30)

    for idx in range(0, img_list.__len__()):
        img_path = download_path + '\\' + str(img_list[idx])
        txt_path = download_path + "\\" + str(txt_list[idx])
        # print(img_path)
        # print(txt_path)
        img = cv2.imread(img_path)
        cv2.putText(img, 'File name : {0}'.format(str(img_list[idx])), location1, font, fontScale, red)
        cv2.imshow('view', img)
        cv2.moveWindow('view',0,0)

        with open(txt_path, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                print(line)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break




# view()
check_view_original()
# check_view_trainig()