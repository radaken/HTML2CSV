import os
import sensetive_vars
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4') #Игнорируем беспонтовые предупреждения 
import re
pattern = re.compile(r'f+e+e+d')

path = sensetive_vars.path

### Закомментировал, чтобы не мешало
# tag = input("Enter tag: ")
# classarg = input("Enter class: ")


### TODO ###
#Описание text-column2 text-page > p
#Документация #tab4 > ul.documentation-list > li [span,a]
#Галлерея card-gallery > img[]



def parse(filedir):
    with open(filedir, encoding="utf8") as filedir:
        soupful = BeautifulSoup(filedir, 'html.parser')

    soup = soupful.find(class_='row card-product-wrap') #Контейнер с карточкой товара, без всей страницы
    try:
    #Старая цена
        for old_price in soup.select('.price > .old-price'):
            print(f"OLD PRICE: {old_price.text}")

    #Цена действительная
        for price in soup.select('.price > span:not(.old-price)'):
            print(f"PRICE: {price.text}")

    #Название товара
        for title in soup.select(".product-desc > h1"):
            print(f"Title: {title.text}")


    #Ищем аттрибуты товаров 
        ul_info = soup.find("ul", class_="info") #Контейнер, в котором хранятся аттрибуты
        li_counter = 0 #Счётчик для аттрибутов (в будущем группировать можно)
        for li in ul_info.find_all("li"):
            li_counter += 1
            print(f'ATT{li_counter}_NAME: {li.find("span", class_="item1").text}') #Название аттрибута
            print(f'ATT{li_counter}_VAL: {li.find("span", class_="item2").text}')   #Значение аттрибута
        li_counter = 0
    except:
        print("Error")

for root, dirs, files in os.walk(path):
    for file in files:
        if(file.endswith(".htm")):
            if (re.search(pattern, path)): #TODO: Not working. Needs to ignore /feed/ directory. I know! I need to add /additional/path/to/file to /original/path
                continue
                print(f'RegExp on feed worked!')
            print(os.path.join(root,file))
            parse(os.path.join(root,file))
            input()