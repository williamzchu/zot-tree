import { useContext, useEffect, useState } from "react"
import { HoverContext } from "./HoverContext"
import { Line } from "@react-three/drei"

export default function Edge({course, points, other, mark, unmark}){
    const context = useContext(HoverContext)
    const [hovered, setHovered] = useState(false)

    let color = 0xd3d3d3
    if (context[other] == 1 || context[other]  == 2){
        color = 0x333333
        //mark(other)
    }
    else if (context[course] >= 3){
        color = 0x008800
        //mark(other)
    }
    if (context[course] == 2){
        color = 0x0000AA
        //mark(other)
    }
    //unmark(other)
    return (
    <>
        <Line points={points} color={color} opacity={0.9}/>
    </>
  );
}