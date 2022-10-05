from bs4 import BeautifulSoup    ## a package handle the html text data.
import re                        ##import the regular expression  (re)
import urllib.request,urllib.error   ## import the urllib package for request a html and distinguish the error
import xlwt                  ## import the package for operating excel in pycharm.




##  define a function using to get the html data from the website we need.
def askurl(url):
    head={'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36'
    }
    request=urllib.request.Request(url,headers=head)
    html=''
    try:                                                   ## in case there are some unobserved error appear during the process, i use the try error
        response=urllib.request.urlopen(request)           ## to catch the error. and also i use the hasattr() function to catch the error code and the
        html=response.read().decode('utf-8')               ##  reason of the code if error exist.
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e,'code')
        if hasattr(e,'reason'):
            print(e.reason)
    return html


"""
since in the data getting part, i have to use the regular expression to get some of the data, so i first apply the re.compile() to create the rule
to locate the data i need. i only create the rule for room data and bath room data, since their data structure is a little bit complex, cant using
BS4 to get the information directly.
"""
roomrule = re.compile(r'<li class="ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF gHpOjD attributes-facilities-item-wrapper bedroom-facility"><i class="Icon-ciffxn laCPQJ rui-icon rui-icon-bed-small property-bedroom"></i>(.*)</li>')
bathroomrule = re.compile(r'<li class="ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF gHpOjD attributes-facilities-item-wrapper bathroom-facility"><i class="Icon-ciffxn lmepmd rui-icon rui-icon-bath-small property-bathroom"></i>(.*)</li>')


##  here i create a function for getting the data from a given url.
def getdata(baseurl):
    datalist = []
    for i in range(0,90):
        url=baseurl+str(i)
        print('第{}页'.format(i + 1))
        html=askurl(url)

        soup = BeautifulSoup(html, 'html.parser')
        try:
            listinlist = soup.find_all('ul', attrs={'class':'ListingsListstyle__ListingsListContainer-gFQClw hrxUtk listing-list','data-test-id':'listing-list'})
            listinlist = listinlist[0]
        except IndexError:
            continue
        for i in listinlist:
            data=[]

            # get the property name
            name=i.find_all('h2',attrs={'class':'ListingDescriptionMiddlestyle__TitleWrapper-jcwIxd fZKpIG listing-title'})
            if len(name)==0:
                continue
            name=name[0].string
            data.append(name)
            # # print(name)


            ## get the loction of the property
            address=i.find_all('div',attrs={'class':'ListingDescriptionMiddlestyle__AddressWrapper-gHTFBT dGmqjA address'})
            if len(address)==0:
                 continue
            address=address[0].string
            data.append(address)


            ##  get the room type of the property
            house_type=i.find_all('div',attrs={'class':'ListingDescriptionMiddlestyle__PropertyTypeWrapper-ogahe qpbwG property-type'})
            if len(house_type)==0:
                continue
            house_type=house_type[0].string
            data.append(house_type)

            ## get the size of the house
            size=i.find_all('span',attrs={'class':'size'})
            if len(size)==0:
                continue
            size=size[0].string
            data.append(size)



            ## get the number of the room.
            room=i.find_all('li',attrs={'class':'ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF gHpOjD attributes-facilities-item-wrapper bedroom-facility'})
            if len(room)==0:
                continue
            room=room[0]
            room1=re.findall(roomrule,str(room))[0]
            data.append(room1)


            ## get the number of the bathroom.
            bathroom=i.find_all('li',attrs={'class':'ListingAttributesstyle__ListingAttrsFacilitiesItemWrapper-jCPNCF gHpOjD attributes-facilities-item-wrapper bathroom-facility'})
            if len(bathroom)==0:
                continue
            bathroom=bathroom[0]
            bathroom1=re.findall(bathroomrule,str(bathroom))[0]
            data.append(bathroom1)

            #  get the rental price of the house
            price=i.find_all('li',attrs={'class':'ListingPricestyle__ItemWrapper-cBCBVa jXCKCc'})
            if len(price)==0:
                continue
            price=price[0].string
            price=price.strip('$')
            data.append(price)

            datalist.append(data)
    return datalist                        ###  get all the property information, and return datalist.  the form is nested list. eg.  [[house1 information],[house2 information],[house3 information],[house4 info],....]




##  this function is help to write the data from the datalist to the excel, and save the data.
def savedata(datalist,savepath):
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet=book.add_sheet('squarefoot3001_16000',cell_overwrite_ok=True)
    col=('property_name','address','type','size','room_num','bathroom_num','price')
    for i in range(0,7):
        sheet.write(0,i,col[i])
    for i in range(0,len(datalist)):
        data=datalist[i]
        for j in range(0,7):
            sheet.write(i+1,j,data[j])
    book.save(savepath)




## set a main function, in order to combine three functions we define above. make it run automatically.
def main():
    baseurl='https://www.squarefoot.com.hk/sc/%E7%A7%9F%E6%88%BF/list/?bedroom=1&minPrice=3000&maxPrice=16000&page='
    #爬取网页
    datalist=getdata(baseurl)
    savepath='squarefoot_3001_16000.xls'
    #3.保存数据
    savedata(datalist,savepath)



if __name__ =='__main__':            #当程序执行时
#调用函数
    main()
    print('爬取完毕')
































