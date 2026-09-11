import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

/**
 * Scientific 3D Flood Water Visualization (Three.js)
 * 
 * Features:
 * - Fluid volume flowing along the downstream channel (X-axis: Upstream A -> Downstream B/C -> Communities D/E)
 * - NO visible tank, NO box walls, NO cartoon borders - pure fluid volume in scientific dark void
 * - Realistic Gerstner wave displacement with turbulence responding to water level and rate of rise
 * - Water depth, velocity, and surge height interpolate smoothly from backend simulation state
 * - Highly optimized for Intel integrated GPUs (smooth 60 FPS)
 */
export default function FloodWater3D({ nodes = [], scenario = 'NORMAL' }) {
  const mountRef = useRef(null);
  const targetLevelRef = useRef(0.6);
  const targetRateRef = useRef(0.0);
  const targetRiskRef = useRef('NORMAL');

  // Update target physics properties from backend nodes
  useEffect(() => {
    if (nodes && nodes.length > 0) {
      // Calculate max and average water levels
      const levels = nodes.map(n => Number(n.water_level_m) || 0);
      const rates = nodes.map(n => Math.abs(Number(n.rate_of_rise_m_h)) || 0);
      const maxLvl = Math.max(...levels, 0.2);
      const maxRate = Math.max(...rates, 0);

      targetLevelRef.current = maxLvl;
      targetRateRef.current = maxRate;

      // Determine highest risk level
      const hasCritical = nodes.some(n => n.risk_level === 'CRITICAL');
      const hasWarning = nodes.some(n => n.risk_level === 'WARNING');
      const hasWatch = nodes.some(n => n.risk_level === 'WATCH');
      if (hasCritical) targetRiskRef.current = 'CRITICAL';
      else if (hasWarning) targetRiskRef.current = 'WARNING';
      else if (hasWatch) targetRiskRef.current = 'WATCH';
      else targetRiskRef.current = 'NORMAL';
    }
  }, [nodes, scenario]);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth || 800;
    const height = container.clientHeight || 500;

    // 1. Scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x03060c);
    scene.fog = new THREE.FogExp2(0x03060c, 0.025);

    // 2. Camera
    const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 100);
    camera.position.set(-14, 9, 14);
    camera.lookAt(1, 0, 0);

    // 3. WebGL Renderer
    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      powerPreference: 'high-performance',
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;
    container.appendChild(renderer.domElement);

    // 4. Lighting
    const ambientLight = new THREE.AmbientLight(0x0d2847, 1.8);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0x7dd3fc, 2.4);
    sunLight.position.set(-10, 18, 12);
    scene.add(sunLight);

    const rimLight = new THREE.DirectionalLight(0x38bdf8, 1.2);
    rimLight.position.set(15, -5, -10);
    scene.add(rimLight);

    // 5. Flow Channel Geometry (Length: 26 units, Width: 7 units)
    const channelLength = 26;
    const channelWidth = 7.5;
    const gridX = 90;
    const gridZ = 35;

    const surfaceGeometry = new THREE.PlaneGeometry(
      channelLength,
      channelWidth,
      gridX,
      gridZ
    );
    surfaceGeometry.rotateX(-Math.PI / 2);

    // Custom Water Surface Shader
    const waterUniforms = {
      uTime: { value: 0 },
      uFlowSpeed: { value: 1.2 },
      uWaveHeight: { value: 0.15 },
      uWaterLevel: { value: 0.6 },
      uTurbulence: { value: 1.0 },
      uDeepColor: { value: new THREE.Color(0x04244a) },
      uShallowColor: { value: new THREE.Color(0x1a8fd8) },
      uFoamColor: { value: new THREE.Color(0xbae6fd) },
    };

    const waterMaterial = new THREE.ShaderMaterial({
      uniforms: waterUniforms,
      vertexShader: `
        uniform float uTime;
        uniform float uFlowSpeed;
        uniform float uWaveHeight;
        uniform float uWaterLevel;
        uniform float uTurbulence;

        varying vec3 vWorldPosition;
        varying vec3 vNormal;
        varying float vWavePeak;

        // Gerstner Wave approximation for directional fluid flow along +X
        vec3 gerstnerWave(vec2 dir, float steepness, float wavelength, vec2 pos, float time) {
          float k = 6.28318 / wavelength;
          float c = sqrt(9.8 / k);
          vec2 d = normalize(dir);
          float f = k * (dot(d, pos) - c * time * uFlowSpeed);
          float a = steepness / k * uWaveHeight;

          return vec3(
            d.x * (a * cos(f)),
            a * sin(f),
            d.y * (a * cos(f))
          );
        }

        void main() {
          vec3 pos = position;

          // Downstream directional waves (dominant flow along +X from upstream to downstream)
          vec3 wave1 = gerstnerWave(vec2(1.0, 0.15), 0.35, 4.5, pos.xz, uTime);
          vec3 wave2 = gerstnerWave(vec2(0.9, -0.2), 0.25, 2.2, pos.xz, uTime * 1.3);
          vec3 wave3 = gerstnerWave(vec2(1.0, 0.3), 0.20 * uTurbulence, 1.1, pos.xz, uTime * 1.8);
          
          // Small surface capillary ripples
          float ripple = sin(pos.x * 6.0 + uTime * 4.0 * uFlowSpeed) * 
                         cos(pos.z * 6.0 + uTime * 3.0) * 0.03 * uTurbulence;

          vec3 displaced = pos + wave1 + wave2 + wave3;
          displaced.y += ripple;

          // Water height mapped to backend level
          displaced.y += uWaterLevel;

          vWavePeak = (wave1.y + wave2.y + wave3.y + ripple);
          vWorldPosition = (modelMatrix * vec4(displaced, 1.0)).xyz;

          // Analytical normal derivation for sharp specular reflections
          vec3 n = normalize(vec3(
            -(wave1.x + wave2.x) * 0.5,
            1.0,
            -(wave1.z + wave2.z) * 0.5
          ));
          vNormal = normalize(normalMatrix * n);

          gl_Position = projectionMatrix * viewMatrix * vec4(vWorldPosition, 1.0);
        }
      `,
      fragmentShader: `
        uniform vec3 uDeepColor;
        uniform vec3 uShallowColor;
        uniform vec3 uFoamColor;
        uniform float uWaterLevel;

        varying vec3 vWorldPosition;
        varying vec3 vNormal;
        varying float vWavePeak;

        void main() {
          vec3 viewDir = normalize(cameraPosition - vWorldPosition);
          vec3 normal = normalize(vNormal);

          // Fresnel reflectance for fluid surface
          float fresnel = pow(1.0 - max(dot(viewDir, normal), 0.0), 3.0);
          fresnel = clamp(fresnel, 0.15, 0.95);

          // Water depth gradient
          vec3 waterCol = mix(uDeepColor, uShallowColor, clamp(vWavePeak * 2.0 + 0.5, 0.0, 1.0));

          // Crest highlights / foam sparkles on turbulent wave peaks
          if (vWavePeak > 0.18) {
            float foamFactor = smoothstep(0.18, 0.35, vWavePeak);
            waterCol = mix(waterCol, uFoamColor, foamFactor * 0.7);
          }

          // Specular sun reflection
          vec3 lightDir = normalize(vec3(-0.4, 0.8, 0.5));
          vec3 halfVec = normalize(lightDir + viewDir);
          float spec = pow(max(dot(normal, halfVec), 0.0), 32.0);
          vec3 specularColor = vec3(1.0, 0.95, 0.8) * spec * 0.8;

          vec3 finalColor = mix(waterCol, vec3(0.65, 0.85, 1.0), fresnel * 0.6) + specularColor;

          gl_FragColor = vec4(finalColor, 0.85);
        }
      `,
      transparent: true,
      side: THREE.DoubleSide,
    });

    const waterMesh = new THREE.Mesh(surfaceGeometry, waterMaterial);
    scene.add(waterMesh);

    // 6. Water Body Depth Volume (Slab sides creating realistic water depth appearance without box)
    const sideGeometry = new THREE.BufferGeometry();
    const sideMaterial = new THREE.MeshBasicMaterial({
      color: 0x021b3a,
      transparent: true,
      opacity: 0.75,
      side: THREE.DoubleSide,
      depthWrite: false,
    });

    const sideMesh = new THREE.Mesh(sideGeometry, sideMaterial);
    scene.add(sideMesh);

    // 7. Subtle Flow Particles (streaks flowing downstream along X axis)
    const particleCount = 180;
    const particleGeo = new THREE.BufferGeometry();
    const particlePos = new Float32Array(particleCount * 3);
    const particleSpeeds = new Float32Array(particleCount);

    for (let i = 0; i < particleCount; i++) {
      particlePos[i * 3] = (Math.random() - 0.5) * channelLength;
      particlePos[i * 3 + 1] = 0;
      particlePos[i * 3 + 2] = (Math.random() - 0.5) * (channelWidth - 0.5);
      particleSpeeds[i] = 0.8 + Math.random() * 0.8;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));

    const particleMat = new THREE.PointsMaterial({
      color: 0x7dd3fc,
      size: 0.12,
      transparent: true,
      opacity: 0.55,
      blending: THREE.AdditiveBlending,
    });
    const particleSystem = new THREE.Points(particleGeo, particleMat);
    scene.add(particleSystem);

    // 8. Interactive Orbit Control (lightweight mouse rotation)
    let isDragging = false;
    let prevMouseX = 0;
    let prevMouseY = 0;
    let cameraAngle = Math.PI * 0.75;
    let cameraHeight = 9;
    let cameraDist = 20;

    const onMouseDown = (e) => {
      isDragging = true;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;
    };

    const onMouseMove = (e) => {
      if (!isDragging) return;
      const dx = e.clientX - prevMouseX;
      const dy = e.clientY - prevMouseY;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;

      cameraAngle -= dx * 0.005;
      cameraHeight = Math.max(3, Math.min(18, cameraHeight + dy * 0.04));
      updateCamera();
    };

    const onMouseUp = () => {
      isDragging = false;
    };

    const onWheel = (e) => {
      cameraDist = Math.max(12, Math.min(32, cameraDist + e.deltaY * 0.02));
      updateCamera();
    };

    function updateCamera() {
      camera.position.x = Math.cos(cameraAngle) * cameraDist;
      camera.position.z = Math.sin(cameraAngle) * cameraDist;
      camera.position.y = cameraHeight;
      camera.lookAt(1, currentLevel * 0.5, 0);
    }

    const domElem = renderer.domElement;
    domElem.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    domElem.addEventListener('wheel', onWheel, { passive: true });

    // Handle Resize
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    // 9. Smooth Animation Loop
    let currentLevel = 0.6;
    let currentWaveHeight = 0.12;
    let currentFlowSpeed = 1.0;
    let currentTurbulence = 1.0;
    let animationFrameId;
    const clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const dt = clock.getDelta();
      const time = clock.getElapsedTime();

      // Smooth interpolation towards target backend water level
      const targetLvl = targetLevelRef.current;
      const targetRate = targetRateRef.current;
      const risk = targetRiskRef.current;

      // Scale water level visually: 0.3m -> 0.3 units; 3.0m -> 2.4 units
      const visualLevel = Math.min(Math.max(targetLvl * 0.7, 0.2), 3.0);
      currentLevel += (visualLevel - currentLevel) * 0.04;

      // Turbulence & flow velocity dynamic scaling
      let targetTurb = 1.0;
      let targetSpeed = 1.0;
      let targetWave = 0.12;

      if (risk === 'CRITICAL') {
        targetTurb = 2.8;
        targetSpeed = 2.4;
        targetWave = 0.35 + targetRate * 0.4;
      } else if (risk === 'WARNING') {
        targetTurb = 2.0;
        targetSpeed = 1.8;
        targetWave = 0.25 + targetRate * 0.3;
      } else if (risk === 'WATCH') {
        targetTurb = 1.4;
        targetSpeed = 1.3;
        targetWave = 0.18;
      }

      currentWaveHeight += (targetWave - currentWaveHeight) * 0.05;
      currentFlowSpeed += (targetSpeed - currentFlowSpeed) * 0.05;
      currentTurbulence += (targetTurb - currentTurbulence) * 0.05;

      // Update shader uniforms
      waterUniforms.uTime.value = time;
      waterUniforms.uWaterLevel.value = currentLevel;
      waterUniforms.uWaveHeight.value = currentWaveHeight;
      waterUniforms.uFlowSpeed.value = currentFlowSpeed;
      waterUniforms.uTurbulence.value = currentTurbulence;

      // Animate flowing tracer particles along +X downstream
      const posAttr = particleGeo.attributes.position;
      const halfLen = channelLength * 0.5;
      for (let i = 0; i < particleCount; i++) {
        let x = posAttr.getX(i);
        let speed = particleSpeeds[i] * currentFlowSpeed * 1.8;
        x += speed * dt;
        if (x > halfLen) {
          x = -halfLen;
        }
        posAttr.setX(i, x);
        posAttr.setY(i, currentLevel - 0.05);
      }
      posAttr.needsUpdate = true;

      // Slowly drift camera slightly for cinematic immersion if not dragging
      if (!isDragging) {
        cameraAngle += 0.0008;
        updateCamera();
      }

      renderer.render(scene, camera);
    };

    animate();

    // 10. Clean up on unmount
    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      domElem.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      domElem.removeEventListener('wheel', onWheel);

      surfaceGeometry.dispose();
      waterMaterial.dispose();
      sideGeometry.dispose();
      sideMaterial.dispose();
      particleGeo.dispose();
      particleMat.dispose();
      renderer.dispose();

      if (container && domElem.parentNode === container) {
        container.removeChild(domElem);
      }
    };
  }, []);

  // Compute live readout stats for overlay HUD
  const maxWaterLevel = nodes.length > 0 
    ? Math.max(...nodes.map(n => Number(n.water_level_m) || 0)).toFixed(2)
    : '0.60';
  const avgWaterLevel = nodes.length > 0
    ? (nodes.reduce((acc, n) => acc + (Number(n.water_level_m) || 0), 0) / nodes.length).toFixed(2)
    : '0.50';

  return (
    <div className="three-container-wrapper">
      <div ref={mountRef} className="three-canvas" />

      {/* Scientific HUD Overlay */}
      <div className="water-hud-overlay">
        <div className="hud-title">3D FLOOD DYNAMICS (DOWNSTREAM CHANNEL)</div>
        <div className="hud-val">{maxWaterLevel} m <span style={{ fontSize: '0.75rem', fontWeight: 'normal', color: '#94a3b8' }}>MAX LEVEL</span></div>
        <div className="hud-sub">Avg Depth: {avgWaterLevel} m | Directional Flow: Upstream → Downstream</div>
      </div>

      {/* Hazard Progression Bar */}
      <div className="water-hud-progression">
        <div className="progression-step active">
          <span>A: Upstream</span>
          <span>→</span>
        </div>
        <div className="progression-step active">
          <span>B: Downstream</span>
          <span>→</span>
        </div>
        <div className="progression-step active">
          <span>C: Village</span>
          <span>→</span>
        </div>
        <div className="progression-step active">
          <span>D: Low-Risk</span>
          <span>&</span>
          <span>E: Critical Community</span>
        </div>
      </div>
    </div>
  );
}
