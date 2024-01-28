import { Text } from "@react-three/drei";
import { PlaneGeometry, MeshBasicMaterial } from "three";

export default function Node({ course, x, y }) {
  return (
    <>
      <Text color={"black"}>{course}</Text>
      <mesh position={[x, y, 0]}>
        <planeGeometry args={[10, 10]} />
        <meshBasicMaterial color={"white"} />
      </mesh>
    </>
  );
}