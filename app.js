const socket = new WebSocket("ws://127.0.0.1:8765");

// Canvas pour Three.js
const suiCanvas = document.getElementById("sui-canvas");
// Initialisation de Three.js ici (voir exemple ci-dessous)

const messagesDiv = document.getElementById("messages");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");

sendButton.addEventListener("click", () => {
  const message = messageInput.value;
  messagesDiv.innerHTML += `<div>${message}</div>`;
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
  messageInput.value = "";
  socket.send(message);
});

socket.onmessage = (event) => {
  data = JSON.parse(event.data);
  messagesDiv.innerHTML += `<div style="color:blue;">Sui: ${data.speech}</div>`;
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
};

// Exemple d'initialisation de Three.js
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  suiCanvas.clientWidth / suiCanvas.clientHeight,
  0.1,
  1000
);
const renderer = new THREE.WebGLRenderer({ canvas: suiCanvas });
renderer.setSize(suiCanvas.clientWidth, suiCanvas.clientHeight);

// Ajoutez votre logique Three.js ici (création de Sui, animations, etc.)

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}

animate();
