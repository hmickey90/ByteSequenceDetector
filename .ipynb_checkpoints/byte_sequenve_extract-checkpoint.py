import sys
import pandas as pd
import numpy as np
import os
import r2pipe

def read_magic_number(file_path, num_bytes):
    with open(file_path, 'rb') as file:
        file_size = os.path.getsize(file_path)  # Get the size of the file
        if file_size >= num_bytes:
            magic_bytes = file.read(num_bytes)
        else:
            magic_bytes = b''  # Empty bytes if the file is too small
    return magic_bytes


malpath='/media/dataset/linuxmal/'
maldirlist=os.listdir(malpath)
csv_malfile_path = '/home/mickey/Documents/CSV/mal.csv'
dirlist=["f8","2c","94","a8","d2","b8","8a","6a","aa","fb","fc","35","57","06","eb","2d","d6","8d","20","49","80","92","f4","bf","a5","ac","e7","47","32","f5","de","2b","5f","62","7f","38","63","04","6f","bc","12","df","9b","7c","cd","2e","76","f7","5c","c6","77","86","78","58","30","16","a4","45","8e","70","1c","25","40","24","ae","26","79","dd","b6","68","73","c9","cf","29","9f","b2","72","69","ef","65","01","4a","51","23","71","e4","88","be","4b","0c","a7","82","c7","cb","52","5d","e2","10","d7","50","3f","ab","56","36","d9","b1","95","19","b3","7b","2a","46","a9","ba","15","da","53","6c","9a","b7","ea","f0","5a","3e","ed","39","b9","d5","48","3c","fa","28","6d","d3","84","4d","dc","a2","bb","e3","1b","3a","99","55","f1","17","54","a3","0a","98","7a","fe","14","5e","d8","18","59","64","11","81","c5","41","61","d1","f3","96","d0","7d","97","c4","1f","af","91","ad","33","a1","00","4f","f2","cc","5b","ca","27","9e","bd","db","e5","1e","8c","1a","0f","fd","6e","e6","7e","4c","02","c1","0e","4e","0b","09","42","07","a0","21","6b","0d","ce","85","83","1d","67","c2","3d","03","9d","60","43","13","e9","89","66","b5","f6","c8","34","08","9c","31","a6","93","c0","ec","8f","c3","2f","22","3b","d4","f9","b0","75","74","8b","ee","e1","e8","e0","44","87","90","05","b4","37"]
for dir in maldirlist:
    path=malpath+dir
    if dir in dirlist:
        continue
    for file in os.listdir(path): 
        
        filepath=path+'/'+file  
        magic_number_bytes = read_magic_number(filepath, 4)  # Read the first 4 bytes
        #print(f"Magic Number: {magic_number_bytes.hex().upper()}")
        print(filepath)
        magic_number = magic_number_bytes.hex().upper()
        if  magic_number == '7F454C46' and len(magic_number_bytes) == 4:
            r2 = r2pipe.open(filepath)
            r2.cmd('aaa')
            r2.cmd(f's {"main"}')
            code = r2.cmd('pd')
            r2.quit()
            feature=""
            for i in range(len(code)-23):
                if(code[i]=="x" and code[i+1]!=" " and code[i+2]!=" " and code[i+3]!=" " and code[i+4]!=" " and code[i+5]!=" " and code[i+6]!=" " and code[i+7]!=" " and code[i+8]!=" " and code[i+9]==" " and code[i+10]==" " and code[i+11]==" " and code[i+12]==" " and code[i+13]==" " and code[i+14]==" "):
                    for j in range(8):
                        if code[i+15+j]=="0" or code[i+15+j]=="1" or code[i+15+j]=="2" or code[i+15+j]=="3" or code[i+15+j]=="4" or code[i+15+j]=="5" or code[i+15+j]=="6" or code[i+15+j]=="7" or code[i+15+j]=="8" or code[i+15+j]=="9" or code[i+15+j]=="a" or code[i+15+j]=="b" or code[i+15+j]=="c" or code[i+15+j]=="d" or code[i+15+j]=="e" or code[i+15+j]=="f":
                            feature=feature+code[i+15+j]
                        else:
                            break
                elif(code[i]=="x" and code[i+1]!=" " and code[i+2]!=" " and code[i+3]!=" " and code[i+4]!=" " and code[i+5]!=" " and code[i+6]!=" " and code[i+7]!=" " and code[i+8]!=" " and code[i+9]!=" " and code[i+10]==" " and code[i+11]==" " and code[i+12]==" " and code[i+13]==" " and code[i+14]==" "):
                    for j in range(8):
                        if code[i+16+j]=="0" or code[i+16+j]=="1" or code[i+16+j]=="2" or code[i+16+j]=="3" or code[i+16+j]=="4" or code[i+16+j]=="5" or code[i+16+j]=="6" or code[i+16+j]=="7" or code[i+16+j]=="8" or code[i+16+j]=="9" or code[i+16+j]=="a" or code[i+16+j]=="b" or code[i+16+j]=="c" or code[i+16+j]=="d" or code[i+16+j]=="e" or code[i+16+j]=="f":
                            feature=feature+code[i+16+j]
                        else:
                            break
            if(feature==""):
                break
            if(len(feature)<2048):
                while(len(feature)<2048):
                    feature=feature+"0"
            elif(len(feature)>2048):
                feature=feature[0:2048]
            maldatalist=[]
            columns=['file','feature']
            maldf = pd.DataFrame(columns=columns)
            maldatalist.append({'file':file,'feature':feature}) 
            maldf = pd.DataFrame(maldatalist)

            if os.path.exists(csv_malfile_path):
                maldf.to_csv('/home/mickey/Documents/CSV/mal.csv', index=False, mode='a', header=False)
            else:
                maldf.to_csv('/home/mickey/Documents/CSV/mal.csv', index=False)
            del r2,feature,maldatalist,maldf
        else:
             print("File size is smaller than expected")
print("finish")
