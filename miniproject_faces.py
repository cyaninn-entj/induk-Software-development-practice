# -*- coding: utf-8 -*-
"""miniproject-faces.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F5z0QqZQcQZXqMZJCJcIvNULm77JRdVK
"""

# 202216709 성연우
# 미니프로젝트 B1 - 얼굴찾기:SVM 으로 분류하기

# 1. 데이터 확인
# https://github.com/dknife/ML/raw/main/data/Proj2/ 에서 사진을 확인하기

# 2. 미리 준비할 것
# 기울기 , 히스토그램을 구하는 hog() 함수 사용

import matplotlib.pyplot as plt
import numpy as np

from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog

# 3. 얼굴 이미지 읽고 확인해보기
# SVM 을 이용하여 사람 얼굴 이미지를 다른 이미지와 구분하는 것이 이 프로젝트의 목표
# 사람 이미지를 positive 그룹, 다른 이미지는 negative 그룹으로 나눠 모델에 제공할 예정

url = 'https://github.com/dknife/ML/raw/main/data/Proj2/faces/'

face_images = []

for i in range(15):
    file = url + 'img{0:02d}.jpg'.format(i+1)
    img = imread(file)
    img = resize(img, (64,64))
    face_images.append(img)


def plot_images(nRow, nCol, img):
    fig = plt.figure()
    fig, ax = plt.subplots(nRow, nCol, figsize = (nCol,nRow))
    for i in range(nRow):
        for j in range(nCol):
            if nRow <= 1: axis = ax[j]
            else:         axis = ax[i, j]
            axis.get_xaxis().set_visible(False)
            axis.get_yaxis().set_visible(False)
            axis.imshow(img[i*nCol+j])


plot_images(3,5, face_images)

# 4. 얼굴 이미지의 특징 데이터 구하기
# 얼굴 이미지의 중요한 특징만 추출할 때 사용할 수 있는 대표적인 방법인 이미지의 기울기 히스토그램을 사용하는 것
# 이미지를 2차원 공간을 domain 으로 하고, 픽셀값을 range 로 하는 함수로 본다면 각 픽셀 위치에서 기울기를 계산할 수 있다
# 이 기울기를 8개 방향으로 구분하여 각 방향별 빈도를 계산하면 기울기의 히스토그램을 구할 수 있다.
# 사이킷 이미지는 이 기울기 히스토그램을 사이킷 이미지의 feature 서브 모듈에 있는 hog() 함수로 쉽게 구할 수 있게 해줌

face_hogs = []
face_features = []

for i in range(15):
    hog_desc, hog_image = hog(face_images[i], orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualize=True, multichannel=True)
    face_hogs.append(hog_image)
    face_features.append(hog_desc)

plot_images(3, 5, face_hogs)

print(face_features[0].shape)

fig = plt.figure()
fig, ax = plt.subplots(3,5, figsize = (10,6))
for i in range(3):
    for j in range(5):
        ax[i, j].imshow(resize(face_features[i*5+j], (128,16)))

# 5. 사람 얼굴이 아닌 이미지의 특징 벡터 준비
# 사람 얼굴을 준비하는 방법과 동일하게 부 그룹의 데이터가 될 이미지들을 준비함

url = 'https://github.com/dknife/ML/raw/main/data/Proj2/animals/'

animal_images = []

for i in range(15):
    file = url + 'img{0:02d}.jpg'.format(i+1)
    img = imread(file)
    img = resize(img, (64,64))
    animal_images.append(img)

plot_images(3, 5, animal_images)

animal_hogs = []
animal_features = []

for i in range(15):
    hog_desc, hog_image = hog(animal_images[i], orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualize=True, multichannel=True)
    animal_hogs.append(hog_image)
    animal_features.append(hog_desc)

plot_images(3, 5, animal_hogs)

fig = plt.figure()
fig, ax = plt.subplots(3,5, figsize = (10,6))
for i in range(3):
 for j in range(5):
   ax[i, j].imshow(resize(animal_features[i*5+j], (128,16)))

# 6. 학습을 위한 데이터 만들어 학습하기
# 학습된 모델로 훈련 데이터에 대한 예측을 수행

X, y = [], []

for feature in face_features:
    X.append(feature)
    y.append(1)
for feature in animal_features:
    X.append(feature)
    y.append(0)

fig = plt.figure()
fig, ax = plt.subplots(6,5, figsize = (10,6))
for i in range(6):
 for j in range(5):
   ax[i, j].imshow(resize(X[i*5+j], (128,16)),interpolation='nearest')
print(y)

from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

polynomial_svm_clf = Pipeline([
    ("scaler", StandardScaler()),
    ("svm_clf", SVC(C=1, kernel = 'poly', degree=5, coef0=10.0))
 ])
polynomial_svm_clf.fit(X, y)

yhat = polynomial_svm_clf.predict(X)
print(yhat)

# 7. 새로운 데이터에 적용해 보기
# ********************** 여기에 제 사진 한장과 제가 좋아하는 연애인의 사진을 넣어봤습니다 **********************
# url 링크는 제 깃허브의 디렉토리 링크입니다.

url = 'https://github.com/cyaninn-entj/induk-Software-development-practice/raw/main/test_data/'
#url='https://github.com/dknife/ML/raw/main/data/Proj2/test_data/'
#url='https://github.com/dknife/ML/raw/main/data/Proj2/faces/'

test_images = []

for i in range(10):
    file = url + 'img{0:02d}.jpg'.format(i+1)
    img = imread(file)
    img = resize(img, (64,64))
    test_images.append(img)

plot_images(2, 5, test_images)

test_hogs = []
test_features = []
for i in range(10):
    hog_desc, hog_image = hog(test_images[i], orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualize=True, multichannel=True)
    test_hogs.append(hog_image)
    test_features.append(hog_desc)

plot_images(2, 5, test_hogs)

fig = plt.figure()
fig, ax = plt.subplots(2,5, figsize = (10,4))
for i in range(2):
 for j in range(5):
   ax[i, j].imshow(resize(test_features[i*5+j], (128,16)), interpolation='nearest')

test_result = polynomial_svm_clf.predict(test_features)
print(test_result)

fig = plt.figure()
fig, ax = plt.subplots(2,5, figsize = (10,4))
for i in range(2):
    for j in range(5):
        ax[i, j].get_xaxis().set_visible(False)
        ax[i, j].get_yaxis().set_visible(False)
        if test_result[i*5+j] == 1:
            ax[i, j].imshow(test_images[i*5+j],interpolation='nearest')