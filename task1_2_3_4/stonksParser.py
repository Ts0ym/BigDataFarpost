import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import datetime
import json
import os

# Заголовок для запросов
headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/91.0.4472.124 Safari/537.36')
}

class Company:
    def __init__(self, name, ticker, price_rub, PE, year_stonks, year_result_percent):
        self.name = name
        self.ticker = ticker
        self.price_rub = price_rub
        self.PE = PE
        self.year_stonks = year_stonks
        self.year_result_percent = year_result_percent

companies = []

# Обрабатываем 2 страницы индекса
for i in range(2):
    page_num = i + 1
    url = f'https://markets.businessinsider.com/index/components/s&p_500?p={page_num}'
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime('%d/%m/%Y')
    cb_url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={formatted_date}'
    cb_request = requests.get(cb_url)
    
    # Парсинг XML для получения курса USD->RUB
    cb_xml = ET.fromstring(cb_request.text)
    for valute in cb_xml.findall('Valute'):
        if valute.find('CharCode').text == 'USD':
            usd_rate = float(valute.find('Value').text.replace(',', '.'))
            break

    stonks_request = requests.get(url, headers=headers)
    stonks_soup = BeautifulSoup(stonks_request.text, 'html.parser')
    companies_table = stonks_soup.find('tbody', class_='table__tbody')
    if not companies_table:
        continue

    # Обработка строк таблицы только для первой страницы (как в оригинале)
    for tr in companies_table.find_all('tr'):
        if page_num == 1:
            tds = tr.find_all('td')
            
            # Извлекаем имя компании
            a_tag = tds[0].find('a')
            name = a_tag.get('title')
            
            # Цена в долларах
            USD_price_str = tds[1].get_text(strip=True, separator=' ')
            first_number = USD_price_str.split()[0]
            USD_price = float(first_number)
            # Конвертация в рубли
            RUB_price = round(USD_price * usd_rate, 2)
            
            # Годовой рост/падение
            year_result_span = tds[-1].find_all('span')
            year_stonks = year_result_span[1].get_text()
            
            # Переход на страницу компании
            link = a_tag.get('href')
            company_request = requests.get(f'https://markets.businessinsider.com/{link}', headers=headers)
            company_soup = BeautifulSoup(company_request.text, 'html.parser')
            
            # Извлекаем тикер
            price_row = company_soup.find('h1', class_='price-section__identifiers')
            price_span = price_row.find('span', class_='price-section__category')
            mmm_span = price_span.find('span')
            ticker = mmm_span.text[2:]
            
            # Извлекаем P/E
            snapshots = company_soup.find_all('div', class_='snapshot__data-item padding-right--zero')
            PE_snapshot = snapshots[14].get_text(strip=True)
            PE_metric = PE_snapshot[:-9]
            
            # Извлекаем 52 Week Low
            snapshot_small = company_soup.find('div', class_='snapshot__data-item snapshot__data-item--small')
            year_week_low_snapshot = snapshot_small.get_text(strip=True)
            year_week_low = year_week_low_snapshot[:-8]
            
            # Извлекаем 52 Week High
            snapshot_big = company_soup.find('div', class_='snapshot__data-item snapshot__data-item--small snapshot__data-item--right')
            year_week_high_snapshot = snapshot_big.get_text(strip=True)
            year_week_high = year_week_high_snapshot[:-9]
            
            # Вычисляем потенциальную прибыль в процентах
            year_result_percent = round((1 - (float(year_week_low) / float(year_week_high))) * 100, 2)
            
            companies.append(Company(
                name=name,
                ticker=ticker,
                price_rub=RUB_price,
                PE=PE_metric,
                year_stonks=year_stonks,
                year_result_percent=year_result_percent
            ))

# Сортировки по разным критериям
top_price = sorted(companies, key=lambda x: x.price_rub, reverse=True)[:10]
top_pe = sorted([c for c in companies if c.PE != float('inf')], key=lambda x: x.PE, reverse=True)[:10]
top_growth = sorted(companies, key=lambda x: x.year_stonks, reverse=True)[:10]
top_profit = sorted(companies, key=lambda x: x.year_result_percent, reverse=True)[:10]

def create_json(data, key):
    # Сопоставление ключей с атрибутами объекта Company
    attr_map = {
        "price": "price_rub",
        "P/E": "PE",
        "growth": "year_stonks",
        "potential profit": "year_result_percent"
    }
    return [
        {
            "code": item.ticker,
            "name": item.name,
            key: getattr(item, attr_map[key])
        } for item in data
    ]

# Создаем папку для сохранения результатов, если её нет
os.makedirs("results", exist_ok=True)

# Сохраняем данные в файлы с новыми именами
with open(os.path.join("results", "result_price.json"), 'w', encoding='utf-8') as f:
    json.dump(create_json(top_price, "price"), f, indent=2)

with open(os.path.join("results", "result_pe.json"), 'w', encoding='utf-8') as f:
    json.dump(create_json(top_pe, "P/E"), f, indent=2)

with open(os.path.join("results", "result_growth.json"), 'w', encoding='utf-8') as f:
    json.dump(create_json(top_growth, "growth"), f, indent=2)

with open(os.path.join("results", "result_profit.json"), 'w', encoding='utf-8') as f:
    json.dump(create_json(top_profit, "potential profit"), f, indent=2)
