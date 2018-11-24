## YOLOv3行人检测

本脚本集合主要是针对YOLOv3的两个主流版本（[AlexeyAB/darknet](https://github.com/AlexeyAB/darknet) & [pjreddie/darknet](https://github.com/pjreddie/darknet)），本身不包含YOLOv3的代码和配置文件，但是根据指引可以完成一个效果较好的行人检测系统。

目前主要是以下几个功能：

0. 将YOLOv3常用的网址和资料归纳整理了一下；
1. 提供代码，帮助从VOC2007/VOC2012/COCO等数据集中提取出person类图片，并转换标注。这里提取VOC数据集时默认保留了全部difficult=1的图片，效果会更好，具体请参见[Issue #1200](https://github.com/AlexeyAB/darknet/issues/1200)；
2. 提供代码，帮助计算mAP正确率；
3. 建议使用tee指令保存训练日志，可使用本文提供的脚本实现训练过程可视化；


## 效果对比

YOLO_mine（基于AB版本，只检测行人）

![kite-7-final](https://github.com/pascal1129/yolo_person_detect/blob/master/images/kite-7-final.jpg)

YOLO_pj（pj版本，所有类别全检测）

![kite-pj](https://github.com/pascal1129/yolo_person_detect/blob/master/images/kite-pj.jpg)



## 文件结构

```
yolo_person_detect
|
│  README.md
│
├─make_yolo_dataset
│  │  helmet_to_yolo.py                     # 某次比赛用到的转换代码
│  │  show_voc_xml.py                       # 可视化VOC数据集
│  │  show_yolo_label.py                    # 可视化YOLO数据集
│  │  xml2json.py                           # 
│  │  coco_to_yolo.py                       # COCO --> YOLO
│  │
│  ├─YOLO_VOC2007                           # VOC2007
│  │      extract_person.py                 # 从VOC2007数据集中提取person图片
│  │      voc_label.py                      # 将提取到的person图片转为YOLO格式
│  │
│  └─YOLO_VOC2007_2012                      # VOC2007 + VOC2012
│          extract_person_2007.py
│          extract_person_2012.py
│          voc_label.py
│
├─yolo_compute_mAP_on_VOC2007               # 在VOC2007上测试性能
│      reval_voc_py3.py
│      voc_eval_py3.py
│
└─yolo_loss_analyse
    │  analyse.py                           # 训练过程可视化代码
    │  result.png                           # 可视化训练过程
    └─loss
            train7-loss.txt                 # 示例训练日志
```



## 官方Demo运行

- 下载源代码、预训练权重

```Shell
git clone https://github.com/AlexeyAB/darknet.git
cd darknet/
wget https://pjreddie.com/media/files/yolov3.weights
```

- 如果需要编译OpenCV，可参见 [Pascal129/yolo_person_detect: Linux下OpenCV编译和指定版本调用](https://github.com/pascal1129/yolo_person_detect/blob/master/OpenCV_make.md)
- 修改Makefile并编译，可以加上 -j8 等参数设定多CPU编译

```Shell
vim Makefile	
make
```

注意：OpenCV版本号亲测3.40可用，但是3.41不可用，可参见[YOLOv3的Darknet在OpenCV下编译出错填坑](https://zhuanlan.zhihu.com/p/36933700)

- 试运行图片检测demo
```
./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg
```

- 试运行视频检测demo

```
./darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights <video file>
```



## 数据集准备

处理时，默认所有的train = train+val，不区分二者，2007单独还有个test

#### 0、下载VOC2007+2012数据集

下载数据集

    wget <http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar>
    wget <http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar>
    wget <http://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar>

解压缩

    tar xvf VOCtrainval_06-Nov-2007.tar
    tar xvf VOCtest_06-Nov-2007.tar
    tar xvf VOCtrainval_11-May-2012.tar

#### 1、通过extract_person.py提取含人数据

分别运行2007和2012的提取代码

#### 2、通过voc_label.py转化voc数据格式为yolo支持的格式
会在脚本所在文件夹产生相应的txt文本，存储数据集地址信息：

    2007_train.txt 
    2007_test.txt
    2012_train.txt

可根据情况进行配置，比如说不想要测试集，那就整合下训练集、测试集：

	cat 2007_train.txt 2012_train.txt > train.txt



## 配置文件

#### 0、下载源代码，下载预训练权重

	git clone https://github.com/AlexeyAB/darknet.git
	wget https://pjreddie.com/media/files/darknet53.conv.74

#### 1、配置Makefile

#### 2、配置cfg/voc.data
```
classes= 1
train  = /home/pascal/person_data2/train.txt
valid  = /home/pascal/person_data2/2007_test.txt
names = data/voc.names
backup = backup
```

#### 3、配置data/voc.names

	person
#### 4、新建backup文件夹

	mkdir backup

#### 5、配置cfg/yolov3-voc.cfg

	batch, sub按需修改
	一共三个YOLO层，均需要修改：
	classes=1
	filters=18		3*(1+1+4)=18
	
	# filters=(classes + coords + 1)*<number of mask>

#### 6、make编译

#### 7、开始训练，并留下日志

    ./darknet detector train cfg/voc.data cfg/yolov3-voc.cfg ../darknet53.conv.74 -gpus 0,1 | tee -a helmet1.txt

#### 8、恢复训练

	./darknet detector train cfg/voc.data cfg/yolov3-voc.cfg backup/yolov3-voc.backup -gpus 0,1 | tee -a train7.log

#### 9、单张图片测试（需要将batch、subvision均修改为1）

	./darknet detector test cfg/voc.data cfg/yolov3-voc.cfg backup/yolov3-voc_final.weights test_data/p0.jpg

#### 10、性能检测

计算mAp

	./darknet detector map cfg/voc.data cfg/yolov3-voc.cfg backup/yolov3-voc_80172.weights

计算recall（2097张的结果）

	./darknet detector recall cfg/voc.data cfg/yolov3-voc.cfg backup/yolov3-voc_final.weights 

VOC2007test

```Shell
mkdir results
#（PJ版本需要这一步）
# (会在/results生成默认的comp4_det_test_person.txt，这是在VOC2007 test上的结果)
./darknet detector valid cfg/voc.data cfg/yolov3-voc.cfg backup/yolov3-voc_final.weights -gpu 0,1

#在 https://github.com/AlexeyAB/darknet/tree/master/scripts 下载voc_eval_py3.py reval_voc_py3.py ，在./执行
python reval_voc_py3.py output_dir='./'
```



## 训练常用指令

训练：加上了tee指令把训练日志保存到txt文本

```
./darknet detector train cfg/voc.data cfg/yolov3-voc.cfg darknet53.conv.74 -gpus 0,1 |tee -a train7.txt
```

恢复训练

```
./darknet detector train cfg/voc.data cfg/yolov3-voc.cfg backup/yolov3-voc.backup -gpus 0,1 tee -a train7.txt
```

测试

```
./darknet detector test cfg/voc.data cfg/yolov3-voc.cfg backup/yolov3-voc_50000.weights ../test_data/p2.jpg
```



## VOC数据集格式

以上述VOC2007+VOC2012数据集为例，以下均为处理过的数据集：

    VOCdevkit/
    ├── VOC2007
    │   ├── Annotations     原始的VOC标注信息
    │   ├── ImageSets		
    │   │   └── Main		VOC的类标签，和人为提取的样本索引
    │   ├── JPEGImages	    图片文件夹
    │   └── labels			VOC-->YOLO格式的标注信息
    └── VOC2012
         ├── Annotations
         ├── ImageSets
         │   └── Main
         ├── JPEGImages
         └── labels

#### VOC的xml格式

核心部分如下:

	<annotation>
		<object>
	        <name>person</name>
	        <difficult>0</difficult>
	        <bndbox>
	            <xmin>xxx</xmin>
	            <ymin>xxx</ymin>
	            <xmax>xxx</xmax>
	            <ymax>xxx</ymax>
			</bndbox>
		</object>
	</annotation>

#### VOC的图片格式

行列分布同pillow.Image，先行后列



## COCO数据集格式

数据集格式

	COCO
	├── annotations
	├── filelist			训练图片位置
	└── train2017
	    ├── JPEGImages	图片
	    └── labels			生成的YOLO格式标签

[COCO数据集下载](<http://cocodataset.org/#download>)

[COCO-->YOLO格式转换，代码包含了操作介绍](<https://github.com/PaulChongPeng/darknet/blob/master/tools/coco_label.py>)



## 数据集统计

数据集        | 训练集（person）| 测试集（person）
----------------| ---|---
VOC2007   | 5011（2095）  |4952（2097）
VOC2012   | 17125（4374）|未统计
COCO2017| 118287（64115）|未统计

\* 括号里面为person类图片数量



## 训练过程

数据集：VOC2007+VOC2012+COCO2017

硬件环境：GTX1080ti*2, Ubuntu16.04, CUDA9

训练迭代数：8w iters

训练技巧：参见[how-to-train-to-detect-your-custom-objects](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects)



![训练过程](https://github.com/pascal1129/yolo_person_detect/blob/master/images/loss_analyse_result.png)

上图是脚本[analyse.py](https://github.com/pascal1129/yolo_person_detect/blob/master/yolo_loss_analyse/analyse.py)对训练日志[train7-loss.txt](https://github.com/pascal1129/yolo_person_detect/blob/master/yolo_loss_analyse/loss/train7-loss.txt)的训练过程可视化

配置：batch=64/16，总计8w次迭代，在原来的5w次之后，追加2w次0.001和1w次0.0001，0.00001

耗时：5h/万次迭代

结果：loss=0.98

map        | p| r|f1|IOU
----------------| ---|---|--|--
0.8552   | 0.85  |0.84|0.84|69.4%



## 参考资料

[yolov3训练的集大成者](<https://blog.csdn.net/lilai619/article/details/79695109>)

[配置文件的设定参考](<https://blog.csdn.net/helloworld1213800/article/details/79749359>)

[YOLO官网](<https://pjreddie.com/darknet/yolo/>)

