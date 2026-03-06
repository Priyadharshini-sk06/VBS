let scene, camera, renderer, mixer, clock;

function initAvatar() {

    const canvas = document.getElementById("avatarCanvas");

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(45, canvas.clientWidth/canvas.clientHeight, 0.1, 1000);
    camera.position.set(0, 1.4, 3);

    renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        antialias:true,
        alpha:true
    });

    renderer.setSize(canvas.clientWidth, canvas.clientHeight);

    const hemi = new THREE.HemisphereLight(0xffffff,0x444444,1.5);
    scene.add(hemi);

    const dir = new THREE.DirectionalLight(0xffffff,1);
    dir.position.set(0,5,5);
    scene.add(dir);

    clock = new THREE.Clock();

    const loader = new THREE.GLTFLoader();

    loader.load("/static/avatar/model.glb", function(gltf){

        const model = gltf.scene;

        model.scale.set(1.6,1.6,1.6);
        model.position.set(0,-1,0);

        scene.add(model);

        window.avatarMixer = mixer;
        console.log("AVATAR LOADED");

    }, undefined, function(error){
        console.error("MODEL ERROR:", error);
    });

    animate();
}

function animate(){
    requestAnimationFrame(animate);

    if(mixer){
        mixer.update(clock.getDelta());
    }

    renderer.render(scene,camera);
}
function playSignAnimation(path){

    const loader = new THREE.GLTFLoader();

    loader.load(path, function(gltf){

        if(!gltf.animations.length){
            console.log("No animation in file");
            return;
        }

        const clip = gltf.animations[0];

        // 🔥 IMPORTANT: apply animation to SAME avatar
        const action = mixer.clipAction(clip);
        action.reset();
        action.setLoop(THREE.LoopOnce);
        action.clampWhenFinished = true;
        action.play();

        console.log("Playing:", path);

    }, undefined, function(e){
        console.error("Animation load error", e);
    });
}

window.testA = function(){
    playSignAnimation("/static/avatar/ASL/alphabet/A.glb");
}

window.initAvatar = initAvatar;

// let scene, camera, renderer;

// function initAvatar() {
//     const canvas = document.getElementById("avatarCanvas");

//     scene = new THREE.Scene();
//     camera = new THREE.PerspectiveCamera(35, canvas.clientWidth/canvas.clientHeight, 0.1, 1000);
//     camera.position.z = 5;

//     renderer = new THREE.WebGLRenderer({ canvas: canvas });
//     renderer.setSize(canvas.clientWidth, canvas.clientHeight);

//     const geometry = new THREE.BoxGeometry();
//     const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
//     const cube = new THREE.Mesh(geometry, material);

//     scene.add(cube);

//     function animate() {
//         requestAnimationFrame(animate);
//         cube.rotation.y += 0.01;
//         renderer.render(scene, camera);
//     }

//     animate();
// }
