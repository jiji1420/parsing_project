import csv
import requests
from bs4 import BeautifulSoup

def get_html(url):
    response = requests.get(url)
    return response.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages_ul = soup.find('div', class_='pager-wrap').find('ul',class_='pagination').find_all('li')
    last_page = pages_ul[-1]
    total_pages = last_page.find('a').get('href').split('=')[-1]
    return(int(total_pages))

def write_to_csv(data):
    with open('kivano_phone.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow((data['title'],
                         data['price'],
                         data['photo'])) 
          
def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find_all('div', class_='item')
    
    for product in product_list:
        photo = 'https://www.kivano.kg' + product.find('div',class_='listbox_img').find('a').find('img').get('src')
        title = product.find('div', class_= 'listbox_title').find('a').text
        price = product.find('div', class_= 'listbox_price').find('strong').text
      
        data = {'title': title, 'price': price, 'photo': photo}
        write_to_csv(data)


def main():
    phone_url = 'https://www.kivano.kg/mobilnye-telefony'
    pages = '?page='
    
    total_pages = get_total_pages(get_html(phone_url))
    
    for page in range(1, total_pages+1):
        url_with_page = phone_url + pages + str(page)
        html = get_html(url_with_page)
        get_page_data(html)

main()

