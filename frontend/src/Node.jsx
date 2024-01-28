import { Text } from "@react-three/drei";
import { useContext, useState } from "react";
import { PlaneGeometry, MeshBasicMaterial } from "three";
import { HoverContext } from "./HoverContext";
import { Line } from "@react-three/drei";
import * as THREE from 'three'
const col = new THREE.Color()
const grey = new THREE.Color(0xd3ddd3)
const green = new THREE.Color(0x00ff00)
export default function Node({ course, x, y, hover, unhover, click }) {
    const context = useContext(HoverContext)


    let color = 0xd3d3d3
    if (context[course] == 1){
        color = 0x555555
    }
    else if (context[course] == 2){
        color = 0x4444ff
    }
    else if (context[course] >= 3){
        const diff = 4 - context[course] 
        color = col.clone().lerpColors(green, grey, diff)
        //console.log(course, color)
    }
    return (
    <>
      <Text position={[x, y, -0.000001]} color={"black"}>{course}</Text>
      <mesh position={[x, y, -0.000001]} onPointerEnter={() => {hover(course)}} onPointerLeave={() => {unhover(course)}} onClick={()=>click(course)}>
        <planeGeometry args={[10,4]} />
        <meshBasicMaterial color={color}/>
      </mesh>
    </>
  );
}