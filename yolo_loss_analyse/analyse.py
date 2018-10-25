import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

# 提取训练log，去除不可解析的log后，使log文件格式化，生成新的log文件供可视化工具绘图
def extract_log(log_origin, log_new, key_word):
	f_origin = open(log_origin)
	f_new = open(log_new, 'w')
	for line in f_origin:
	    # 去除多gpu的同步log
	    if 'Syncing' in line:
	        continue
	    # 去除除零错误的log
	    if 'nan' in line:
	        continue
	    if key_word in line:
	        f_new.write(line.replace(':',','))
	f_new.close()
	f_origin.close()


def get_loss(file_path):
	result = pd.read_csv(file_path, error_bad_lines=False, names=['batch', 'loss', 'avg', 'rate', 'seconds', 'images'])
	result['avg']=result['avg'].str.split(' ').str.get(1)
	print(result.head())
	print(result.tail())

	result['batch']=pd.to_numeric(result['batch'])
	# result['loss']=pd.to_numeric(result['loss'])
	result['avg']=pd.to_numeric(result['avg'])
	x = result['batch'].values
	y = result['avg'].values
	return(x,y)

def draw_loss():
	x1,y1 = get_loss('train6-loss.txt')
	x2,y2 = get_loss('train6.1-loss.txt')
	
	# 绘制曲线
	plt.plot(x1, y1, color='blue')
	plt.plot(x2, y2, color='orange')
	#设置坐标轴范围
	plt.xlim((0,51000))
	plt.ylim((0,2))
	# 设置坐标轴、图片名称
	plt.xlabel('batch')
	plt.ylabel('avg_loss')
	plt.title('loss')
	# 设置图例
	plt.legend(["train1","train2"], loc="upper right")
	plt.show()





if __name__ == '__main__':
	# extract_log('../../train/train_log/train7.txt','loss/train7-loss.txt','images')


	# draw_loss()
	x1,y1 = get_loss('loss/train7-loss.txt')
	# x4,y4 = get_loss('train7.1-loss.txt')
	
	# 绘制曲线
	plt.plot(x1, y1, color='red')
	# plt.plot(x4, y4, color='blue')
	#设置坐标轴范围
	plt.xlim((1,80200))
	plt.ylim((0,2.5))
	# 设置坐标轴、图片名称
	plt.xlabel('batch')
	plt.ylabel('avg_loss')
	plt.title('loss')
	# 设置图例
	# plt.legend(["train6: COCO+VOC","train6.1: COCO+VOC,upsample"], loc="upper right")
	plt.legend(["train7: COCO+VOC, upsample, 8w iters, AB"], loc="upper right")

	plt.savefig('result.png')
	plt.show()