###PART 1 Wep Scraping
## Get data from hse(use parsel package)

import requests
import csv
import time

f = open('28hse.csv',mode='a',encoding='utf-8-sig',newline='')
csv_writer = csv.DictWriter(f,fieldnames=['标题','地理位置','房屋面积','简易标签','价格','房源链接'])
csv_writer.writeheader()

for page in range(1,1601):
    print(f'============running in page{page}===============' )
    time.sleep(5)
    url = f'https://www.28hse.com/rent/page-{page}'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    html_data = response.text
    import parsel
    selector = parsel.Selector(response.text)
    divs = selector.css('.property_item .content')
    for index in divs:
        title = index.css('.detail_page::text').get()
        location_list = index.css('.district_area a::text').getall()
        location_str = '|'.join(location_list)
        unit_area_list = index.css('.areaUnitPrice div::text').getall()
        unit_area_str = '|'.join(unit_area_list)
        label_list = index.css('.tagLabels .label::text').getall()
        label_str = '|'.join(label_list)
        price = index.css('.extra .green::text').get()
        index_url = index.css('.header.wHoverBlue a::attr(href)').get()
        dit = {
            '标题': title,
            '地理位置': location_str,
            '房屋面积': unit_area_str,
            '简易标签': label_str,
            '价格': price,
            '房源链接': index_url,
        }
        csv_writer.writerow(dit)
        print(title,location_str,unit_area_str,label_str,price,index_url)



