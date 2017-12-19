import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import xlsxwriter

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

def output_ex(savedate,
              realtime,
              coin_list,
              base_list ,
              counter_list,
              price_list ,
              percent_list,
              rAlign_list,
              cropto_list):
    workbook = xlsxwriter.Workbook('./Output/'+savedate+'.xlsx')
    time.sleep(0.1)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 20)
    worksheet.set_column('F:F', 20)
    worksheet.set_column('G:G', 20)
    worksheet.set_column('H:H', 20)
    time.sleep(0.1)
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', '날짜', bold)
    worksheet.write('B1', '코인명', bold)
    worksheet.write('C1', 'Base', bold)
    worksheet.write('D1', 'Counter', bold)
    worksheet.write('E1', '현재가(Crypto)', bold)
    worksheet.write('F1', '현재가(KRW)', bold)
    worksheet.write('G1', '전일대비', bold)
    worksheet.write('H1', '거래대금', bold)
    time.sleep(0.1)
    for num in range(len(coin_list)):
        i = num+1
        worksheet.write(i, 0, realtime)
        worksheet.write(i, 1, coin_list[num])
        worksheet.write(i, 2, base_list[num])
        worksheet.write(i, 3, counter_list[num])
        worksheet.write(i, 5, price_list[num])
        worksheet.write(i, 6, percent_list[num])
        worksheet.write(i, 7, rAlign_list[num])
        time.sleep(0.05)
    num_cro = len(price_list)-len(cropto_list)
    for num in range(len(cropto_list)):
        num_cro = num_cro+1
        worksheet.write(num_cro, 4, cropto_list[num])
        time.sleep(0.05)
    return("Save Complete")


while(1):
    url = "https://www.upbit.com/exchange?code=CRIX.UPBIT.KRW-BTC"
    ts = time.time()
    realtime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    savedate = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    savetime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    print("현재시간 : ",savetime)
    time.sleep(1)
    if savetime == "00:00:40":
        print("크롤링 진행중 ...")
        a,b,c,d,e,f,g = crawling(url)
        print("엑셀 저장중 ...")
        result = output_ex(savedate, realtime, a, b, c, d, e, f, g)
        print(result)
    else:
        continue