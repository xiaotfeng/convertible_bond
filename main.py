#coding:utf-8
import pandas as pd
import numpy as np
import time
io='.\data\\'
holding_list={}
sold_earn_list={}
highlevel_list=[130+2*i for i in range(10)]
lowlevel_list=[110+2*i for i in range(10)]


def read_csv_file(filename):
    csv_data=pd.read_csv(io+filename,header=0,index_col=0)
    #c0=csv_data.columns
    csv_data.index=pd.DatetimeIndex(csv_data.index)
    nrow=len(csv_data.index)
    ncol=len(csv_data.iloc[1,])

    # print(ncol)
    # 删除空列
    # zero_col=[]
    # for col in range(ncol):
    #     if csv_data.iloc[:,col].any()==0:
    #         zero_col.append(csv_data.iloc[:,col].name)
    # for col_name in zero_col:
    #     csv_data.pop(col_name)
    # ncol=len(csv_data.iloc[1,])
    # print(ncol)
    return csv_data


def calc_earning(holding_list):
    earning=np.zeros(10)
    #print(holding_list)
    for i,company in enumerate(holding_list):
        buy_price=holding_list[company][0]
        now_price=holding_list[company][1]
        earning[i]=((1000/float(buy_price))*float(now_price)-1000)
    holding_return=np.sum(earning)
    history_return=0
    for item in sold_earn_list:
        history_return+=sold_earn_list[item]
    tot_return=history_return+holding_return
    # print("holding return={}    total return={}".format(holding_return,tot_return))
    global output_list
    return_list=[tot_return,holding_return,history_return]
    for i in range(len(return_list)):
        return_list[i]=round(float(return_list[i]),2)
    output_list.extend(return_list)


def if_buy(date):
    global holding_list
    global purchase_info_str

    # 确定是否买入
    for company in price_data.columns:
        buy_flag = 0

        # 已持有则跳过买入评估环节

        if company in holding_list:
            continue

        # 无视评级买入
        # 价格低于125且溢价率低于25
        price = price_data.loc[date][company]
        premium = premium_data.loc[date][company]
        # price 为0 认为是bond已到期，premium不作为判断依据
        need_rate1=rating_list['AAA']+rating_list['AAA-']+rating_list['AA+']+rating_list['AA']+rating_list['AA-']
        need_rate2=rating_list['AAA']+rating_list['AAA-']+rating_list['AA+']

        # 尴尬，还是做成无视评级了
        if  price < lowlevel and price != 0:
            if premium < 25 :
                purchase_info_str += 'buy:{}-price:{}-low price;'.format(company, price)
                buy_flag=1

        # AAA 评级买入
        # 到期收益率高于1.5且转股溢价率低于40
        elif company in need_rate2 and YTM_data.loc[date][company] > 1.5 and price != 0:
            if premium < 40 :
                purchase_info_str += 'buy:{}-price:{}-AAA;'.format(company, price)
                buy_flag = 1

        # 判断是否已满
        if buy_flag and len(holding_list)<10:
            # 信息输出字符串
            # print('\nbuy--->' + company + '    ', end='')
            holding_list[company] = [price, -1]
        elif buy_flag and len(holding_list)>=10:
            purchase_info_str+='FULL_purchase_fail'


# 评估是否卖出
def if_sell(date):
    global holding_list
    global sale_info_str
    sell_list=[]

    for company in holding_list:
        sale_flag=0
        now_price=price_data.loc[date][company]
        premium= premium_data.loc[date][company]
        # 如果债券到期,不更新价格   溢价率正常情况也可能为0，不作为到期依据
        if now_price==0:# or premium==0
            # print('===the bond is due!!       ',end='')
            # print('\nsale--->' + company + '   ', end='')
            sale_flag=1
            sale_info_str+='sell:{}-price:{}-due;'.format(company,now_price)
        # 未到期，更新价格
        else:
            holding_list[company][1]=now_price
            # 若价格超过140或溢价率高于40
            if now_price>highlevel or  premium>40 :
                # print('\n===price or premium raised!!       ',end='')
                # print('sale--->'+company+'   ')
                sale_info_str += 'sell:{}-price:{}-premium;'.format(company, now_price)

                sale_flag=1
        if sale_flag:
            sell_list.append(company)

    # 从持有列表中删除
    for company in sell_list:
        # 将净收益计入sold_list
        sold_earn_list[company]=(1000/float(holding_list[company][0])*float(holding_list[company][1]))-1000
        holding_list.pop(company)


# 只是想把他们藏起来
if True:
    t0 = time.time()
    # 读取数据文件
    price_data=read_csv_file('price.csv')
    # balance_data=read_csv_file('balance.csv')
    YTM_data=read_csv_file('YTM.csv')
    premium_data=read_csv_file('premium.csv')
    # 读取评级文件
    rating_data=pd.read_csv('./data/rating.csv',index_col=0)
    # 由于评级文件的title与price文件不一致，修改文件title
    rating_data.columns = price_data.columns
    # 用来纪录各个公司评级的文件
    rating_list = {}
    for company in rating_data.columns:
        rating = rating_data.loc['rating'][company]
        if rating_list.get(rating) == None:
            rating_list[rating] = [company]
        else:
            rating_list[rating] += [company]

for highlevel in highlevel_list:
    for lowlevel in lowlevel_list:
        print('\nLow:{}   High:{}'.format(lowlevel,highlevel))
        # 初始化输出文件
        output_file='./result/result初始策略修正{}_{}.csv'.format(lowlevel,highlevel)
        f=open(output_file,'w')
        title=['日期','总收益','持有收益','历史收益','买入情况','卖出情况']+['股票','买入价','现价']*10
        f.write(','.join(title)+'\n')
        f.close()
        # 这样子会快一点，整个添加完之后再关
        f=open(output_file,'a')

        for date in price_data.index:
            tot_time=time.time()-t0
            print('\r'+str(date)[:10]+'      {} min : {} sec'.format(int(tot_time/60),int(tot_time%60)),end='')
            output_list=[]
            output_list.append(str(date)[:10])

            purchase_info_str=''
            sale_info_str=''
            if_buy(date)
            if_sell(date)
            # 计算收益，当期已卖出的计入历史收益
            calc_earning(holding_list)
            # 输出到文件
            # 买入卖出情况
            output_list.extend([purchase_info_str,sale_info_str])
            # 持有的债券信息
            for item in holding_list:
                output_list.append(str(item))
                output_list.extend(holding_list[item])
            for i in range(len(output_list)):
                output_list[i]=str(output_list[i])
            f.write(','.join(output_list)+'\n')
        f.close()



