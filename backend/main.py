"""
app.py

This one file is all you need to start off with your FastAPI server!
"""

from typing import Optional

import uvicorn
from fastapi import FastAPI, status
import requests
from fastapi.middleware.cors import CORSMiddleware
import json


# Initializing and setting configurations for your FastAPI application is one
# of the first things you should do in your code.
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

file = open('../degreeCourses.json')
degree_courses = json.load(file)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{degree}")
def get_degree(degree: str):
    try:
        f = open(degree + ".json", 'r')
        s = json.load(f)
        return s
    except (FileNotFoundError):
        return {"Degree not Found": []}

@app.get("/courses/{course_id}")
def get_course(course_id: str):
    # gets the course info given its course id
    res = requests.get(f"https://api-next.peterportal.org/v1/rest/courses/{course_id}")
    return res.json()

@app.get("/courses/prereq/{course_id}")
def get_course_prereq(course_id: str):
    # gets the pre req tree for a course if it exists
    res = get_course(course_id)
    if res['statusCode'] == 200:
        return res['payload']['prerequisiteTree']
    else:
        # no info abt the course was found
        return {}

@app.get("/courses/complete-prereq/{course_id}")
def get_complete_preq(course_id:str, seen_courses={}):
    # gets the complete pre req tree for a certain course
    if course_id in seen_courses.keys():
        return {'completeTree': seen_courses[course_id]['prerequisiteTree'], 'height': seen_courses[course_id]['height']}
    else:
        tree = get_course_prereq(course_id)
        return process_tree(tree, seen_courses)

def process_tree(tree: dict, seen_courses={}):
    # helper to create the complete pre req tree for a course
    # recurses down to build entire tree
    complete_tree = {'completeTree': {}, 'height': 0}
    if 'height' in tree.keys():
        complete_tree['height'] = tree['height']
    if 'OR' in tree.keys():
        complete_tree['completeTree']['OR'] = []
        heights = [0]
        for or_course in tree['OR']:
            if 'AND' in or_course.keys():
                process = process_tree(or_course, seen_courses)
                tree = process['completeTree']
                height = process['height']
                heights.append(height)
                complete_tree['completeTree']['OR'].append(tree)
            else:
                if 'courseId' in or_course.keys():
                    or_course_id = or_course['courseId'].replace(" ", "")
                    if or_course_id in seen_courses:
                        or_course = {'courseId': or_course_id, "prerequisiteTree": seen_courses[or_course_id]['prerequisiteTree'], "height": seen_courses[or_course_id]['height']}
                    else:
                        or_course_tree = get_complete_preq(or_course_id, seen_courses)
                        or_course = {'courseId': or_course_id, "prerequisiteTree": or_course_tree['completeTree'], "height": or_course_tree['height']}
                        seen_courses[or_course_id] = {"prerequisiteTree": or_course['prerequisiteTree'], "height": or_course_tree['height']}
                        heights.append(or_course_tree['height'])
                    complete_tree['completeTree']['OR'].append(or_course)
        complete_tree['height'] += (max(heights)+1)
        if complete_tree['completeTree']['OR'] == [] or complete_tree['completeTree']['OR'] == [{}]:
            complete_tree['completeTree'] = {}
        if complete_tree['completeTree'] == {}:
            complete_tree['height'] = 0
    if 'AND' in tree.keys():
        complete_tree['completeTree']['AND'] = []
        heights= [0]
        for and_course in tree['AND']:
            if 'OR' in and_course.keys():
                process = process_tree(and_course, seen_courses)
                tree = process['completeTree']
                height = process['height']
                heights.append(height)
                complete_tree['completeTree']['AND'].append(tree)
            else:
                if 'courseId' in and_course.keys():
                    and_course_id = and_course['courseId'].replace(" ", "")
                    if and_course_id in seen_courses:
                        and_course = {'courseId': and_course_id, "prerequisiteTree": seen_courses[and_course_id]['prerequisiteTree'], "height": seen_courses[and_course_id]['height']}
                    else:
                        and_course_tree = get_complete_preq(and_course_id, seen_courses)
                        and_course = {'courseId': and_course_id, "prerequisiteTree": and_course_tree['completeTree'], "height": and_course_tree['height']}
                        seen_courses[and_course_id] = {"prerequisiteTree": and_course['prerequisiteTree'], "height": and_course['height']}
                        heights.append(and_course_tree['height'])
                    complete_tree['completeTree']['AND'].append(and_course)
        complete_tree['height'] += (max(heights)+1)
        if complete_tree['completeTree']['AND'] == [] or complete_tree['completeTree']['AND'] == [{}]:
            complete_tree['completeTree'] = {}
        if complete_tree['completeTree'] == {}:
            complete_tree['height'] = 0
    return complete_tree

@app.get("/tree/{school}/{degree}")
def get_tree_for_degree(school, degree):
    tree = {degree:{}}
    seen_courses = {}
    for d in degree_courses[school]:
        if d[0] == degree:
            courses = d[2]
            break
    for course in courses:
        if course in seen_courses.keys():
            tree[degree][course] = seen_courses[course]
        else:
            tree_info= get_complete_preq(course, seen_courses)
            seen_courses[course] = {"prerequisiteTree": tree_info['completeTree'], "height": tree_info['height']}
            tree[degree][course] = {"prerequisiteTree": tree_info['completeTree'], "height": tree_info['height']}
    return tree
    


# TODO: Add POST route for demo
@app.post('/add-courses/{course_id}')
def add_course(course_id):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", port=5001, reload=True)
