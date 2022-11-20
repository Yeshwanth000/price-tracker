from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import requests
from bs4 import BeautifulSoup

TEMPLATES_DIRS =(
    'os.path.join(BASE_DIR,"templates"),'
)

def home(request):
    return render(request,'home.html')

# def index(request):
#     #return HttpResponse("<h1>Hello world<h1>")
#     return render(request,'index.html')

def about(request):
    return render(request, 'about.html')

def index(response):
    #p = response.GET.get('search')
    url =response.GET.get('search')
    items={}
    items_1={}
    ti=''
    pr=''
    amz = 'https://www.amazon.in/s?k='+url.replace(' ','+')
    page = requests.get(amz ,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"})#for not getting captcha 
    soup = BeautifulSoup(page.content,'html.parser')
    links = soup.find_all('a',class_="a-link-normal s-no-outline")
    for i in range(len(links)):
        try:
            org_link = 'https://amazon.in'+links[i].get('href')
            page = requests.get(org_link ,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"})#for not getting captcha 
            soup = BeautifulSoup(page.content,'html.parser')
            ti = soup.find('span',id="productTitle").get_text().strip()
            pr = int(soup.find('span',class_="a-price-whole").get_text().replace(',','').replace('.','').strip())
            if url.lower() in ti.lower():
                items[ti] = pr
            else:
                items_1[ti] = pr
        except Exception:
            continue
        if len(items) == 1:
            break
        if i > len(links)//2:
            break


    flip = 'https://www.flipkart.com/search?q='+url.replace('+','%20')
    page = requests.get(flip ,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"})#for not getting captcha 
    soup = BeautifulSoup(page.content,'html.parser')
    links = soup.find_all('a') #soup.select("_30jeq3")[0].getText()
    for link in links:
        t = link.get('href')
        try:
            org_link = 'https://www.flipkart.com' + t
            page = requests.get(org_link ,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"})#for not getting captcha 
            soup = BeautifulSoup(page.content,'html.parser')
            ti1 = soup.find('span',class_='B_NuCI').get_text().replace('\xa0','')
            pr1 = int(soup.find('div',class_='_30jeq3 _16Jk6d').get_text()[1:].replace(',',''))
            if url.replace(' ','-') in t:
                items[ti1] = pr1
            else:
                items_1[ti1] = pr1
        except Exception:
            continue
        if len(items) == 1:
            break
    return render(response,'result.html',{"title":ti,"price":pr,"title1":ti1,"price1":pr1})


