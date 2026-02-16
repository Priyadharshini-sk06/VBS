let scene, camera, renderer, mixer, clock;
let avatar;
let recognition;

const SIGN_MAP = {
  "hello": "hello",
  "explain": "explain",
  "architecture": "architecture",
  "project": "project"
};

init3D();
initSpeech();

function init3D() {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(45, window.innerWidth / 420, 0.1, 1000);
  camera.position.set(0, 1.6, 3);

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, 420);
  document.getElementById("avatarContainer").appendChild(renderer.domElement);

  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(2, 5, 5);
  scene.add(light);

  clock = new THREE.Clock();

  const loader = new THREE.GLTFLoader();
  loader.load("/static/avatar/model.glb", (gltf) => {
    avatar = gltf.scene;
    mixer = new THREE.AnimationMixer(avatar);
    scene.add(avatar);
    animate();
  });
}

function animate() {
  requestAnimationFrame(animate);
  if (mixer) mixer.update(clock.getDelta());
  renderer.render(scene, camera);
}

function playSign(word) {
  const signLang = document.getElementById("signLang").value;
  const file = SIGN_MAP[word];

  if (file) {
    loadAnimation(`/static/avatar/animations/${signLang}/${file}.glb`);
  } else {
    spellWord(word);
  }
}

function loadAnimation(path) {
  const loader = new THREE.GLTFLoader();
  loader.load(path, (gltf) => {
    const action = mixer.clipAction(gltf.animations[0]);
    action.reset();
    action.play();
  });
}

function spellWord(word) {
  [...word.toUpperCase()].forEach((letter, i) => {
    setTimeout(() => {
      loadAnimation(`/static/avatar/animations/asl/alphabet/${letter}.glb`);
    }, i * 700);
  });
}

function initSpeech() {
  recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.continuous = true;

  recognition.onresult = (event) => {
    const text = event.results[event.results.length - 1][0].transcript;
    document.getElementById("transcript").innerText = text;

    text.toLowerCase().split(" ").forEach(playSign);
  };
}

function startListening() {
  recognition.lang = document.getElementById("spokenLang").value;
  recognition.start();
}

function stopListening() {
  recognition.stop();
}
