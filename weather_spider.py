import requests
from bs4 import BeautifulSoup


def parse_page(url):
    headers = {
        "Refer":"http://www.weather.com.cn/textFC/xn.shtml",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }
    response = requests.get(url,headers = headers)
    text = response.content.decode('utf8')
    soup = BeautifulSoup(text,'lxml')
    # print(response.content.decode('utf-8'))
    conMidtable = soup.find('div',class_='conMidtab')
    tables = conMidtable.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            if index == 0:
                city_td = tds[1]
            else:
                city_td = tds[0]
            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            min_temp = list(temp_td.stripped_strings)
            print(min_temp)
            print({'city':city,'min_temp':min_temp})


def main():
    # url = "http://www.weather.com.cn/textFC/hb.shtml"
    url = "http://www.weather.com.cn/textFC/db.shtml"
    parse_page(url)


if __name__ == '__main__':
    main()

