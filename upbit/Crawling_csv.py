import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import csv

def crawling(url):
    driver = webdriver.Chrome('./chromedriver')
    time.sleep(2)
    driver.get(url)
    time.sleep(6)
    select = driver.find_elements_by_xpath('//*[@class="ty05"]/li')
    coin_list = []
    base_list = []
    counter_list = []
    cropto_list = []
    price_list = []
    percent_list = []
    rAlign_list = []
    for i in range(4):
        select[i].click()
        time.sleep(0.3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.select('td.tit a')
        codes = soup.select('td.tit em')
        croptos = soup.select('td.price strong')
        prices = soup.select('td.price em')
        percents = soup.select('td.percent')
        rAligns = soup.select('table.highlight td.rAlign')
        for title in titles:
            coin_list.append(title.text)
        for code in codes:
            a = code.text
            base_list.append(a.split('/')[0])
            counter_list.append(a.split('/')[1])
        if i == 0:
            for cropto in croptos:
                price_list.append(cropto.text)
        else:
            for cropto in croptos:
                cropto_list.append(cropto.text)
            for price in prices:
                price_list.append(price.text)
        for percent in percents:
            percent_list.append(percent.text)
        for rAlign in rAligns:
            rAlign_list.append(rAlign.text)
    return( coin_list,
            base_list ,
            counter_list,
            price_list ,
            percent_list,
            rAlign_list,
            cropto_list)


def output_csv(savedate,
          realtime,
          coin_list,
          base_list ,
          counter_list,
          price_list ,
          percent_list,
          rAlign_list,
          cropto_list):
    with open("Output/" + savedate + ".csv", 'w', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Date'] +
                        ['Currency'] +
                        ['Base'] +
                        ['Counter'] +
                        ['Cropto'] +
                        ['Price'] +
                        ['Percent'] +
                        ['rAlign']
                        )
        for i in range(len(coin_list)):
            num = i
            cro_num = len(price_list) - len(cropto_list)
            if i <= cro_num:
                print(i)
                writer.writerow([realtime] +
                                [coin_list[num]] +
                                [base_list[num]] +
                                [counter_list[num]] +
                                ['None'] +
                                [price_list[num]] +
                                [percent_list[num]] +
                                [rAlign_list[num]]
                                )
            else:
                print(i)
                print(num)
                writer.writerow([realtime] +
                                [coin_list[num]] +
                                [base_list[num]] +
                                [counter_list[num]] +
                                [cropto_list[num - cro_num]] +
                                [price_list[num]] +
                                [percent_list[num]] +
                                [rAlign_list[num]]
                                )
    return ("코빗 화이팅ㅎㅎ")


while(1):
    url = "https://www.upbit.com/exchange?code=CRIX.UPBIT.KRW-BTC"
    ts = time.time()
    realtime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    savedate = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    savetime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    print("현재시간 : ",savetime)
    time.sleep(1)
    if savetime == "08:59:00":
        print("크롤링 진행중 ...")
        a,b,c,d,e,f,g = crawling(url)
        print("CVS 저장중 ...")
        result = output_csv(savedate, realtime, a, b, c, d, e, f, g)
        print(result)
    else:
        continue