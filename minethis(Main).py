from email import message
from pyexpat import native_encoding
from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup
import lxml
import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import schedule
from aiogram.utils.markdown import hlink


#Задаем переменную бота для обращения в телегу по токену / Create token
TOKEN = None #Обозначаем токен / Denote token
with open("C:/Users/applm/OneDrive/Рабочий стол/Projects/project BOT/TOKEN.txt") as f:  #Открываем файл с токеном / Open file with token
    TOKEN = f.read().strip() #Считываем токен и удаляем лишнее / Read and delete excess

bot = Bot (TOKEN, parse_mode=types.ParseMode.HTML) #Присваиваем токен / Assigning a token


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
@dp.message_handler () 
async def news (message: types.Message):
    if message.text == "Получить свежачок":
        url = ("https://www.cybersport.ru/tags/dota-2")
        r = requests.get (url=url)
        soup = BeautifulSoup (r.text, "lxml")
        rounded_block = soup.find_all (class_="rounded-block root_d51Rr with-hover no-padding no-margin")
        for round in rounded_block:
            round_title = round.find (class_="title_nSS03").text
            round_data = round.find (class_="pub_AKjdn").text
            round_link = round.find (class_="link_CocWY")
            round_url = f'https://www.cybersport.ru{round_link.get("href")}'
            news_dict [round_data] = {
                "time": round_data,
                "title": round_title,
                "url": round_url
            }
        with open ("news_dict.json","w",encoding='utf-8') as file:
            json.dump(news_dict, file, indent=4, ensure_ascii=False)

#Вывоод словаря с новостями / Output dictionary with news   
    for k,v in sorted(news_dict.items()):
        news = f"<b>{v['time']}</b>\n"\
            f"{hlink(v['title'],v['url'])}"
        await message.answer(news)

#Проверка новинокновостей в json c таймером на 30 минут / Check new news to json with timer on 30 seconds
def check_update_news():
    with open ("news_dict.json", encoding='utf-8') as file:
        news_dict = json.load (file)
    url = ("https://www.cybersport.ru/tags/dota-2")
    r = requests.get (url=url)
    soup = BeautifulSoup (r.text, "lxml")
    rounded_block = soup.find_all (class_="rounded-block root_d51Rr with-hover no-padding no-margin")
    fresh_news = {}
    for round in rounded_block:
        round_data = round.find (class_="pub_AKjdn").text
        if round_data in news_dict:
            continue
        else:
            round_title = round.find (class_="title_nSS03").text
            round_data = round.find (class_="pub_AKjdn").text
            round_link = round.find (class_="link_CocWY")
            round_url = f'https://www.cybersport.ru{round_link.get("href")}'
            news_dict [round_data] = {
                "time": round_data,
                "title": round_title,
                "url": round_url
            }
            fresh_news [round_data] = {
                "time": round_data,
                "title": round_title,
                "url": round_url
            }

    with open ("news_dict.json","w",encoding='utf-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
    return fresh_news

# for k,v in sorted(news_dict.items()):
#     news = f"<b>{v['time']}</b>\n"\
#     f"{hlink(v['title'],v['url'])}"
#     await message.answer(news)

#Таймер на 30 минут 
# schedule.every(5).minutes.do(check_update_news)
# while True: 
#     schedule.run_pending()

#Клавиатуры киттиков / Kitty keyboard

#запуск бота  
if __name__ == "__main__":
    executor.start_polling (dp, skip_updates=True, on_startup=on_startup)
