import requests
from bs4 import BeautifulSoup as BS
import csv

def get_html(BASE_URL):
    response = requests.get(BASE_URL)
    return response.text

def get_total_pages(html):
    soup = BS(html, 'lxml')
    pages = soup.find('ul', class_="pagination")
    page = pages.find_all('li')[-1]
    total_page = page.find('a').get('href').split('=')[-1]
    return int(total_page)

def get_data(html):
    soup = BS(html, 'lxml')
    specsearsh = soup.select('div[class^="list-item list-label"]')
    for car in specsearsh:
        if specsearsh != None:
            title = car.find('h2', class_='name').text.strip()
            
            price_dollar = car.find('p', class_='price').find('strong').text
            del_ = price_dollar.replace(' ', '')
            price_som = int(del_.replace('$', '')) * 84

            
            price = f'$ {price_dollar} ({price_som} сом)'
            try:
                image = car.find('div', class_ = 'thumb-item-carousel').find('img', class_ = 'lazy-image').get('data-src')
            except AttributeError:
                image = 'Нет фото'
            
            try:
                year = car.find('p', class_="year-miles").find('span').text.strip()
            
            except ArithmeticError:
                year = None
            
            try:
                toplivo = car.find('p', class_="body-type").text.strip()
            
            except ArithmeticError:
                toplivo = None
            
            try:
                rule = car.find('p', class_="volume").text.strip()
            
            except ArithmeticError:
                
                rule = None
            
            description =f'{year}/{toplivo}/{rule}'
            
            write_csv({
                'title': title,
                'image': image,
                'price': price,
                'description': description
            })

        # print(price)

def write_csv(data):
    with open('cars.csv', 'a') as file:
        name = ['title', 'price', 'description', 'image']
        write = csv.DictWriter(file, delimiter=',', fieldnames=name)
        write.writerow(data)

def main():

    BASE_URL = 'https://www.mashina.kg/specsearch/all/'
    page = '?page='
    
    total_page = get_total_pages(get_html(BASE_URL))
    
    for i in range(1, total_page+1):
        url_page = BASE_URL + page + str(i)
        html = get_html(url_page)
        get_data(html)

main()

