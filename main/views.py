from django.shortcuts import render
from requests import request as req
from bs4 import BeautifulSoup
from requests import  request


def queryset(**kwargs):

    return dict(kwargs)


def search_media(key, page=1):
    key = key.replace(' ', '+')
    page1 = request('GET', f'https://mediapark.uz/site/search?text={key}&page={page}').text

    soup = BeautifulSoup(page1, 'lxml')

    products = soup.find_all('div', {'class': 'products'})
    qs = []
    for item in products:
        title = item.find('img', {'class': 'img-responsive'})['alt'].replace('Смартфон ', '')
        img = 'https://mediapark.uz' + item.find('img', {'class': 'img-responsive'})['src']
        old_price = item.find('span', {'class': 'old-price'}).contents[0].replace('Старая цена: ', '')
        price = item.find('span', {'class': 'price'}).contents[0].replace('Цена: ', '')
        month_price = item.find('span', {'class': 'permonth-price'}).contents[1].contents[0]
        url = 'https://mediapark.uz' + item.find('img', {'class': 'img-responsive'}).parent['href']

        qs.append(queryset(title=title, img=img, old_price=old_price, month_price=month_price, price=price, url=url))
    return qs


def search_tex(key):
    key = key.replace(' ', '+')
    page1 = req('GET', f'https://texnomart.uz/ru/product/search?category=&key={key}').text

    soup1 = BeautifulSoup(page1, 'lxml')

    products = soup1.find_all('div', {'class': 'product-list__item'})
    qs = []
    for item in products:
        title = item.find('a', {'class': 'product-name'})['title']
        url = 'https://texnomart.uz'+item.find('a', {'class': 'product-name'})['href']
        img = 'https://texnomart.uz' + item.find('img', {'class': 'product-img'})['data-src']
        old_price = item.find('span', {'class': 'discount-del-label'})
        price = item.find('div', {'class': 'product-price'}).findAll('div')[1].contents[0]
        month_price = item.find('div', {'class': 'product-installment'}).contents[0]

        qs.append(queryset(title=title, img=img, old_price=old_price, month_price=month_price, price=price, url=url))

    return qs


def search_olx(key, page=1):

    key = key.replace(' ', '-')
    html = request('GET', f'https://www.olx.uz/list/q-{key}/?page={page}').text

    soup = BeautifulSoup(html, 'lxml')

    products = soup.find_all('tr', {'class': 'wrap'})
    qs = []
    for item in products:
        try:
            title = item.find('img', {'class': 'fleft'})['alt']
            img = item.find('img', {'class': 'fleft'})['src']
            url = item.find('a', {'class': 'detailsLink'})['href']
            price = item.find('p', {'class': 'price'}).contents[1].contents[0]
            qs.append(queryset(title=title, img=img, url=url, price=price))
        except:
            pass
    return qs


def index(request):

    if request.GET:
        key = request.GET.get('search')
        media = search_media(key)
        texno = search_tex(key)
        olx = search_olx(key)
        products = media + olx + texno
        # products = texno
    else:
        products = []

    context = {
        'products': products
    }

    return render(request, 'index.html', context)
