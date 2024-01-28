import { useEffect, useLayoutEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import React from 'react';
import Tree from 'react-d3-tree';
import Node from "./Node";
import * as THREE from 'three'
import { Canvas } from "@react-three/fiber";
import { OrbitControls, OrthographicCamera } from "@react-three/drei";

function App() {
  const [nodeList, setNodeList] = useState([]);
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleWindowResize = () => {
      setWidth(window.innerWidth)
    };

    window.addEventListener('resize', handleWindowResize);

    return () => {
      window.removeEventListener('resize', handleWindowResize);
    };
  }, [width]);


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

  for (let i = 0; i < 15; i++){
    for (let j = 0; j < tree_list[i].length; j++){
      const c = tree_list[i][j]
      const y = tree[c].height * 100
      const x = (j / tree_list[i].length) * width + 50
      nodelist.push(<Node course={c} x={x} y = {y}></Node>)
    }
  }

  return (
    <>
      <Canvas>
        <OrbitControls enableRotate={false}/>
        <orthographicCamera/>
        {nodelist}
      </Canvas>
    </>
  );
}

export default App;