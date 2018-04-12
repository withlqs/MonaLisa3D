#!/usr/bin/env python3
import cv2


def show(img):
    height, width = img.shape[:2]
    ratio = width / height

    if height > width:
        height = 960
        width = int(height * ratio)
    else:
        width = 960
        height = int(width / ratio)

    cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Preview', (width, height))
    cv2.imshow('Preview', img)
    cv2.waitKey(0)


def remove_color(img, color):
    color_num = 0
    if color == 'B':
        color_num = 0
    elif color == 'G':
        color_num = 1
    elif color == 'R':
        color_num = 2
    for x in img:
        for y in x:
            y[color_num] = 0
    return img


def output_3d(left, right):
    if left.shape[0] != right.shape[0] or left.shape[1] != left.shape[1]:
        raise Exception('Input shape size not equal, left.shape = %dx%d, right.shape = %dx%d' % (
        left.shape[0], left.shape[1], right.shape[0], right.shape[1]))
    # right_output = remove_color(right, 'R')
    # left_output = remove_color(left, 'B')
    lefts = cv2.split(left)
    rights = cv2.split(right)
    return cv2.merge([rights[0], rights[1], lefts[2]])


def reshape(img1, img2, offset1, offset2):
    h1 = img1.shape[0]
    h2 = img2.shape[0]
    w1 = img1.shape[1]
    w2 = img2.shape[1]
    if h1 != h2:
        raise Exception('Height is not equal.')

    if offset1 != 0 and offset2 != 0:
        raise Exception('Offset are all zeros.')

    if offset2 != 0:
        img1 = img1[0:h1, offset2:min(img1.shape[1], offset2 + img2.shape[1])]
        img2 = img2[0:h2, :img1.shape[1]]
    else:
        img2 = img2[0:h2, offset1:min(img2.shape[1], offset1 + img1.shape[1])]
        img1 = img1[0:h1, :img2.shape[1]]

    # ratio = w2 / h2
    # w2new = 0
    # h2new = 0
    # if h1 * w2 > h2 * w1:
    #     h2new = h1
    #     w2new = int(h2new * ratio)
    # else:
    #     w2new = w1
    #     h2new = int(w2new / ratio)
    # print('small is %dx%d' % (h1, w1))
    # print('resize to %dx%d' % (h2new, w2new))
    # img_resize = cv2.resize(img2, (w2new, h2new))
    return img1, img2


def main():
    left = cv2.imread('stylized_left.jpg', cv2.IMREAD_COLOR)
    right = cv2.imread('stylized_right.jpg', cv2.IMREAD_COLOR)
    left_new, right_new = reshape(right, left, 60, 0)
    img_3d = output_3d(left_new, right_new)
    cv2.imwrite('monalisa_3d.jpg', img_3d)
    show(img_3d)
    pass


if __name__ == '__main__':
    main()
