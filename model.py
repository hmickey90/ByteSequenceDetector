import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

mdata = pd.read_csv('/home/mickey/Documents/CSV/mal.csv', encoding = 'big5')
x =[]
label = pd.read_csv('/media/dataset/dataset.csv', encoding = 'big5', dtype={'Column2': str})
label_x=[]
label_y=[]
i=0
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
        
    elif(label['filename'][start][0]+label['filename'][start][1]!=f):
        start=0
        for infor in label['filename']:
            if(infor[0]+infor[1]!=f):
                start=start+1
            else:
                break

        while(label['filename'][start+count]!=data):
            count=count+1

    else:
        while(label['filename'][start+count]!=data):
            count=count+1
        
    if label_y != 'Unknown':
        label_y.append(label['label'][start+count])
        data = mdata['feature'][i]
        label_x.append(" ".join(data[i:i+2] for i in range(0, len(data), 2)))
    i=i+1
vectorizer = CountVectorizer(analyzer='word', ngram_range=(4, 4), lowercase=False)
X=vectorizer.fit_transform(label_x)

from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
svm_classifier = LinearSVC(C=0.2)
knn_classifier = KNeighborsClassifier(n_neighbors=3)
nb_classifier =  MultinomialNB()
mlp_classifier = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=1000)

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X,label_y,test_size = 0.2,shuffle = True)
svm_classifier.fit(x_train,y_train)
print("SVM:",accuracy_score(y_test,svm_classifier.predict(x_test)))
knn_classifier.fit(x_train,y_train)
print("KNN:",accuracy_score(y_test,knn_classifier.predict(x_test)))
nb_classifier.fit(x_train,y_train)
print("NB:",accuracy_score(y_test,nb_classifier.predict(x_test)))
mlp_classifier.fit(x_train,y_train)
print("MLP:",accuracy_score(y_test,mlp_classifier.predict(x_test)))
