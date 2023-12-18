'''the code in this part is a additional part, since when we making the analysis, coming up a thought about making a analysis basing on
the different district of HK.  so we just add a new code for getting the  district that each property belonging to . And the whole flow is
 similar to the step to getting the longtitude and latitude , and it is also using the approach of gaode api. the only difference is that,
 the input parameter is longtitude and latitude, instead of the precise address.'''


import requests
import pandas as pd

table=pd.read_excel('C:/Users/666/Desktop/python/7890 project/squarefoot_with_longla.xls')
table['district']=''


##
def get_20_location(block_num):
    longla_list=[]
    for i in range(20):
        longla_list.append(table['long_la'][i+20*block_num])
    location=''
    for j in range(20):
        location+=longla_list[j]+'|'
    return location


# location_test='114.163825,22.276284|114.027788,22.292031'
def gaodde(location):
    parameters = {'key': '','location': location,'batch':'true'}
    base = 'https://restapi.amap.com/v3/geocode/regeo'
    response = requests.get(base,parameters)
    answer = response.json()
    district_list=[]
    for i in range(len(answer['regeocodes'])):
        print(answer['regeocodes'][i]['addressComponent']['district'])
        district_list.append(answer['regeocodes'][i]['addressComponent']['district'])
    return district_list


def append_to_table(district_list):
    for i in range(20):
        table['district'][i+20*block_num]=district_list[i]



##  主函数运行

for n in range(928):
    block_num=n
    location=get_20_location(block_num)
    district_list=gaodde(location)
    append_to_table(district_list)
    print('第{}个block完成'.format(n))


##  数据输出为excel
outputpath='C:/Users/666/Desktop/python/7890 project/squarefoot_with_district.csv'
table.to_csv(outputpath,sep=',',index=False,header=True)





