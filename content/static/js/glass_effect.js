const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('canvas-container').appendChild(renderer.domElement);

// Загрузка вашего фонового изображения (лес с мостом)
const loader = new THREE.TextureLoader();
const bgTexture = loader.load('{% static "images/forest-bg.jpg" %}');

// Шейдер преломления
const material = new THREE.ShaderMaterial({
    uniforms: {
        uTexture: { value: bgTexture },
        uRefraction: { value: 0.05 }, // Сила искажения
        uMouse: { value: new THREE.Vector2(0, 0) }
    },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        varying vec2 vUv;
        uniform sampler2D uTexture;
        uniform float uRefraction;
        
        void main() {
            // Имитация выпуклости (как на скриншоте)
            vec2 distortedUv = vUv + (texture2D(uTexture, vUv).rg - 0.5) * uRefraction;
            vec4 color = texture2D(uTexture, distortedUv);
            gl_FragColor = color;
        }
    `
});

const geometry = new THREE.PlaneGeometry(5, 3);
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);
camera.position.z = 2;

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}
animate();