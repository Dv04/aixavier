'use client';

import { Canvas, useFrame } from "@react-three/fiber";
import { Points, PointMaterial } from "@react-three/drei";
import { useMemo, useRef, useState, useEffect } from "react";
import * as THREE from "three";

function PointCloud() {
  const ref = useRef<THREE.Points>(null);
  const [parallax, setParallax] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 0.6;
      const y = (e.clientY / window.innerHeight - 0.5) * 0.6;
      setParallax({ x, y });
    };
    window.addEventListener("pointermove", handler);
    return () => window.removeEventListener("pointermove", handler);
  }, []);

  const positions = useMemo(() => {
    const count = 4000;
    const arr = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const r = 10 * Math.cbrt(Math.random());
      const theta = Math.random() * 2 * Math.PI;
      const phi = Math.acos(2 * Math.random() - 1);
      const x = r * Math.sin(phi) * Math.cos(theta);
      const y = r * Math.sin(phi) * Math.sin(theta);
      const z = r * Math.cos(phi);
      arr[i * 3 + 0] = x;
      arr[i * 3 + 1] = y;
      arr[i * 3 + 2] = z;
    }
    return arr;
  }, []);

  useFrame((state, delta) => {
    if (!ref.current) return;
    ref.current.rotation.y += delta / 10;
    ref.current.rotation.x = THREE.MathUtils.lerp(ref.current.rotation.x, parallax.y / 3, 0.1);
    ref.current.rotation.z = THREE.MathUtils.lerp(ref.current.rotation.z, -parallax.x / 3, 0.1);
  });

  return (
    <Points ref={ref} positions={positions} stride={3} frustumCulled>
      <PointMaterial size={0.06} transparent color="#4be0c1" opacity={0.35} depthWrite={false} sizeAttenuation />
    </Points>
  );
}

export default function PointField() {
  return (
    <div className="pointer-events-none fixed inset-0 z-0 opacity-60">
      <Canvas camera={{ position: [0, 0, 20], fov: 55 }}>
        <fog attach="fog" args={["#020308", 5, 24]} />
        <GridFloor />
        <PointCloud />
      </Canvas>
      <div className="absolute inset-0 bg-gradient-to-b from-[#020308] via-transparent to-[#020308]" />
    </div>
  );
}

function GridFloor() {
  const lines = useRef<THREE.Group>(null);
  useFrame((_, delta) => {
    if (!lines.current) return;
    lines.current.position.z -= delta * 4;
    if (lines.current.position.z < -10) lines.current.position.z = 0;
  });

  const gridGeometry = useMemo(() => {
    const group = new THREE.Group();
    const material = new THREE.LineBasicMaterial({ color: "#00FF94", transparent: true, opacity: 0.35 });
    const size = 60;
    const divisions = 40;
    const step = size / divisions;
    for (let i = -size / 2; i <= size / 2; i += step) {
      const pointsH = [new THREE.Vector3(-size / 2, 0, i), new THREE.Vector3(size / 2, 0, i)];
      const geoH = new THREE.BufferGeometry().setFromPoints(pointsH);
      group.add(new THREE.Line(geoH, material));
      const pointsV = [new THREE.Vector3(i, 0, -size / 2), new THREE.Vector3(i, 0, size / 2)];
      const geoV = new THREE.BufferGeometry().setFromPoints(pointsV);
      group.add(new THREE.Line(geoV, material));
    }
    return group;
  }, []);

  return (
    <group ref={lines} position={[0, -4, 0]}>
      {gridGeometry.children.map((child) => (
        <primitive object={child} key={child.uuid} />
      ))}
    </group>
  );
}
