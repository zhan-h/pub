from concurrent.futures import ThreadPoolExecutor
from django.shortcuts import render
import requests
from .models import Zycwz
from lxml import etree


def get_data(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    url = 'https://www.zyctd.com/jiage/1-0-0-{}.html'.format(page)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    selector = etree.HTML(response.text)
    name_list = selector.xpath('//table/tbody/tr/td[1]/a/text()')
    size_list = selector.xpath('//table/tbody/tr/td[2]/a/@title')
    price_list = selector.xpath('//table/tbody/tr/td[4]/text()')
    wook_list = selector.xpath('//table/tbody/tr/td[6]/text()')
    for name, size, price, wook in zip(name_list, size_list, price_list, wook_list):
        if not Zycwz.objects.filter(zy_name=name, zy_profession=size, zy_price=float(price.strip().replace('%', '')),
                                    zy_work=float(wook.strip().replace('%', ''))).exists():
            run_zy = Zycwz(zy_name=name, zy_profession=size, zy_price=float(price.strip().replace('%', '')),
                           zy_work=float(wook.strip().replace('%', '')))
            run_zy.save()


# Create your views here.

def index(request):
    if request.method == 'POST':
        def main():
            max_pages = 133
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(get_data, range(1, max_pages + 1))

        main()
        data = Zycwz.objects.all()
        datas = []
        for i in data:
            datas.append([i.zy_work, i.zy_price])
        return render(request, 'index.html', {'data': data, 'datas': datas})
    data = Zycwz.objects.all()
    datas = []
    for i in data:
        if i.zy_work != 0 and i.zy_price < 500:
            datas.append([i.zy_work, i.zy_price])
    return render(request, 'index.html', {'data': data, 'datas': datas})
