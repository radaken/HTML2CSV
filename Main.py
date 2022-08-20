from cgitb import text
from ctypes.wintypes import MSG
from email import message, message_from_string
import logging
import string
from typing import Dict, Text
from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup
import lxml
import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#задаем переменную бота для обращения в телегу по токену
TOKEN = None
with open("C:/Users/applm/OneDrive/Рабочий стол/project BOT/TOKEN.txt") as f:
    TOKEN = f.read().strip()

bot = Bot (TOKEN)

#Словарь для парсинга
news_dict = {}

#dp = диспетчер для комманд
dp = Dispatcher (bot)

#возврат из под клавы
catsMain = KeyboardButton ('Главное меню')

#клава
news_key = KeyboardButton('Получить свежачок')
cats = KeyboardButton("Получить китика <3")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(news_key,cats)

#под клава для китиков
cats_animation = KeyboardButton('Флексящий китик')
cats_picture = KeyboardButton('Статичный китик')
catsMenu = ReplyKeyboardMarkup (resize_keyboard=True).add(cats_animation,cats_picture,catsMain)

#сообщение в CMD о старте
async def on_startup (_):
    print ("МУЗЫКА ПОШЛА")

#Стандартные комманды
@dp.message_handler (commands = ["start"])
async def start  (message: types.Message):
    await bot.send_message( message.from_user.id, 'YEP начинаем',reply_markup = mainMenu)
    await bot.send_sticker(message.chat.id,"CAACAgIAAxkBAAEFiWli9TsP9B1BLa8HrEqL51EtH4UQEAACnhYAArpIyUtcjAeK6Rs_SykE")

#парсер с выводом

#@dp.message_handler (commands = ['Получить свежачок'])
async def news (message: types.Message):
    url = ("https://www.cybersport.ru/tags/dota-2")
    r = requests.get (url)
    soup = BeautifulSoup (r.text, "lxml")
    rounded_block = soup.find_all (class_="container_qPDo5")
    for round in rounded_block:
        round_title = round.find ( class_="title_nSS03").text   
        round_data = round.find (class_="pub_AKjdn").text
        round_url = f'https://www.cybersport.ru/tags/dota-2{round.find_all("href")}'
        print (round_data,round_title,round_url)
        news_dict = {
            "time": round_data,
            "title": round_title,
            "url": round_url
            }

    with open ("news_dict.json","w",encoding='utf-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

#@dp.message_handler (commands = ['Получить китика <3'])
async def kitik (message:types.Message):
    await bot.send_sticker (message.from_user.id, "CAACAgIAAxkBAAEFiWli9TsP9B1BLa8HrEqL51EtH4UQEAACnhYAArpIyUtcjAeK6Rs_SykE")

#обработка нажатий клавиатуры
async def registor_client (dp: Dispatcher):
    dp.register_message_handler (kitik, commands=['Получить китика <3'])
    dp.register_message_handler (news, commands=['Получить свежачок'])

#запуск бота    
if __name__ == "__main__":
    executor.start_polling (dp, skip_updates=True, on_startup=on_startup)
