"""this part is to get the accuracte location address, say the longtitude and latitude, basing on the property name  we get from the
 previous data set getting from web scrapping.  in this part, we achieve the purpose with the help of gaode api"""

import requests
import pandas as pd


##  this function is to get the data from the gaode api, the input parameter is the address, which is the property name we get from the previous
def gaodde(address):
    parameters = {'key': 'd8b26ae3b70ae5a74518831fce786e42','address': address }
    base = 'https://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base,parameters)
    answer = response.json()
    long_la=answer['geocodes'][0]['location'].split(',')
    return long_la



#  here i read the previous data, and set a new column, for creating a more precise address. eg. '沙田第一城' to '香港-沙田-沙田第一城'
table=pd.read_excel('C:/Users/666/Desktop/python/7890 project/squarefoot_test.xls')
table['precise_address']=''
table['long_la']=''

for i in range(len(table)):
    table['precise_address'][i]='香港'+table['address'][i]+table['property_name'][i]



##  this function is to add the longtitude and latitude data i get from the gaode() function to the pandas table in the new column i create above.
def get_long_la(table):
    for i in range(0,len(table)):
        address=table['precise_address'][i]
        table['long_la'][i]=gaodde(address)
        print('第{}条完成'.format(i))
    return table

for i in range(0,len(table)):
    table['long_la'][i]=table['long_la'][i][0]+','+table['long_la'][i][1]


##  output the pandas table in CSV form.
outputpath='C:/Users/666/Desktop/python/7890 project/squarefoot_with_longla.csv'
table.to_csv(outputpath,sep=',',index=False,header=True)





















