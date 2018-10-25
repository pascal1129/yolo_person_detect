import os
import shutil

# person类训练集、测试集标签地址
VOC2012_trainval =  'VOCdevkit/VOC2012/ImageSets/Main/person_trainval.txt'
# VOC2012_test =      'VOCdevkit/VOC2012/ImageSets/Main/person_test.txt'
# 标签所在文件夹
VOC2012_label =     'VOCdevkit/VOC2012/ImageSets/Main/'

# 图片和标注地址
VOC2012_images =        'VOCdevkit/VOC2012/JPEGImages'
VOC2012_annotations =   'VOCdevkit/VOC2012/Annotations'

# 待删除的无用文件夹
FOLDER_TO_DELETE = ['VOCdevkit/VOC2012/SegmentationClass', 'VOCdevkit/VOC2012/SegmentationObject', 'VOCdevkit/VOC2012/ImageSets/Layout', 'VOCdevkit/VOC2012/ImageSets/Segmentation','VOCdevkit/VOC2012/ImageSets/Action']

# 含person类的图片的序列号
train_person_index = []
# test_person_index = []

def rm_unnecessary_files():
    # 删除无用的文件夹 
    for file in FOLDER_TO_DELETE:
        if os.path.exists(file):
            shutil.rmtree(file)
    # 清空无用和过期的label文件
    for file in os.listdir(VOC2012_label):
        if 'person' not in file:
            os.remove(os.path.join(VOC2012_label, file))
    print('[0] remove unnecessary files done')  

def get_index(dataset_path):
    person_index = []
    with open(dataset_path,'r') as f:
        line = f.readline()
        # 判断文件是否结束
        while line:
            # 一行十个字符，最后一个字符是'\n'，因此检测倒数第三个字符即可
            if line[-3] != '-':
                index = line.split(' ')[0]
                # 如果该序列号不存在于列表，则添加
                if index not in person_index:
                    person_index.append(index)
            line = f.readline()
        f.close
    # 排个序，便于使用
    person_index.sort()
    print('[1] extract pics: %d'%(len(person_index)))
    return person_index


def write_txt(person_index, label_path):
    # 所有的训练数据写入train
    with open(os.path.join(VOC2012_label, label_path),'w') as f:
        for index in person_index:
            line = index + '\n'
            f.write(line)
    f.close
    print('    write labels into txt finished')


if __name__ == '__main__':
    rm_unnecessary_files()                              # 删除无用文件夹
    train_person_index = get_index(VOC2012_trainval)    # 提取训练集中的含人数据
    write_txt(train_person_index, 'train.txt')
    print('[2] All is done!')