import { useEffect, useLayoutEffect, useRef, useState } from "react";
import "./App.css";
import React from 'react';
import Node from "./Node";
import * as THREE from 'three'
import { Canvas } from "@react-three/fiber";
import { Line, OrbitControls, OrthographicCamera } from "@react-three/drei";
import {HoverContext} from "./HoverContext";
import Edge from "./Edge";

const width = 15
const maxHeight = 40
function App() {
  const [nodeList, setNodeList] = useState([]);
  const [data, setData] = useState(null)
  const [context, setContext] = useState({});
  const [postreqs, setPostreqs] = useState({});

  useEffect(
    () => {
      fetch('mathminor_prereqs.json')
      .then((response) => response.json())
      .then(json =>{
        setData(json)
        const newcontext = {}
        for (const [key, value] of Object.entries(json)){
          newcontext[key] = localStorage.getItem(key)
        }
        setContext(newcontext)
      })
    }, []
  )
  
  const nodelist = []
  const linelist = []
  
  function markExtended(course){
    const newcontext = {...context}
    if (context[course] == 0){
      newcontext[course] = 3
    }
    setContext(newcontext)
  }

  function unMarkExtended(course){
    const newcontext = {...context}
    if (context[course] == 3){
      newcontext[course] = 0
    }
    setContext(newcontext)
  }
  
  function updatePotential(){
    const newcontext = {...context}
    console.log(newcontext)
    for (const [key, value] of Object.entries(data)){
      if (context[key] == 1 || context[key] == 2){
        continue
      }
      else{
        let count = 0
        for (let i = 0; i < value.prereqs.length; i++){
          const other = value.prereqs[i]
          if (context[other] == 2){
            count += 1
          }
        }
        if (value.prereqs.length == 0){
          newcontext[key] = 0
        }
        else{
          newcontext[key] = count/value.prereqs.length
        }
      }
    }
    setContext(newcontext)
  }
  
  //0 = undone, 1 = hovered, 2 = finished, 3 = prereqs finished
  function clickContext(course){
    const newcontext = {...context}
    if (context[course] != 2){
      newcontext[course] = 2
    }
    else{
      newcontext[course] = 0
    }
    localStorage.setItem(course, newcontext[course])
    setContext(newcontext)
    //updatePotential()
  }

  function hoverContext(course){
    const newcontext = {...context}
    if (context[course] != 2){
      newcontext[course] = 1
      setContext(newcontext)
    }
  }

  function unHoverContext(course){
    const newcontext = {...context}
    if (context[course] != 2){
      newcontext[course] = 0
      setContext(newcontext)
    }
  }

  if (data){

    const tree = data

    const tree_list = []
    for (let i = 0; i < maxHeight; i++){
      tree_list.push([])
    }
  
    for (const [key, value] of Object.entries(tree)){
      tree_list[value.height].push(key)
    }

    let w = 0
    for (let i = 0; i < maxHeight; i++){
      w = Math.max(w, tree_list[i].length)
    }
    //console.log(w)
    for (let i = 0; i < maxHeight; i++){
      nodelist.push([])
    }

    const refs={}
    for (let i = 0; i < maxHeight; i++){
      for (let j = 0; j < tree_list[i].length; j++){
        const c = tree_list[i][j]
        const y = -tree[c].height * 10 + Math.sin((j + 1) / (tree_list[i].length + 1) *Math.PI) * 50
        const x = (j + 1) / (tree_list[i].length + 1)*width*w - width*w/2
  
        refs[c] = {x: x, y: y}
        nodelist.push(<Node key={c} course={c} x={x} y = {y} hover={hoverContext} unhover={unHoverContext} click={clickContext}></Node>)
      }
    }
  
    for (let i = 0; i < maxHeight; i++){
      for (let j = 0; j < tree_list[i].length; j++){
        const c = tree_list[i][j]
        if (context[c] >= 3){
          context[c] = 0
        }
        let count = 0
        for (let k = 0; k < tree[c].prereqs.length; k++){
          const points = []
          const other = tree[c].prereqs[k]
          if (context[other] == 2){
            count++
          }
          if ( tree[c].prereqs.length && context[c]!=2  && context[c]!=1 && count){
            context[c] = 3 + count/tree[c].prereqs.length
          }

          points.push(new THREE.Vector3(refs[c].x, refs[c].y, -1))
          points.push(new THREE.Vector3(refs[other].x, refs[other].y, -1))
  
          const geo = new THREE.BufferGeometry().setFromPoints(points)
  
          const line = <Edge course={c} points={points} other={other} mark={markExtended} unmark={unMarkExtended}/>
          linelist.push(line)
        }
  
      }
    }

  }


  return (
    <HoverContext.Provider value={context}>
      <Canvas>
        <OrbitControls enableRotate={false} enableDamping={false}/>
        <orthographicCamera position={[0,0,10]}/>
        <group scale={0.1}>
          {nodelist}
          {linelist}
        </group>
      </Canvas>
    </HoverContext.Provider>
  );
}

export default App;