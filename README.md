# ZOT Tree

## Introduction

ZOT Tree is a web app that displays the complete pre-requisite tree of an entire degree at UCI. 

## This Application

This application consists of a [React](https://react.dev/) frontend and
[FastAPI](https://fastapi.tiangolo.com/) backend. 

Please view the `README.md`s in
`frontend/` and `backend/` for more information on how to start everything.

Here are some screenshots of its functionalities:

<img width="1792" alt="Screenshot 2024-01-28 at 11 00 54 AM" src="https://github.com/williamzchu/zot-tree/assets/78942001/0e9b823f-d5d1-406d-a706-fd6f8e7ab308">

<img width="1792" alt="Screenshot 2024-01-28 at 11 03 00 AM" src="https://github.com/williamzchu/zot-tree/assets/78942001/fcdd0809-7b39-421b-95fa-99a9ef0e86cb">

<img width="1792" alt="Screenshot 2024-01-28 at 10 55 15 AM" src="https://github.com/williamzchu/zot-tree/assets/78942001/c0726efc-eb7d-45ab-a1d0-0455046c7ad2">

<img width="1792" alt="Screenshot 2024-01-28 at 10 55 00 AM" src="https://github.com/williamzchu/zot-tree/assets/78942001/e4486e55-5225-499e-bcae-95b0f7d0a75b">

The entire tree of a degree is created on the page and users can interact with it in different ways. 
Hovering over a course node changes the color of the lines to black to display the path for courses that it unlocks when completed.
Clicking on a course node will mark it as complete and it changes the color of the node to blue. It will also display the pre-requisites that should have been completed before taking that course with a blue line. And as stated before, the black lines will lead to courses that unlock once that course is complete. The courses it unlocks are colored in green and those courses have green lines to signify the other pre-requisites required to unlock them.

