var scene;
var camera;
var renderer;
var textureLoader;
var texture1;
var geometry;
var material;
var mesh;
var light;
var pLight;
var velX = 0.001;
var velY = 0.001;
var i = 0;
var firstTime = 0;




function init() {

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 10000);
    camera.position.z = 1000;

    textureLoader = new THREE.TextureLoader();
    texture1 = textureLoader.load("https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Spotify_logo_without_text.svg/2000px-Spotify_logo_without_text.svg.png")
    texture1.wrapS = texture1.wrapT = THREE.RepeatWrapping;

    light = new THREE.AmbientLight(0xffffff);
    pLight = new THREE.PointLight(0xffffff, 1, 1000);
    pLight.position.set(25, 400, 25);

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);

    geometry = new THREE.BoxGeometry(500, 500, 500);
    material = new THREE.MeshPhongMaterial({
        color: 0x1db954,
        map: texture1,
        wireframe: false
    });
    mesh = new THREE.Mesh(geometry, material);
    mesh.scale.y = 0.01;
    mesh.scale.x = 0.01;
    mesh.scale.z = 0.01;
    scene.add(light, pLight);
    scene.add(mesh);



    document.getElementById("WebGLCanvas").appendChild(renderer.domElement);

    speed();

}

function animate() {

    var b = document.getElementById('speed').getAttribute('data-value');
    b = b * 10;
    requestAnimationFrame(animate);

    mesh.rotation.x += velX;
    mesh.rotation.y += velY;

    if (i < 100) {
        mesh.scale.z += (b / 1000);
        mesh.scale.y += (b / 1000);
        mesh.scale.x += (b / 1000);
        // console.log(mesh.scale.x, mesh.scale.y);
        i++;
    } else if (i < 400) {
        mesh.scale.z -= (b / 1000);
        mesh.scale.y -= (b / 1000);
        mesh.scale.x -= (b / 1000);
    }
    if (mesh.scale.y < 0.01) {
        i = 0;
    }

    renderer.render(scene, camera);

}


function speed() {

    var b = document.getElementById("speed").getAttribute('data-value');
    b = b * 10;
    if (firstTime == 0) {
        animate();
        velX = (b / 100);
        velY = (b / 100);
        firstTime++;
    } else {
        velX = (b / 100);
        velY = (b / 100);
    }
}
