import time
import datetime
from bs4 import BeautifulSoup
import requests
import csv


def crawling(url_):
    source = requests.get(url_).text
    html = BeautifulSoup(source, 'html.parser')
    links = html.select('.volume-header a')
    url_list = []
    num_print = 1
    for link in links:
        text = link.text.replace('.', '-')
        url = 'https://coinmarketcap.com/exchanges/' + text
        url_list.append(url)
    id_num = 0
    all_data = []
    for url in url_list:
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')
        table = soup.find('table')
        names = soup.select('h1.text-large')
        for name in names:
            name = name.text
        data = []
        try:
            for tr in table.find_all('tr'):
                tds = list(tr.find_all('td'))
                for td in tds:
                    data.append(td.text)
        except:
            data=[]
        for i in range(int(len(data) / 7)):
            data_all = data[i * 7:(i + 1) * 7]
            id_num = id_num + 1
            name = name
            currency = data_all[1]
            base = data_all[2].split('/')[0]
            counter = data_all[2].split('/')[1]
            vol_dal = data_all[3].replace('\n', '').replace('$', '').replace(' ', '')
            price = data_all[4].replace('\n', '').replace('$', '').replace(' ', '')
            vol_per = data_all[5]
            date = savedate
            all_data.append([id_num, name, currency, base, counter, vol_dal, price, vol_per, date])
        print("완료 페이지 수 : ",num_print)
        num_print = num_print + 1
    return all_data

def output_csv (all_data):
    with open("Output/" + realtime + ".csv", 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Id'] +
                        ['Name'] +
                        ['Currency'] +
                        ['Base'] +
                        ['Counter'] +
                        ['Volume($)'] +
                        ['Price($)'] +
                        ['Volume(%)'] +
                        ['Date'])
        for i in range(len(all_data)):
            writer.writerow(all_data[i])
    return ("코빗 화이팅ㅎㅎ")



while(1):
    url = "https://coinmarketcap.com/exchanges/volume/24-hour/all/"
    ts = time.time()
    realtime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    savedate = (datetime.date.today() - datetime.timedelta(1)).strftime('%Y-%m-%d')
    savetime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    print("현재시간 : ",savetime)
    time.sleep(1)
    if savetime == "00:19:00":
        print("크롤링 진행중 ...")
        a = crawling(url)
        print(" CSV 저장중 ...")
        result = output_csv(a)
        print(result)
    else:
        continue