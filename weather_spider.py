import requests
from bs4 import BeautifulSoup
import html5lib
from pyecharts import Bar

ALL_DATA = []
def parse_page(url):
    headers = {
        "Refer":"http://www.weather.com.cn/textFC/xn.shtml",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }
    response = requests.get(url,headers = headers)
    text = response.content.decode('utf8')
    soup = BeautifulSoup(text,'html5lib')
    # print(response.content.decode('utf-8'))
    conMidtable = soup.find('div',class_='conMidtab')
    tables = conMidtable.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            min_temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({'city':city,'min_temp':min_temp})
            # print(min_temp)
            # print({'city':city,'min_temp':min_temp})


def main():
    url_list = [
        'http://www.weather.com.cn/textFC/hb.shtml', # 华北地区
        'http://www.weather.com.cn/textFC/db.shtml', # 东北地区
        'http://www.weather.com.cn/textFC/hd.shtml', # 华东地区
        'http://www.weather.com.cn/textFC/hz.shtml', # 华中地区
        'http://www.weather.com.cn/textFC/hn.shtml', # 华南地区
        'http://www.weather.com.cn/textFC/xb.shtml', # 西北地区
        'http://www.weather.com.cn/textFC/xn.shtml', # 西南地区
        'http://www.weather.com.cn/textFC/gat.shtml', # 港澳台地区
    ]
    for url in url_list:
        parse_page(url)
    #分析数据
    #根据最低气温排序

    #按天气最低进行排序，并只取10个
    ALL_DATA.sort(key=lambda data:data['min_temp'])
    data = ALL_DATA[0:10]
    #分别取出所有城市和温度
    cities = list(map(lambda x:x['city'],data))
    temps = list(map(lambda x:x['min_temp'],data))

    chart = Bar("中国天气最低气温排行榜")
    chart.add('',cities,temps)
    chart.render('temperature.html')


if __name__ == '__main__':
    main()

