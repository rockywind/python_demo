import numpy as np
import os
import scipy.misc as sm
import cv2
import csv

import codecs

import matplotlib.pyplot as plt

CSV_Dir = '/home/user/vel_analyse/0705_bp_output_whole_changed_vel.csv'
CSV_SaveDir = '/home/user/vel_analyse/0705_bp_output_whole_P2.csv'
Names = ['front_x_position','front_y_position','rear_x_position','rear_y_position']
X_Range = [(-3.5,-1.5),(1.5,3.5)]
Y_Range = [(0,5)]


def getRow(csvd):
    with open(csvd) as csvfile:
        csv_reader = csv.reader(csvfile)  
        birth_header = next(csv_reader)  
    return birth_header


    
def getLines(csvd):
    line = 0
    with open(csvd) as csvfile:
        csv_reader = csv.reader(csvfile)  
        birth_header = next(csv_reader)  
        for row in csv_reader:   
            line = line+1
    return line-1


    
def KeepFront(valsRaw, Names, X_Range, Y_Range):
    frontX, frontY = valsRaw[Names[0]], valsRaw[Names[1]]
    keepx = False
    keepy = False
    for label in X_Range:
        if ((frontX>label[0]) or (frontX==label[0])) and ((frontX<label[1]) or (frontX==label[1])):
            keepx = True
            break
    for label in Y_Range:
        if ((frontY>label[0]) or (frontY==label[0])) and ((frontY<label[1]) or (frontY==label[1])):
            keepy = True
            break
    if keepx and keepy:
        return True
    return False


def KeepRare(valsRaw, Names, X_Range, Y_Range):
    frontX, frontY = valsRaw[Names[2]], valsRaw[Names[3]]
    keepx = False
    keepy = False
    for label in X_Range:
        if ((frontX>label[0]) or (frontX==label[0])) and ((frontX<label[1]) or (frontX==label[1])):
            keepx = True
            break
    for label in Y_Range:
        if ((frontY>label[0]) or (frontY==label[0])) and ((frontY<label[1]) or (frontY==label[1])):
            keepy = True
            break
    if keepx and keepy:
        return True
    return False



def process(row):
    valsRaw = {}
    write_data = {}
    none_data = ['','','','','','','','','']
    for k in row:
        if row[4] >2:
            write_data.append(row[0])
            write_data.append(none_data)




def Keep(Dict, key):
    val = Dict[key]
    if val=='':
        return True
    else:
        return not(val>2)


def DataLoc(csd, idx):
    csvfile = open(csd)
    reDict = {}
    birth_data = []
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:   
        birth_data.append(row)
    data = birth_data[idx+1]
    keys = birth_data[0]
    if len(data)!=len(keys):
        delta = len(keys)-len(data)
        for d in range(delta):
            data.append('')
    for k in range(len(birth_data[0])):
        if data[k]!='':
            val = float(data[k])
        else:
            val = ''
        reDict[keys[k]] = val
    return reDict
        

if __name__=="__main__":
    # Data = pd.read_csv(CSV_Dir)
     file_head = ['frame_id', 'front_x_position', 'front_y_position','front_vel', 'front_P' ,'rear_x_position','rear_y_position','rear_vel', 'rear_P', 'average_vel','host_North', 'host_East', 'target_North','target_East','realtive_vel','realtive_toge']
     with open(CSV_Dir) as csvfile:
        outFile = open(CSV_SaveDir,"w")
        targetWriter = csv.writer(outFile)
        targetWriter.writerow(file_head)
        reader=csv.reader(csvfile)
        next(reader)
        for i,rows in enumerate(reader):
            write_data = []
            none_data = ['','','','','','','','','']
            if rows[4]=='' or (float(rows[4]) > 2) :
                write_data+=[rows[0]]
                write_data+=none_data
                write_data+=rows[10:]
                # print(rows[10:])
            else:
                write_data = rows 
            
            targetWriter.writerow(write_data)
   