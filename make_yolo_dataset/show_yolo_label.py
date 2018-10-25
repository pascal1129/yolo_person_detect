import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from PIL import Image,ImageFont,ImageDraw,ImageFont

classes = ['person']
# classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def convert_annotation(year, image_id):
    
    im_path  = ('VOCdevkit/VOC%s/JPEGImages/%s.jpg'%(year, image_id))
    im = Image.open(im_path)

    im_w = int(im.size[0])
    im_h = int(im.size[1])

    draw = ImageDraw.Draw(im)

    
    label_path = ('VOCdevkit/VOC%s/labels/%s.txt'%(year, image_id))

    with open(label_path) as file:
        line = file.readline()
        while line:
            cls = int(line.split(' ')[0])
            x = float(line.split(' ')[1])
            y = float(line.split(' ')[2])
            w = float(line.split(' ')[3])
            h = float(line.split(' ')[4].split('\n')[0])
            
            # print(cls,x,y,w,h)
        
            real_w = im_w * w
            real_h = im_h * h
            x1 = (( x*im_w + 1.0 ) * 2.0 - real_w )/2.0
            x2 = (( x*im_w + 1.0 ) * 2.0 + real_w )/2.0
            y1 = (( y*im_h + 1.0 ) * 2.0 - real_h )/2.0
            y2 = (( y*im_h + 1.0 ) * 2.0 + real_h )/2.0

            draw.rectangle([x1,y1,x2,y2], outline='red', fill=None)
            # 防止越界
            if y1-15>=10:
                draw.text([x1,y1-15],classes[cls],"black")
            else:
                draw.text([x1,y1],classes[cls],"black")
            line = file.readline()
    im.show()
    im.save('tmp/'+image_id+'.jpg')


if __name__ == '__main__':
    convert_annotation('2012','2010_001107')

    # with open('./VOCdevkit/VOC2012/ImageSets/Main/train.txt') as file:
    #     line = file.readline()
    #     while line:
    #         convert_annotation('2012',line[:-1])
    #         line = file.readline()
    #         break
    #     file.close
