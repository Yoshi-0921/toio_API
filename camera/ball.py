from io import BytesIO
import cv2

import IPython
from PIL import Image
import numpy as np
import cv2


def show(a, fmt='jpeg'):
    f = BytesIO()
    Image.fromarray(a).save(f, fmt)
    IPython.display.display(IPython.display.Image(data=f.getvalue()))


def getMask(frame, lower, upper):
    # HSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array(lower)
    upper = np.array(upper)
    if lower[0] >= 0:
        # 色相が正の値のとき、赤以外のマスク
        mask = cv2.inRange(hsv, lower, upper)
    else:
        # 色相が負の値のとき、赤用マスク
        h = hsv[:, :, 0]
        s = hsv[:, :, 1]
        v = hsv[:, :, 2]
        mask = np.zeros(h.shape, dtype=np.uint8)
        mask[((h < lower[0] * -1) | h > upper[0]) & (s > lower[1]) & (s < upper[1]) & (v > lower[2]) & (v < upper[2])] = 255

    return cv2.bitwise_and(frame, frame, mask=mask)


# 輪郭取得
def getContours(img, t, r):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 一番大きい輪郭を抽出
    contours.sort(key=cv2.contourArea, reverse=True)

    # 一つ以上検出
    if len(contours) > 0:
        for cnt in contours:
            # 最小外接円を描く
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius)

            if radius > r or len(contours) == 1:
                return center
    return


def get_ball_center(capture, **kwargs):
    ret, frame = capture.read()
    if ret:
        res_blue = getMask(frame, [100, 45, 50], [150, 255, 255])
        center = getContours(res_blue, 50, 50)
        kwargs['ball_center'] = center
    return kwargs


def convert_ball_position(board_x1, board_y1, board_x2, board_y2, camera_x1, camera_y1, camera_x2, camera_y2, **kwargs):
    try:
        center = kwargs['ball_center']
        x = (center[0] - camera_x1) * (board_x2 - board_x1) / (camera_x2 - camera_x1) + board_x1
        y = (center[1] - camera_y1) * (board_y2 - board_y1) / (camera_y2 - camera_y1) + board_y1
        kwargs['ball_center'] = (int(x), int(y))

    except TypeError:
        kwargs['ball_center'] = None

    return kwargs


if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    while 1:
        response = get_ball_center(cap, **{})
        print(response)
