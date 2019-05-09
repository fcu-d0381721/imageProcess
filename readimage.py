from os import listdir
from os.path import isfile, join
import xml.etree.cElementTree as ET
import os
import cv2
import numpy as np
import argparse
import glob


def readFolder(mypath, files):
    all_image_name = []  # 以迴圈處理
    for f in files:
      fullpath = join(mypath, f)  # 產生檔案的絕對路徑
      if isfile(fullpath):  # 判斷 fullpath 是檔案還是目錄
        all_image_name.append(f[:-4])
    return all_image_name


def getTagId(mypath):
    s = []
    tree = ET.parse(mypath)
    root = tree.getroot()
    for size in root.iter('size'):  # 讀取size下的各個元素
        width = size.find('width').text
        height = size.find('height').text
        depth = size.find('depth').text
        # print(width, height, depth)
    for ob in root.iter('object'):  # 讀取object下的各個元素
        name = ob.find('name').text
        for locate in ob.iter('bndbox'):  # 讀取bndbox下的各個元素
            xmin = locate.find('xmin').text
            ymin = locate.find('ymin').text
            xmax = locate.find('xmax').text
            ymax = locate.find('ymax').text
        s.append([xmin, ymin, xmax, ymax])
    return s


def rotate(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated


def cutImage(image_path, size, file_name):
    img = cv2.imread(image_path)
    for i in size:
        xmin = int(i[0])
        ymin = int(i[1])
        w = int(i[2]) - int(i[0])
        h = int(i[3]) - int(i[1])
        crop_img = img[ymin:ymin + h, xmin:xmin + w]
    # cv2.imshow("cropped", crop_img)
    # cv2.waitKey(0)
        cv2.imwrite('./image/' + file_name + '.jpg', crop_img)


def reshapetosmall(image_path, file_name):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    print('hello')
    cv2.imwrite('./image_small/' + file_name + '_small.jpg', img)


def reshapetobig(image_path, file_name):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (0, 0), fx=2, fy=2)  # 因為原圖已被縮小，所以要放大回來再放大兩倍，所以總共是4倍
    print('hi')
    cv2.imwrite('./image_big/' + file_name + '_big.jpg', img)


def rotation_small(image_path, file_name):
    image = cv2.imread(image_path)
    count = 24
    while count != 360:
        rotated = rotate(image, count)
        count += 24
        cv2.imwrite('./image_rotation_small/' + file_name + '_' + str(count) + '.jpg', rotated)


def rotation_big(image_path, file_name):
    image = cv2.imread(image_path)
    count = 24
    while count != 360:
        rotated = rotate(image, count)
        count += 24
        cv2.imwrite('./image_rotation_big/' + file_name + '_' + str(count) + '.jpg', rotated)


mypath = "./train_cdc/train_images"
files = listdir(mypath)
all_image_name = readFolder(mypath, files)
print(all_image_name)

for i in all_image_name:
    image = "./train_cdc/train_images/" + i + ".jpg"
    reshapetosmall(image, i)
    rotation_small(image, i)


for i in all_image_name:
    image = "./train_cdc/train_images/" + i + ".jpg"
    reshapetobig(image, i)
    rotation_big(image, i)