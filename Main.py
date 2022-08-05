from ast import parse
from email import header, message
import logging
from pydoc import describe
from tkinter import image_types
from turtle import title
from typing import Literal
from aiogram import Bot, Dispatcher, executor, types
import os
import requests
from bs4 import BeautifulSoup
import time
import lxml

#задаем переменную бота для обращения в телегу по токену
bot = Bot (token = "5517148105:AAEcSNGxe_-wYCWCotJe87dsfuG8nPT8dNY")

#dp = диспетчер для комманд
dp = Dispatcher (bot)

#бот в CMD сообщает о старте
async def on_startup (_):
    print ("МУЗЫКА ПОШЛА")
    print ("ЕБКА ПОШЛА")

#Стандартные комманды
@dp.message_handler (commands = ["start","help,news"])
async def start(message: types.Message):
        await message.answer ("YEP начинаем")
        
async def help(message: types.Message):
    await message.answer ("Шо опять? Шо случилось?")

#парсинг новостей
url = ("https://www.cybersport.ru/tags/dota-2")
r = requests.get (url)
soup = BeautifulSoup (r.text, "lxml")
rounded_block = soup.find_all (class_="container_qPDo5")
for round in rounded_block:
    round_title = round.find ( class_="title_nSS03") 
    round_data = round.find (class_="pub_AKjdn")
    round_url = f'https://www.cybersport.ru/tags/dota-2 {round.find ("a")}'
    print(round_data,round_title,round_url)

#запуск бота    
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)