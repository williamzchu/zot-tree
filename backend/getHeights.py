import json

f = open("prereqs.json", 'r')
s = json.load(f)

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

o = open('cs_prereqs.json', 'w')
json.dump(result, o)