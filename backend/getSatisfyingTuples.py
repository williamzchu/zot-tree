import json

f = open('compsci.json', 'r')
s = json.load(f)


for x in s["Computer Science, B.S."]['COMPSCI112']['prerequisiteTree']:
    print(x)