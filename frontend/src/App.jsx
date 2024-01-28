import { useEffect, useLayoutEffect, useRef, useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import React from 'react';
import Tree from 'react-d3-tree';
import Node from "./Node";
import * as THREE from 'three'
import { Canvas } from "@react-three/fiber";
import { Line, OrbitControls, OrthographicCamera } from "@react-three/drei";

const width = 24
function App() {
  const [nodeList, setNodeList] = useState([]);


  const tree = {
    ICS33: {height: 2, prereqs:["ICS32", "ICS32A"]}, 
    ICS32A: {height: 1, prereqs:["ICS31"]}, 
    ICS32: {height: 1, prereqs:["ICS31"]}, 
    ICS31: {height: 0, prereqs:[]}
  }

  const tree_list = []
  for (let i = 0; i < 15; i++){
    tree_list.push([])
  }

  for (const [key, value] of Object.entries(tree)){
    tree_list[value.height].push(key)
  }

  const nodelist = []
  for (let i = 0; i < 15; i++){
    nodelist.push([])
  }
  const refs = {}
  for (let i = 0; i < 15; i++){
    for (let j = 0; j < tree_list[i].length; j++){
      const c = tree_list[i][j]
      const y = tree[c].height * 4
      const x = (j+1)/(tree_list[i].length+1) * width - width/2

      refs[c] = {x: x, y: y}
      nodelist.push(<Node key={c} course={c} x={x} y = {y}></Node>)
    }
  }

  const linelist = []
  for (let i = 0; i < 15; i++){
    for (let j = 0; j < tree_list[i].length; j++){
      const c = tree_list[i][j]
      
      for (let k = 0; k < tree[c].prereqs.length; k++){
        const points = []
        const other = tree[c].prereqs[k]
        points.push(new THREE.Vector3(refs[c].x, refs[c].y, -1))
        points.push(new THREE.Vector3(refs[other].x, refs[other].y, -1))

        const geo = new THREE.BufferGeometry().setFromPoints(points)

        const line = <Line points={points} color={"black"}/>
        linelist.push(line)
      }

    }
  }
  console.log(refs)
  return (
    <>
      <Canvas>
        <OrbitControls enableRotate={false} enableDamping={true}/>
        <orthographicCamera position={[0,0,10]}/>
        <group scale={0.1}>
          {nodelist}
          {linelist}
        </group>
      </Canvas>
    </>
  );
}

export default App;