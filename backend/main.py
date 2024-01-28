"""
app.py

This one file is all you need to start off with your FastAPI server!
"""

from typing import Optional

import uvicorn
from fastapi import FastAPI, status
import requests
# from dotenv import load_env
# import os
from fastapi.middleware.cors import CORSMiddleware
import json

# load_env()

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


# The line starting with "@" is a Python decorator. For this tutorial, you
# don't need to know exactly how they work, but if you'd like to read more on
# them, see https://peps.python.org/pep-0318/.
#
# In short, the decorator declares the function it decorates as a FastAPI route
# with the path of the provided route. This line declares that a new GET route
# called "/" so that if you access "http://localhost:5000/", the below
# dictionary will be returned as a JSON response with the status code 200.
#
# For any other routes you declare, like the `/home` route below, you can access
# them at "http://localhost:5000/home". Because of this, we'll be omitting the
# domain portion for the sake of brevity.
@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/home")
# def home():
#     return {"message": "This is the home page"}


# The routes that you specify can also be dynamic, which means that any path
# that follows the format `/items/[some integer]` is valid. When providing
# such path parameters, you'll need to follow this specific syntax and state
# the type of this argument.
#
# This path also includes an optional query parameter called "q". By accessing
# the URL "/items/123456?q=testparam", the JSON response:
#
# { "item_id": 123456, "q": "testparam" }
#
# will be returned. Note that if `item_id` isn't an integer, FastAPI will
# return a response containing an error statement instead of our result.
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/courses/{course_id}")
def get_course(course_id: str):
    # gets the course info given its course id
    # res = requests.get(f"{os.getenv('PETER_PORTAL_URL')}/courses/{course_id}")
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
def get_complete_preq(course_id:str, seen_courses={}, seen=False):
    # gets the complete pre req tree for a certain course
    # pretty slow
    seen_courses = seen_courses
    tree = get_course_prereq(course_id)
    return process_tree(tree, seen_courses, seen)

def process_tree(tree: dict, seen_courses={}, seen=False):
    # helper to create the complete pre req tree for a course
    # recurses down to build entire tree
    seen_courses = seen_courses
    complete_tree = {'prerequisiteTree': {}, 'height': 0}
    if 'height' in tree.keys():
        complete_tree['height'] = tree['height']
    if 'OR' in tree.keys():
        complete_tree['prerequisiteTree']['OR'] = []
        heights = [0]
        for or_course in tree['OR']:
            if 'AND' in or_course.keys():
                process = process_tree(or_course, seen_courses)
                tree = process['prerequisiteTree']
                height = process['height']
                heights.append(height)
                complete_tree['prerequisiteTree']['OR'].append(tree)
            else:
                if 'courseId' in or_course.keys():
                    or_course_id = or_course['courseId'].replace(" ", "")
                    if or_course_id in seen_courses:
                        or_course = {'courseId': or_course_id, "prerequisiteTree": seen_courses[or_course_id]['prerequisiteTree'], "height": seen_courses[or_course_id]['height']}
                    else:
                        or_course_tree = get_complete_preq(or_course_id, seen_courses)
                        or_course = {'courseId': or_course_id, "prerequisiteTree": or_course_tree['prerequisiteTree'], "height": or_course_tree['height']}
                        seen_courses[or_course_id] = {"prerequisiteTree": or_course['prerequisiteTree'], "height": or_course_tree['height']}
                        heights.append(or_course_tree['height'])
                        complete_tree['prerequisiteTree']['OR'].append(or_course)
        complete_tree['height'] += (max(heights)+1)
        if complete_tree['prerequisiteTree']['OR'] == [] or complete_tree['prerequisiteTree']['OR'] == [{}]:
            complete_tree['prerequisiteTree'] = {}
    if 'AND' in tree.keys():
        complete_tree['prerequisiteTree']['AND'] = []
        heights= [0]
        for and_course in tree['AND']:
            if 'OR' in and_course.keys():
                process = process_tree(and_course, seen_courses)
                tree = process['prerequisiteTree']
                height = process['height']
                heights.append(height)
                complete_tree['prerequisiteTree']['AND'].append(tree)
            else:
                if 'courseId' in and_course.keys():
                    and_course_id = and_course['courseId'].replace(" ", "")
                    if and_course_id in seen_courses:
                        and_course = {'courseId': and_course_id, "prerequisiteTree": seen_courses[and_course_id]['prerequisiteTree'], "height": seen_courses[and_course_id]['height']}
                    else:
                        and_course_tree = get_complete_preq(and_course_id, seen_courses)
                        and_course = {'courseId': and_course_id, "prerequisiteTree": and_course_tree['prerequisiteTree'], "height": and_course_tree['height']}
                        seen_courses[and_course_id] = {"prerequisiteTree": and_course['prerequisiteTree'], "height": and_course['height']}
                        heights.append(and_course_tree['height'])
                        complete_tree['prerequisiteTree']['AND'].append(and_course)
        complete_tree['height'] += (max(heights)+1)
        if complete_tree['prerequisiteTree']['AND'] == [] or complete_tree['prerequisiteTree']['AND'] == [{}]:
            complete_tree['prerequisiteTree'] = {}
        if complete_tree['prerequisiteTree'] == {}:
            complete_tree['height'] = 0
    if seen:
        return complete_tree, seen_courses
    else:
        return complete_tree

@app.get("/tree/{school}/{degree}")
def get_tree_for_degree(school, degree):
    tree = {degree:{}}
    seen_courses = {}
    for d in degree_courses[school]:
        if d[0] == degree:
            courses = d[2]
            break
    # still not working properly
    # courses are being saved with incorrect trees
        
    # for course in courses:
    #     if course in seen_courses.keys():
    #         tree[degree][course] = seen_courses[course]
    #     else:
    #         tree_info, seen_courses = get_complete_preq(course, seen_courses, True)
    #         seen_courses[course] = tree_info
    #         tree[degree][course] = tree_info
    return tree
    


# TODO: Add POST route for demo
@app.post('/add-courses/{course_id}')
def add_course(course_id):

    pass


if __name__ == "__main__":
    uvicorn.run("main:app", port=5001, reload=True)
