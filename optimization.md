# 一个可转债的回测

直接复制一个之前写的内容，有点乱

[TOC]



## 1. 是否存在转债价格变为0后，又出现非0价格的情况

1. 发现1例中途几天价格为0，后又恢复的转债

   1. 110035.SH（白云转债）
   2. 于2017/6/13 -2017/6/20转债价格为0四天，后恢复
   3. ![13b649f7393207395807257e3755a4e](C:\Users\zikep\AppData\Local\Temp\WeChat Files\13b649f7393207395807257e3755a4e.png)
   4. 目前无法在网络上搜索到白云转债相关数据，找到公告“**白云机场关于公司可转换公司债券赎回的提示性公告**”显示

   >（六）交易和转股
   >
   >赎回登记日次一交易日起（2017年6月7日），白云转债将停止
   >
   >交易和转股。

   5. 且2017/6/20后的数据均为125.95，未发生变化，因此认为白云转债在2017/6/7日后已停止交易

2. 发现5例曾出现过一段时间，后长期转债价格为0，

   1. 113011.SH
   2. 113012.SH
   3. 128014.SZ
   4. 127004.SZ
   5. 128015.SZ
   6. 以上转债均于2017/6/20转债价格变为0，于2019/9/16又恢复数据
   7. ![112fd23c6232dbf7e1aae42b2292d8d](C:\Users\zikep\AppData\Local\Temp\WeChat Files\112fd23c6232dbf7e1aae42b2292d8d.png)
   8. 经过查询，根据搜狐证券中关于[113011.SH（光大转债）](http://q.stock.sohu.com/cn/113011/lshq.shtml)的数据显示，中间时间有交易数据，因此认为可能是由于**数据库的内容缺失**，目前暂时还没有补上中间缺失的数据





## 2. 修正之前回测存在的评级错误问题

评级文件中所标注的证券代码和价格、溢价率文件中标注的证券代码不同，（例如在价格文件中代码为100220.SH，评级文件中为122.SH）

根据修正后的评级情况，将上次的回测结果进行了修正

## 3. 将‘AA+’评级的转债纳入c方案

即  <评级为AAA 或AA+且 到期收益率大于1.5% 且转股溢价率小于40%>的回测结果



## 4.计算多个买入卖出触法价格情况下的收益率

 将买入价格和卖出价格分别在[110,128]和[130,148]之间选取，步长取2，分别计算收益，得到的结果如下表，其中第一列表示买入的下限的变化，第一行表示卖出的上限变化（**由于后面两列还没计算完所以暂时无数据**）、

|         | 130    | 132    | 134    | 136    | 138    | 140    | 142    | 144    | 146  | 148  |
| ------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ---- | ---- |
| **110** | 19.66% | 27.82% | 28.85% | 31.01% | 32.26% | 33.56% | 35.70% | 36.96% |      |      |
| **112** | 20.24% | 25.54% | 27.18% | 31.74% | 32.99% | 34.18% | 36.32% | 37.58% |      |      |
| **114** | 21.29% | 25.72% | 27.33% | 27.23% | 27.88% | 29.81% | 31.63% | 32.37% |      |      |
| **116** | 24.49% | 29.74% | 31.36% | 31.74% | 32.39% | 34.35% | 36.17% | 38.28% |      |      |
| **118** | 24.38% | 27.72% | 30.23% | 32.18% | 34.22% | 36.66% | 37.99% | 39.04% |      |      |
| **120** | 24.49% | 27.87% | 30.38% | 32.25% | 33.82% | 35.27% | 36.60% | 38.86% |      |      |
| **122** | 23.21% | 26.50% | 28.80% | 30.66% | 32.28% | 33.72% | 35.04% | 36.76% |      |      |
| **124** | 17.08% | 18.63% | 20.31% | 26.94% | 29.13% | 30.54% | 31.33% | 33.04% |      |      |
| **126** | 17.22% | 18.62% | 19.74% | 23.52% | 25.12% | 26.56% | 27.62% | 28.66% |      |      |
| **128** | 13.46% | 15.46% | 17.71% | 21.98% | 22.91% | 24.60% | 25.86% | 27.20% |      |      |

将该表格着色后，颜色偏绿表示受益更高，颜色偏红表示收益低

![1581665686338](C:\Users\zikep\AppData\Roaming\Typora\typora-user-images\1581665686338.png)

从现有结果大致可以看出当下限取118时收益率最高，最优上限暂时未知