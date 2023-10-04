import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

mdata = pd.read_csv('/home/mickey/Documents/CSV/mal.csv', encoding = 'big5')
x =[]
label = pd.read_csv('/media/dataset/dataset.csv', encoding = 'big5', dtype={'Column2': str})
label_x=[]
label_y=[]
for data in mdata['feature']:
    label_x.append(" ".join(data[i:i+2] for i in range(0, len(data), 2)))

vectorizer = CountVectorizer(analyzer='word', ngram_range=(4, 4), lowercase=False)
X=vectorizer.fit_transform(label_x)
start=0
for data in mdata['file']:
    count=0
    f=data[0]+data[1]
    if(start==-1):
        for infor in label['filename']:
            if(infor[0]+infor[1]!=f):
                start=start+1
            else:
                break

        while(label['filename'][start+count]!=data):
            count=count+1
        label_y.append(label['label'][start+count])
    elif(label['filename'][start][0]+label['filename'][start][1]!=f):
        start=0
        for infor in label['filename']:
            if(infor[0]+infor[1]!=f):
                start=start+1
            else:
                break

        while(label['filename'][start+count]!=data):
            count=count+1
        label_y.append(label['label'][start+count])
    else:
        while(label['filename'][start+count]!=data):
            count=count+1
        label_y.append(label['label'][start+count])

from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.svm import LinearSVR
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score
svm_classifier1 = SVC(C=0.2)
svm_classifier2 = LinearSVC(C=0.2)

svm_classifier4 = SGDClassifier(loss='hinge', alpha=1/0.2)

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X,label_y,test_size = 0.2,shuffle = True)
svm_classifier1.fit(x_train,y_train)
print("SVM1:",accuracy_score(y_test,svm_classifier1.predict(x_test)))
svm_classifier2.fit(x_train,y_train)
print("SVM2:",accuracy_score(y_test,svm_classifier2.predict(x_test))) #95.63
svm_classifier4.fit(x_train,y_train)
print("SVM4:",accuracy_score(y_test,svm_classifier4.predict(x_test))) #74.86
