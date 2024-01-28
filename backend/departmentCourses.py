import requests
from bs4 import BeautifulSoup
import json
import re

result = requests.get("https://catalogue.uci.edu/schoolsandprograms/")

soup = BeautifulSoup(result.content, "html.parser")

htmls = soup.find_all("h4")


departmentCourses = {}
for i in htmls:
    departmenturl = 'https://catalogue.uci.edu/' + i.find('a')['href'] + "/#courseinventory"
    departmentresult = requests.get(departmenturl)

    departmentsoup = BeautifulSoup(departmentresult.content, 'html.parser')
    print(departmenturl)
    for i in departmentsoup.find_all('strong'):
        text = i.text
        if ("Unit" in text and '.' in text):
            j = text.index('.')

            splitted = text[0:j].split()
            depart = ""
            for k in range(0, len(splitted)-1):
                depart += splitted[k]
            
            if depart not in departmentCourses:
                departmentCourses[depart] = []
            departmentCourses[depart].append(splitted[-1])

f = open("departmentCourses.json", 'w')

f.write(json.dumps(departmentCourses))