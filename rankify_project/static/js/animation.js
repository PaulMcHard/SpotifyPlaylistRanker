var scene;
var camera;
var renderer;
var textureLoader;
var texture1;
var geometry;
var sphGeo;
var sphMat;
var sph;
var material;
var mesh;
var light;
var pLight;
var redLight;
var greenLight;
var blueLight;
var velX = 0.001;
var velY = 0.001;
var i = 0;
var firstTime = 0;


function init() {
	//SCENE INSTANTIATION
    scene = new THREE.Scene();

	//CAMERA INSTANTIATION
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 10000);
    camera.position.z = 1000;

	//TEXTURES
    textureLoader = new THREE.TextureLoader();
    texture1 = textureLoader.load("https://cpmmckeown.github.io/spotify-logo.png")
    texture1.wrapS = texture1.wrapT = THREE.MirroredRepeatWrapping;

	//LIGHTS
    light = new THREE.AmbientLight(0xffffff);

    pLight = new THREE.PointLight(0xffffff, 1, 1000);
    pLight.position.set(100, 400, 100);

	//redLight
	redLight = new THREE.SpotLight(0xff0000);
    redLight.position.set(25, 400, 25);
	redLight.castShadow = true;
	redLight.shadow.mapSize.width = 1024;
	redLight.shadow.mapSize.height = 1024;
	redLight.power = 0;

	//greenLight
	greenLight = new THREE.SpotLight(0x00ff00);
    greenLight.position.set(-500, 400, 100);
	greenLight.castShadow = true;
	greenLight.shadow.mapSize.width = 1024;
	greenLight.shadow.mapSize.height = 1024;
	greenLight.power = 0;

	//blue light
	blueLight = new THREE.SpotLight(0x0000ff);
    blueLight.position.set(500, 400, 100);
	blueLight.castShadow = true;
	blueLight.shadow.mapSize.width = 1024;
	blueLight.shadow.mapSize.height = 1024;
	blueLight.power = 0;

	//RENDERER
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);

	//GEOMETRIES
    geometry = new THREE.BoxGeometry(500, 500, 500);
	sphGeo = new THREE.SphereGeometry(50, 50, 50);
	plnGeo = new THREE.PlaneGeometry(1000, 1000); //massive back plane

	//MATERIALS
	//Cube material
    material = new THREE.MeshPhongMaterial({
        color: 0x1db954,
        map: texture1,
        wireframe: false
    });
	//Sphere Material
	sphMat = new THREE.MeshPhongMaterial
	({
		color: 0x1db954,
        map: texture1,
	});
	//Plane Material
	plnMat = new THREE.MeshPhongMaterial
	({
		color: 0x000000, side: THREE.DoubleSide
	})

	//MESHES
	//Cube Mesh
    mesh = new THREE.Mesh(geometry, material);
    mesh.scale.y = 0.01;
    mesh.scale.x = 0.01;
    mesh.scale.z = 0.01;
	//Sphere Mesh
	sph = new THREE.Mesh( sphGeo, sphMat );
	//Plane Mesh
	pln = new THREE.Mesh( plnGeo, plnMat);
	pln.position.set(0, 0, 0);


	//ADDS LIGHTS
    scene.add(light, pLight, redLight, greenLight, blueLight);

	//ADD MESHES
	//scene.add(mesh);
	scene.add(sph);
	scene.add(pln);

	//APPENDS THIS TO WebGLCanvas DIV
    document.getElementById("WebGLCanvas").appendChild(renderer.domElement);

	//ON INIT THE ANIMATION BEGINS
    speed();

}

function animate() {

    var b = document.getElementById('speed').getAttribute('data-value');
    b = b * 10;
	console.log(b);

    requestAnimationFrame(animate);

	//CUBE
    mesh.rotation.x += velX;
    mesh.rotation.y += velY;
	//SPHERE
	sph.rotation.x += velX;
    sph.rotation.y += velY;

	//This allows the cube to change size as the animation loop
	//progresses.
	//THE SMALLER THE DIVISION FACTOR THE MORE THEY GROW
	if (i < 100 && b >= 8) {
		//CUBE
        mesh.scale.z += (b / 800);
        mesh.scale.y += (b / 800);
        mesh.scale.x += (b / 800);
		//SPHERE
		sph.scale.x += (b / 300);
		sph.scale.y += (b / 300);
		sph.scale.z += (b / 300);
        //This prints to the console the current scale
		//handy to let you know the anim loop is working
		//even if you can't see the animation.
		//console.log(mesh.scale.x, mesh.scale.y);
		redLight.power += (b*50);
		redLight.angle += (b/100);
		greenLight.power += (b*50);
		greenLight.angle += (b/200);
		blueLight.power += (b*50);
		blueLight.angle += (b/150);
		//console.log(sph.scale.x, sph.scale.y);
        i++;
		//console.log(i);
    } else if (i < 400 && b >= 8) {
		//CUBE
        mesh.scale.z -= (b / 800);
        mesh.scale.y -= (b / 800);
        mesh.scale.x -= (b / 800);
		//SPHERE
		//THESE VALUES REPRESENT HOW SMALL THE CUBE GETS ON IT'S
		//SHRINK. THE LOWER THE VALUE, THE MORE IT SHRINKS
		//!!! NOTE: NUMBERS HAVE TO BALANCE OR IT WILL GROW/SHRINK INFINITELY !!!///
		sph.scale.x -= (b / 300);
        sph.scale.y -= (b / 300);
		sph.scale.z -= (b / 300);
		redLight.power -= (b*50);
		redLight.angle -= (b/100);
		greenLight.power -= (b*50);
		greenLight.angle -= (b/150);
		blueLight.power -= (b*50);
		blueLight.angle -= (b/150);
    }
    if (i < 100) {
		//CUBE
        mesh.scale.z += (b / 800);
        mesh.scale.y += (b / 800);
        mesh.scale.x += (b / 800);
		//SPHERE
		sph.scale.x += (b / 300);
		sph.scale.y += (b / 300);
		sph.scale.z += (b / 300);
        //This prints to the console the current scale
		//handy to let you know the anim loop is working
		//even if you can't see the animation.
		//console.log(mesh.scale.x, mesh.scale.y);
		//redLight.power += (b*500);
		//redLight.angle += (b*500);
		//console.log(sph.scale.x, sph.scale.y);
        i++;
		//console.log(i);
    } else if (i < 400) {
		//CUBE
        mesh.scale.z -= (b / 800);
        mesh.scale.y -= (b / 800);
        mesh.scale.x -= (b / 800);
		//SPHERE
		//THESE VALUES REPRESENT HOW SMALL THE CUBE GETS ON IT'S
		//SHRINK. THE LOWER THE VALUE, THE MORE IT SHRINKS
		//!!! NOTE: NUMBERS HAVE TO BALANCE OR IT WILL GROW/SHRINK INFINITELY !!!///
		sph.scale.x -= (b / 300);
        sph.scale.y -= (b / 300);
		sph.scale.z -= (b / 300);
		//redLight.power = 0;
    }

	//This sets the minimum size of the cube.
    if (mesh.scale.y < 0.5) {
        i = 0;
    }
	if (sph.scale.y < 0.5)
	{
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
