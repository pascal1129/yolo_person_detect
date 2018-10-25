import os
import pandas as pd
import numpy as np
from PIL import Image

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


if __name__ == '__main__':
    df = pd.read_csv('./train_labels.csv')
    print('Origin shape: ',df.shape)
    df = df.dropna(axis=0)
    labels = np.array(df)
    num_of_labels = labels.shape[0]
    print('Preprocessed: ',num_of_labels)

    image_ids = []

    for index in range(num_of_labels):
        image_path = './JPEGImages/'+ labels[index,0]
        img = Image.open(image_path)
        w = img.size[0]
        h = img.size[1]

        xmin = int(labels[index,1].split(' ')[0])
        ymin = int(labels[index,1].split(' ')[1])
        xmax = int(labels[index,1].split(' ')[2])
        ymax = int(labels[index,1].split(' ')[3])

        b = (float(xmin), float(xmax), float(ymin), float(ymax))
        bb = convert((w,h), b)

        cls_id = 0

        image_id = labels[index,0][:-4]
        with open('./labels/' + image_id + '.txt', 'a+') as out_file:
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


        if image_id not in image_ids:
            image_ids.append(image_id)

    print('labels created done')

    with open('./train.txt','w') as f:
        wd = os.getcwd()
        for image_id in image_ids:
            f.write('%s/JPEGImages/%s.jpg\n'%(wd, image_id))
        f.close()

    print('train.txt created done')