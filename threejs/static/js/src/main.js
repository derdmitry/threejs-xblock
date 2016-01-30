var container, scene, renderer, camera, light, clock, loader;
var WIDTH, HEIGHT, VIEW_ANGLE, ASPECT, NEAR, FAR;

container = document.querySelector('.viewport');

clock = new THREE.Clock();

WIDTH = window.innerWidth,
    HEIGHT = window.innerHeight;

VIEW_ANGLE = 45,
    ASPECT = WIDTH / HEIGHT,
    NEAR = 1,
    FAR = 10000;

scene = new THREE.Scene();

renderer = new THREE.WebGLRenderer({antialias: true});

renderer.setSize(WIDTH, HEIGHT);
renderer.shadowMapEnabled = true;
renderer.shadowMapSoft = true;
renderer.shadowMapType = THREE.PCFShadowMap;
renderer.shadowMapAutoUpdate = true;

container.appendChild(renderer.domElement);

camera = new THREE.PerspectiveCamera(VIEW_ANGLE, ASPECT, NEAR, FAR);

camera.position.set(0, 100, 300);
camera.rotation.x = -Math.PI / 12;

scene.add(camera);

light = new THREE.DirectionalLight(0xffffff);

light.position.set(0, 100, 60);
light.castShadow = true;
light.shadowCameraLeft = -60;
light.shadowCameraTop = -60;
light.shadowCameraRight = 60;
light.shadowCameraBottom = 60;
light.shadowCameraNear = 1;
light.shadowCameraFar = 1000;
light.shadowBias = -.0001
light.shadowMapWidth = light.shadowMapHeight = 1024;
light.shadowDarkness = .7;

scene.add(light);

loader = new THREE.JSONLoader();
var mesh;
if(typeof three_model !== 'undefined'){
    var geomat = loader.parse(three_model);
}else{
    var geomat = loader.parse(car);

}
var plane = new THREE.PlaneGeometry(50, 50);
function load_geometry(geometry, material) {
    mesh = new THREE.Mesh(
        geometry,
        material
    );

    mesh.receiveShadow = true;
    mesh.castShadow = true;
    mesh.rotation.y = -Math.PI / 5;

    scene.add(mesh);
    render();
};
load_geometry(geomat.geometry, geomat.material);
function render() {
    var time = clock.getElapsedTime();
    mesh.rotation.y += .01;

    renderer.render(scene, camera);
    requestAnimationFrame(render);
}