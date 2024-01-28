import json
import requests

department = "Engineering"
degree = "Computer Science and Engineering, B.S."
f = open("degreeCourses.json", 'r')
s = json.load(f)[department]


courses = {}
def recurse(course):
    if course not in courses:
        print(course)
        response = requests.get("https://api-next.peterportal.org/v1/rest/courses/" + course)
        if(response.status_code == 200):
            d = json.loads(response.text)
            courses[course] = []
            for x in d["payload"]["prerequisiteList"]:
                courses[course].append(x.replace(' ', ''))
            for c in d["payload"]["prerequisiteList"]:
                recurse(c.replace(' ', ''))
        else:
            courses[course] = []

for x in s:
    if (x[0] == degree):
        print(x)
        for course in x[2]:
            if course not in courses:
                recurse(course)


s = courses

heights = {}

def recurse(course):
    if course not in heights:
        if len(s[course]) == 0:
            heights[course] = 0
            return 0
        else:
            h = 0
            for c in s[course]:
                h = max(recurse(c) + 1, h)
            heights[course] = h
            return h
    return heights[course]

for course in s:
    recurse(course)

result = {}
for course in heights:
    result[course] = {'height': heights[course], 'prereqs': s[course]}
print(result)
f = open("mathminor_prereqs.json", 'w')
f.write(json.dumps(result))