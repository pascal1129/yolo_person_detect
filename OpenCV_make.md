## 0.0、Linux下OpenCV编译和指定版本调用

在多人共用的服务器上，可能存在OpenCV多版本共存的混乱局面，给其他依赖OpenCV的代码的编译带来不确定性。为此本文档主要是介绍如何在Ubuntu上编译OpenCV，并通过环境变量调用指定版本。



## 0.1、CMake与Mak最简单的理解

正常的开发步骤：源文件(.c) --> 编译得到目标文件(.o) --> 连接得到可执行文件(.exe)

源文件过多时，可使用make工具批处理编译源文件。此外，makefile是一个事先编写好的规则文件，make依据它来批处理编译。cmake工具能够输出各种各样的makefile或者project文件，它的依据是cmakelist。

![Cmake](https://img-blog.csdn.net/20160521170837135)

更多内容参见 [CMake与Make最简单直接的理解 - CSDN博客](https://blog.csdn.net/zgrjkflmkyc/article/details/51471229)



## 1、下载OpenCV源码

可以去 [OpenCV官网](https://opencv.org/) 下载源码；

这里以3.4.1版本的编译为例进行演示，版本选择需要自己考虑，比如说但**3.4.1版本与yolo不兼容，亲测3.4.0版本与yolo兼容**

下载地址：<https://codeload.github.com/opencv/opencv/tar.gz/3.4.1>



## 2、解压缩

```
tar -zxvf opencv-3.4.1.tar.gz
```



## 3、cmake编译

```
cd opencv-3.4.1
mkdir build
cd build

# 注意，下面是一条指令，部分环境下可能显示成两行，看起来像两行
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/home/pascal/software/opencv341 ..
```

得到结果

```
-- Configuring done
-- Generating done
-- Build files have been written to: /home/pascal/downloads/opencv-3.4.1/build
```



## 4、make编译

```
make
```

此过程耗时较久，服务器CPU有6个核心，因此可通过make -j12加速，一般取CPU核心数的两倍

查看CPU有几个核心，可以参考： [Linux 如何查看主机的cpu总个数和总内存_百度经验](https://jingyan.baidu.com/article/63f2362848492a0209ab3d49.html) 和 [make太慢了，加快编译速度的方法 make -j - CSDN博客](https://blog.csdn.net/gonghuihuihui/article/details/79091762)

得到下面这个结果，说明编译成功

[![FF0Umj.md.png](https://s1.ax1x.com/2018/11/24/FF0Umj.md.png)](https://imgchr.com/i/FF0Umj)



## 5、安装

```
make install
```

结果：

[![FF0spT.md.png](https://s1.ax1x.com/2018/11/24/FF0spT.md.png)](https://imgchr.com/i/FF0spT)



## 6、更新环境变量，确定OpenCV的调用版本

在.bashrc文件中添加新的opencv路径：

```
export PKG_CONFIG_PATH=/home/pascal/software/opencv341/lib/pkgconfig
export LD_LIBRARY_PATH=/home/pascal/software/opencv341/lib
```

更新bashrc：

```
source ~/.bashrc
```

参考资料：

主要流程参考： [Linux下面安装OpenCV3.3.0 - CSDN博客](https://blog.csdn.net/u013685902/article/details/78695094)

环境变量设置参考：[ubuntu下opencv2.4.10 和 opencv 3.10 多版本切换问题 - CSDN博客](
https://blog.csdn.net/kekong0713/article/details/53688131)

整体流程可参考，步骤五release和步骤七cd ..不对:[ubuntu12.04 64位安装opencv-2.4.9 - CSDN博客](https://blog.csdn.net/dengshuai_super/article/details/51394118)



## 7、验证：OpenCV版本查看

pkg-config可用与列举出某个库的相关信息，比如此库的路径、相关头文件路径等，常用命令如下：

```
# 头文件
pkg-config --cflags opencv

# 库文件
pkg-config --libs opencv

# 库版本
pkg-config --modversion opencv
```

经过重新设置，服务器上的OpenCV相关参数发生如下变化：

```
版本：3.1.0 --> 3.4.1
库文件：/usr/local/lib --> /home/pascal/software/opencv341/lib
头文件：/usr/local/include/opencv /usr/local/include -->
/home/pascal/software/opencv341/include/opencv /home/pascal/software/opencv341/include
```

参见：[pkg-config 详解 - CSDN博客](https://blog.csdn.net/newchenxf/article/details/51750239)

