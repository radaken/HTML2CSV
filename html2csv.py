import os
import sensetive_vars
from bs4 import BeautifulSoup

path = sensetive_vars.path

tag = input("Enter tag: ")
classarg = input("Enter class: ")

def parse(filedir, tag, classarg):
    with open(filedir, encoding="utf8") as filedir:
        soup = BeautifulSoup(filedir, 'html.parser')
    for tags in soup.find_all(tag, {'class' : classarg}):
        print(tags)

for root, dirs, files in os.walk(path):
    for file in files:
        if(file.endswith(".htm")):
            print(os.path.join(root,file))
            parse(os.path.join(root,file), tag, classarg)
            input()