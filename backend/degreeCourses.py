import requests
from bs4 import BeautifulSoup
import json
import re

URL = "https://catalogue.uci.edu/undergraduatedegrees/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("div", id="textcontainer")

r = str(results).split("\n")[228:]

d = open("departmentCourses.json", 'r')
departmentCourses = json.load(d)
#print(departmentCourses)

degreeCourses = {}
curr = None
for h in r:
    s = BeautifulSoup(h, "html.parser")
    
    cleaned = s.getText()
    if (len(cleaned) < 3):
        continue

    if "," not in cleaned:
        curr = cleaned

    else:
        if curr not in degreeCourses:
            degreeCourses[curr] = []
        degreeCourses[curr].append([cleaned, "https://catalogue.uci.edu" + s.find('a')['href'] + "/#requirementstext"])

#f = open("degreeCourses.json", "w")
#f.write(json.dumps(degreeCourses))
        
def lerpcourse(a, b, department):
    if (department not in departmentCourses):
        #print(department)
        return []
    if (len(b) == 0):
        return [a]
    
    if (not re.match(r'[0-9]+[A-Z]*', a) or not re.match(r'[0-9]+[A-Z]*', b)):
        #print(a, b)
        return []
    #print(a, "+",b, department)
    results = []
    
    start = 0
    anum = ''.join(filter(str.isdigit, a))
    for num in departmentCourses[department]:
        curr = ''.join(filter(str.isdigit, num))
        if (int(anum) <= int(curr)):
            break
        start+=1

    end = 0
    enum = ''.join(filter(str.isdigit, b))

    for num in departmentCourses[department]:
        curr = ''.join(filter(str.isdigit, num))

        if (int(enum) < int(curr)):
            break
        end+=1
    end -= 1

    for i in range(start, end + 1):
        results.append(departmentCourses[department][i])

    return results

#print(lerpcourse("11", "132", "ART"))

for department in degreeCourses:
    for degree in degreeCourses[department]:
        print(degree)
        #if (degree[0] != 'Drama, B.A.'):
        #    continue
        degreePage = requests.get(degree[1])
        degreeSoup = BeautifulSoup(degreePage.content, "html.parser")
        courses = None
        try:
            courses = degreeSoup.findAll('table', class_="sc_courselist")[0]
        except IndexError:
            degree.append([])
            continue

        classes = set()
        for c in courses.find_all('tr'):
        
            departmentName = ""
            nums = False
            for word in c.text.split():
                word = word.replace('–', '-')
                word = word.replace(',', '')
                if '.' not in word and "(" not in word and  ")" not in word and not any(x.isdigit() for x in word) and word.isupper():
                    if nums:
                        departmentName = word
                    else:
                        departmentName += word
                    nums = False
                elif departmentName != "" and re.match(r'[0-9]+[A-Z]*', word):
                    nums = True
                    if ('-' in word):
                        words = word.split('-')
                        interpolated= lerpcourse(words[0], words[1], departmentName)
                        if len(interpolated) == 0:
                            nums = False
                        for n in interpolated:
                            #print(words[0], words[1], lerpcourse(words[0], words[1], departmentName))
                            classes.add(departmentName + n)
                            
                    else:
                        classes.add(departmentName + word)
                        continue
    

                #print(departmentName)
        degree.append(sorted(list(classes)))
        print(degree[2])
        #break
    #break

f = open("degreeCourses.json", 'w')
f.write(json.dumps(degreeCourses))
