import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text } from '@react-three/drei';
import * as THREE from 'three';

interface Organism {
    id: string;
    fitness: number;
    generation: number;
    energy?: number;
}

interface Evolution3DProps {
    organisms: Organism[];
    currentGeneration: number;
}

function OrganismSphere({ organism, index }: { organism: Organism; index: number }) {
    const meshRef = useRef<THREE.Mesh>(null);

    // Size based on fitness (0.5 to 2.0)
    const size = useMemo(() => {
        return Math.max(0.5, Math.min(2.0, organism.fitness * 2));
    }, [organism.fitness]);

    // Color based on fitness tier
    const color = useMemo(() => {
        if (organism.fitness > 0.7) return '#10b981'; // Green - excellent
        if (organism.fitness > 0.4) return '#3b82f6'; // Blue - good
        return '#ef4444'; // Red - poor
    }, [organism.fitness]);

    // Position in 3D space
    const position = useMemo(() => {
        const x = (organism.generation * 3) - 15;
        const y = organism.fitness * 10 - 5;
        const z = (index % 10) * 2 - 10;
        return [x, y, z] as [number, number, number];
    }, [organism.generation, organism.fitness, index]);

    // Gentle float animation
    useFrame((state) => {
        if (meshRef.current) {
            meshRef.current.position.y += Math.sin(state.clock.elapsedTime + index) * 0.001;
        }
    });

    return (
        <group position={position}>
            <mesh ref={meshRef}>
                <sphereGeometry args={[size, 32, 32]} />
                <meshStandardMaterial
                    color={color}
                    emissive={color}
                    emissiveIntensity={0.3}
                    metalness={0.8}
                    roughness={0.2}
                />
            </mesh>
            {/* Glow effect */}
            <mesh scale={size * 1.2}>
                <sphereGeometry args={[1, 16, 16]} />
                <meshBasicMaterial
                    color={color}
                    transparent
                    opacity={0.1}
                />
            </mesh>
        </group>
    );
}

function GridHelper3D() {
    return (
        <>
            <gridHelper args={[50, 50, '#00f3ff', '#1e293b']} position={[0, -6, 0]} />
            <axesHelper args={[20]} />
        </>
    );
}

export default function Evolution3D({ organisms, currentGeneration }: Evolution3DProps) {
    return (
        <div className="evolution-3d-container" style={{ width: '100%', height: '600px', background: '#0a0e1a', borderRadius: '16px', overflow: 'hidden' }}>
            <Canvas
                camera={{ position: [15, 5, 15], fov: 60 }}
                style={{ background: 'linear-gradient(to bottom, #0a0e1a, #1e293b)' }}
            >
                <ambientLight intensity={0.3} />
                <pointLight position={[10, 10, 10]} intensity={0.8} color="#00f3ff" />
                <pointLight position={[-10, -10, -10]} intensity={0.5} color="#a855f7" />

                <GridHelper3D />

                {/* Render organisms */}
                {organisms.map((organism, index) => (
                    <OrganismSphere key={organism.id} organism={organism} index={index} />
                ))}

                {/* Generation label */}
                <Text
                    position={[0, 8, 0]}
                    fontSize={1.5}
                    color="#00f3ff"
                    anchorX="center"
                    anchorY="middle"
                >
                    Generation {currentGeneration}
                </Text>

                <OrbitControls
                    enablePan={true}
                    enableZoom={true}
                    enableRotate={true}
                    maxDistance={50}
                    minDistance={5}
                />
            </Canvas>

            <div style={{
                position: 'absolute',
                top: '20px',
                right: '20px',
                background: 'rgba(15, 23, 42, 0.8)',
                backdropFilter: 'blur(10px)',
                padding: '12px 16px',
                borderRadius: '8px',
                border: '1px solid rgba(0, 243, 255, 0.3)',
                color: '#e0e7ff',
                fontSize: '14px'
            }}>
                <div style={{ marginBottom: '8px', fontWeight: '600', color: '#00f3ff' }}>Legend</div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                    <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#10b981' }}></div>
                    <span>Excellent (0.7+)</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                    <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#3b82f6' }}></div>
                    <span>Good (0.4-0.7)</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ef4444' }}></div>
                    <span>Poor (&lt;0.4)</span>
                </div>
            </div>
        </div>
    );
}
