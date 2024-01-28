import { Text } from "@react-three/drei";
import { PlaneGeometry, MeshBasicMaterial } from "three";

export default function Node({ course, x, y }) {

  return (
    <>
      <Text position={[x, y, -0.000001]} color={"black"}>{course}</Text>
      <mesh position={[x, y, -0.000001]}>
        <planeGeometry args={[4,1.4]} />
        <meshBasicMaterial/>
      </mesh>
    </>
  );
}