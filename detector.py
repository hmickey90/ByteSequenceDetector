from malwareDetector.detector import detector
from typing import Any
import numpy as np
import sys
import pandas as pd
import os
import r2pipe
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score


def read_magic_number(file_path, num_bytes):
    with open(file_path, 'rb') as file:
        file_size = os.path.getsize(file_path)  # Get the size of the file
        if file_size >= num_bytes:
            magic_bytes = file.read(num_bytes)
        else:
            magic_bytes = b''  # Empty bytes if the file is too small
    return magic_bytes

class subDetector(detector):
    def __init__(self)-> None:
        pass
    def extractFeature(self,data_path:str)-> None:
        datalist=[]
        for file in os.listdir(data_path):         
            filepath=data_path+'/'+file  
        
            r2 = r2pipe.open(filepath)
            r2.cmd('aaa')
            r2.cmd(f's {"main"}')
            code = r2.cmd('pd')
            r2.quit()
            feature = ""
            i = 0
            
            l=len(code.split('\n'))
            for i in range(l):
                temp = [_str for _str in code.split('\n')[i].split(' ') if _str != '']
                for j in range(len(temp)):
                    try:
                        if temp[j][0:2]=="0x" and all(temp[j+1][k].isdigit() or temp[j+1][k] in 'abcdef' for k in range(8)):
                            feature+=''.join(temp[j+1])
                            break
                    except IndexError:
                        break
   
            feature = feature.ljust(2048, '0')[:2048]
            datalist.append({'file':file,'feature':feature}) 
    
    
        with open('data.pickle', 'wb') as file:
            pickle.dump(datalist, file)

    def vectorize(self,label_path:str,ngram:int):
        with open('data.pickle', 'rb') as file:
            loaded_data = pickle.load(file)
        label = pd.read_csv(label_path, encoding = 'big5', dtype={'Column2': str})
        label_x=[]
        label_y=[]
        for data in [record['feature'] for record in loaded_data]:
            label_x.append(" ".join(data[i:i+2] for i in range(0, len(data), 2)))
        vectorizer = CountVectorizer(analyzer='word', ngram_range=(ngram, ngram), lowercase=False)
        X=vectorizer.fit_transform(label_x)
        start = 0    
        for data in [record['file'] for record in loaded_data]:
            count = 0
            f = data[0] + data[1]
            while start < len(label['filename']) and label['filename'][start][0] + label['filename'][start][1] != f:
                start += 1
            while label['filename'][start + count] != data:
                count += 1
            label_y.append(label['label'][start + count])

        return X, label_y

    def pmodel(self,x_train,y_train):
        svm_classifier = LinearSVC(C=0.2)
        knn_classifier = KNeighborsClassifier(n_neighbors=3)
        nb_classifier =  MultinomialNB()
        svm_classifier.fit(x_train,y_train)
        knn_classifier.fit(x_train,y_train)
        nb_classifier.fit(x_train,y_train)
        return svm_classifier, knn_classifier, nb_classifier
    
    def predict(self,svm_classifier,knn_classifier,nb_classifier,x_test,y_test)-> None:        
        print("SVM:",accuracy_score(y_test,svm_classifier.predict(x_test)))
        print("KNN:",accuracy_score(y_test,knn_classifier.predict(x_test)))
        print("NB:",accuracy_score(y_test,nb_classifier.predict(x_test)))


