import pandas as pd
import numpy as np
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import GeoType
from pyecharts.charts import Map
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']='SimHei'
plt.rcParams['axes.unicode_minus']=False#是图片显示中文
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
#1 简便查看
data = pd.read_excel(r'/Users/liuliu/python 数据分析/squarefoot.xls')
data.describe().T
data.info()
#2 房源在不同区域的分布情况
df=data.district.value_counts()
#3 房源分布可视化
# 绘制数值型特征列的箱型图
import matplotlib.pyplot as plt
import seaborn as sns
sub1=['size','room_num','bathroom_num','price']
fig,axes=plt.subplots(len(sub1),1,figsize=(20,10))
plt.subplots_adjust(hspace=1)
for i,feature in enumerate(sub1):
    sns.boxplot(data[feature],ax=axes[i],whis=2,orient='h')
plt.show()
#作箱线图，观察不同区域，不同房型的价钱分布
import matplotlib.pyplot as plt
# 在之前代码的基础上增加两行代码
plt.rcParams['font.sans-serif']=['SimHei']    # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来显示负号
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.figure(figsize=(16,12))
sns.boxplot(y='district',x='price',data=data,
           showmeans=True,width=0.3,color='red',
           flierprops={'marker':'o','markerfacecolor':'indianred','markersize':5},
           meanprops={'marker':'D','markersize':3,'color':'black'},
           medianprops={'linestyle':'--','color':'orange'})
plt.xticks(rotation=15,fontsize=10)
plt.ylabel('地区',fontsize=15)
plt.xlabel('价格',fontsize=15)
plt.legend(loc='best',fontsize=15)

# 用饼图可视化房源分布区域占比

plt.figure(figsize=(12,12))
plt.title("香港各区房源分布比")
nei_sum=data['district'].value_counts()
labels=nei_sum.index
plt.pie(nei_sum,labels=labels,autopct='%.2f%%',explode=[0.1 if i in ['东城区','朝阳区 / Chaoyang','海淀区'] else 0 for i in labels],
       startangle=90,counterclock=False,textprops={'fontsize':12,'color':'black'},colors=sns.color_palette('RdBu',n_colors=18))
plt.legend(loc='best', fontsize=10)
plt.show()


#地图可视化
import geopandas
hk =geopandas.read_file(r'/Users/liuliu/Downloads/香港特别行政区.json')
fig, ax = plt.subplots(figsize=(10, 8), dpi=200)

hk_map = hk.geometry.plot(ax=ax, fc="#CCEBEB", ec="#009999", lw=1)
ax.text(.91, 0.05, '\nVisualization by DataCharm', transform=ax.transAxes,
        ha='center', va='center', fontsize=8)

ax.axis('off')  # 移除坐标轴
plt.savefig('hk_charts_pir.png', width=8, height=8,
            dpi=900, bbox_inches='tight', facecolor='white')

for loc, label in zip(hk.geometry.representative_point(),hk.name):
    ax.text(loc.x,loc.y,label,size=5,color="#0DCFE3")

for x,y,price in zip(data['lo'],data['la'],data['price']):
    hk_map.scatter(x,y,price/500,color='#FFEB3B',alpha=.5,ec='k',lw=.1)

from adjustText import adjust_text
# 使用adjustText修正文字重叠现象
new_texts = [ax.text(loc.x,loc.y,label,size=5,color="#0DCFE3") for loc, label in \
             zip(hk.geometry.representative_point(),hk.name)]
adjust_text(new_texts,only_move={'text': 'xy'},)