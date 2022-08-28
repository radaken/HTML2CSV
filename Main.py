from ctypes.wintypes import MSG
from email import message
import logging
from multiprocessing import Value
from pyexpat import native_encoding
import string
from typing import Dict, Text
from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup
import lxml
import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#Задаем переменную бота для обращения в телегу по токену / Create token
TOKEN = None #Обозначаем токен / Denote token
with open("C:/Users/applm/OneDrive/Рабочий стол/project BOT/TOKEN.txt") as f:  #Открываем файл с токеном / Open file with token
    TOKEN = f.read().strip() #Считываем токен и удаляем лишнее / Read and delete excess

bot = Bot (TOKEN) #Присваиваем токен / Assigning a token

#Словарь для парсинга / Dictionary for parse
news_dict = {}

#Dp = диспетчер для комманд / Dispatcherfor command
dp = Dispatcher (bot)

#Возврат из под клавы / Return keyboard
catsMain = KeyboardButton ('Главное меню') 

#Клава / Keyboard
news_key = KeyboardButton('Получить свежачок') #Создаем кнопку / Create button
cats = KeyboardButton("Получить китика <3") #Создаем кнопку / Create button
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(news_key,cats) #Выводи клавиатуру с кнопками / Output keyboard with buttons

#Подклава для китиков / Sub keyboard for kitty
cats_animation = KeyboardButton('Флексящий китик') #Создаем кнопку / Create button
cats_picture = KeyboardButton('Статичный китик') #Создаем кнопку / Create button
catsMenu = ReplyKeyboardMarkup (resize_keyboard=True).add(cats_animation,cats_picture,mainMenu) #Возвращаемся из под клавы в глав клаву / Return main keyboard from sub keyborad

#Сообщение в CMD о старте / Message about start in CMD
async def on_startup (_): #Задаем функцию / Setting the function
    print ("МУЗЫКА ПОШЛА") #Вывод сообщения / Output message

#Комманда старта / Command start
@dp.message_handler (commands = ["start"]) #Задаем комманду / Setting the command
async def start  (message: types.Message): #Задаем функцию / Setting the function
    await bot.send_message( message.from_user.id, 'YEP начинаем',reply_markup = mainMenu) #Отправляем приветствие / Send hello
    await bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEFiWli9TsP9B1BLa8HrEqL51EtH4UQEAACnhYAArpIyUtcjAeK6Rs_SykE") #Отправляем стикер / Send sticker

#Парсер с выводом / Parse with output
@dp.message_handler () #Задаем комманду / Setting the command
async def news (message: types.Message): #Задаем функцию / Setting the function
    if message.text == "Получить свежачок": #Задаем условие / Setting condition
        url = ("https://www.cybersport.ru/tags/dota-2") #Обозначаем URL / Denote URL
        r = requests.get (url=url) #Делаем запрос / Request 
        soup = BeautifulSoup (r.text, "lxml") #"Хранилище" запроса / "Storage" request 
        rounded_block = soup.find_all (class_="rounded-block root_d51Rr with-hover no-padding no-margin") #Обращаемся в нужный класс с новостями / Turn to the right class with the news
        for round in rounded_block: #Делаем цики для парсинга всех новостей / Сreate loop for parse all news
            round_title = round.find (class_="title_nSS03").text #Парсим заголовок новости / Parse news title 
            round_data = round.find (class_="pub_AKjdn").text #Парсим время + дату новости / Parse time + data news
            round_link = round.find (class_="link_CocWY") #Парсим ссылку новости / Parse link news
            round_url = f'https://www.cybersport.ru{round_link.get("href")}' #Парсим ссылку новости / Parse link news
            print (round_data,round_title,round_url) #Проверка результата / Checking the results 
            #round_id = round_url.split("/")[-1] #Убираем лишнее с id (ключи словаря) / Removing the excess from the id
            news_dict [round_data] = { #Добавляем в словарь все спаршенное (ключи = время) / Adding everything to the dictionary (keys = time)
                "time": round_data, #Время новости / Link time
                "title": round_title, #Заголовок новости / Link title
                "url": round_url #Ссылка на новость / Link news
            }
        with open ("news_dict.json","w",encoding='utf-8') as file: #Сохраняем все в json файл с переводом в русский / Save everything in json file with translate in russian 
            json.dump(news_dict, file, indent=4, ensure_ascii=False) #Сохраняем все в json файл / Save everything in json file

            
#Вывод словаря с новостями / Output dictionary with news   
    for k,v in sorted(news_dict.items()): #Цикл вывода новостей в тг / Loop output news in telegram
        news = f"{v['time']}\n"\
            f"{v['title']}\n"\
            f"{v['url']}"
        await message.answer(news) #Отправка новостей в чат / Sending news in a chat

#Проверка новинок
#async def check_news ():
    #with open ("news_dict.json")as file:
       # news_list = json.load(file)
   # for round_id in news_dict :
       # round_title = round.find (class_="title_nSS03").text
       # round_data = round.find (class_="pub_AKjdn").text
       # round_link = round.find (class_="link_CocWY")
       # round_url = f'https://www.cybersport.ru/tags/dota-2{round_link.get("href")}'
       # round_id = round_url.split("/")[-1]
       # if round_id in news_dict:
          #  continue
        #else:
            #round_link = round.find (class_="link_CocWY")
           # round_url = f'https://www.cybersport.ru/tags/dota-2{round_link.get("href")}'
            #news_dict [round_id] = {
                #"time": round_data,
                #"title": round_title,
                #"url": round_url
           # }
        
#обработка нажатий клавиатуры

   # elif message.text == "Получить китика <3":
        #await bot.send_message (message.from_user.id, reply_markup = nav.catsMain )
       # if message.text == "Флексящий китик":
            #await bot.send_sticker (message.from_user.id, "CAACAgIAAxkBAAEFiWli9TsP9B1BLa8HrEqL51EtH4UQEAACnhYAArpIyUtcjAeK6Rs_SykE")
       # elif message.text == "Статичный китик":
           # await bot.send_sticker (message.from_user.id, "AACAgIAAxkBAAEFpPJjA8uPbkgZzlwBZWPQ7UuKh7HvfgAC_AwAAmn2CUunISFcu6AR3ykE")
    #elif message.text == "mainMenu":
        #await bot.send_message (message.from_user.id,??? )
#обработка нажатий клавиатуры

#Запуск бота / Start bot     
if __name__ == "__main__": #Условие запуска / Condition for start
    executor.start_polling (dp, skip_updates=True, on_startup=on_startup) #Пропуск обновлений / Skip update 
