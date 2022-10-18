# -*- coding: utf-8 -*-
"""SVM_BIOS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ub2xMlNhr1kJtorlBK2qZb9-0mkb7vLK
"""

from google.colab import drive
drive.mount('/content/drive')

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage.io import imread
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn import svm
from sklearn.metrics import accuracy_score,confusion_matrix
import pickle
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

target = []
dataset = []
flat_data = []

DATADIR = '/content/drive/MyDrive/Office/Dataset/'
Categorys = ['blank', 'boot', 'dell', 'hp', 'human', 'lenovo']
IMG_SIZE=512

for category in Categorys:
    class_num = Categorys.index(category)    # Label Encoding the values
    path = os.path.join(DATADIR,category)   # Create a path to use all images
    for img in os.listdir(path):
        img_array = imread(os.path.join(path,img))
        img_resized = resize(img_array,(256,256,3)) # Normalizes the values from 0 to 1
        flat_data.append(img_resized.flatten())
        dataset.append(img_resized)
        target.append(class_num)
        # print(img_array.shape)
        # plt.imshow(img_array)
        # break

flat_data = np.array(flat_data)
target = np.array(target)
dataset = np.array(dataset)

unique,count = np.unique(target,return_counts=True)
plt.bar(Categorys,count)
plt.show()

x_train, x_test,y_train, y_test = train_test_split(flat_data,target,test_size = 0.1,random_state = 109)

param_grid = [
              {'C':[1,100,1000],'kernel':['linear']},
              {'C':[1,10,1000],'gamma':[0.001,0.0001],'kernel':['rbf']},
]

svc = svm.SVC(probability=True)
clf = GridSearchCV(svc,param_grid)
clf.fit(x_train,y_train)

pickle.dump(clf,open('/content/drive/MyDrive/Office/screen_detect_model.p','wb'))
# model = pickle.load(open('splash_detect_model.p','rb'))


y_pred = clf.predict(x_test)
print(y_pred)
print(confusion_matrix(y_pred, y_test))

print(accuracy_score(y_pred,y_test))

model = pickle.load(open('/content/drive/MyDrive/Office/screen_detect_model.p','rb'))

print(accuracy_score(y_pred,y_test))

pickle.dump(clf,open('/content/drive/MyDrive/Office/screen_detect_model.p','wb'))

model = pickle.load(open('/content/drive/MyDrive/Office/screen_detect_model.p','rb'))

flat_data = []
img = imread('/content/drive/MyDrive/Office/Dataset/dell/Copy of 4705.Dell_logo.jpg')
img_resized = resize(img,(256,256,3))
flat_data.append(img_resized.flatten())
flat_data = np.array(flat_data)
y_out = model.predict(flat_data)
y_out = Categorys[y_out[0]]
plt.imshow(img_resized)
plt.show()
print(f'Predicted output : {y_out}')

train_pred = model.predict(x_train)

print(accuracy_score(train_pred,y_train))

flat_data = np.array(flat_data)
target = np.array(target)
dataset = np.array(dataset)
x_train, x_test,y_train, y_test = train_test_split(flat_data,target,train_size = 0.01,random_state = 109)

train_pred = model.predict(x_train)

print(accuracy_score(train_pred,y_train))

flat_data = []
img = imread('/content/drive/MyDrive/Office/test/dell_legacy-O7010-0010-after-press - Copy.jpg')
img_resized = resize(img,(256,256,3))
flat_data.append(img_resized.flatten())
flat_data = np.array(flat_data)
y_out = model.predict(flat_data)
y_out = Categorys[y_out[0]]
plt.imshow(img_resized)
plt.show()
print(f'Predicted output : {y_out}')