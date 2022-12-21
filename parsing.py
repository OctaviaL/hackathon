import requests
from bs4 import BeautifulSoup as BS
import csv

def get_html(BASE_URL):
    response = requests.get(BASE_URL)
    soup = BS(response.text, 'lxml')
    specsearsh = soup.select('div[class^="list-item list-label"]')
    for car in specsearsh:
        if specsearsh != None:
            title = car.find('h2', class_='name').text.strip()
            
            price_dollar = car.find('p', class_='price').find('strong').text
            del_ = price_dollar.replace(' ', '')
            price_som = int(del_.replace('$', '')) * 84

            
            price = f'$ {price_dollar} ({price_som} сом)'
            
            try:
                image = car.find('div', class_='thumb-item-carousel').find('img', class_="lazy-image").get('data-src')
            
            except ArithmeticError:

                image = None
            
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

# def get_total_pages(soup):
#     pages = soup.find('ul', class_="pagination")
#     page = pages.find_all('li')[-1]
#     total_page = page.find('a').get('href').split('=')[-1]
#     return int(total_page)


BASE_URL = 'https://www.mashina.kg/specsearch/all/?page=1'
# page = '?page='
for i in BASE_URL:
    if 'page=1' in i:
        get_html(BASE_URL)
    else:
        url2 = 'https://www.mashina.kg/commercialsearch/all/'
        i = 1
        url2 += '?page=' + str(i)
        i += 1
        get_html(url2)
        if i == 25:
            break
    
    # for i in range(1, total_pages+1):
    #     url_page = BASE_URL + page + str(i)
