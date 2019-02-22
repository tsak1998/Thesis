let cameraWorldPosition = new THREE.Vector3();
let spriteWorldPosition = new THREE.Vector3();
let spriteWorldScale = new THREE.Vector3();

export default function(sprite, renderer, camera) {
	if (renderer.domElement.width && renderer.domElement.height && sprite.material.map.height) {
		sprite.getWorldPosition(spriteWorldPosition);
		camera.getWorldPosition(cameraWorldPosition);
		let worldDistanceBetweenSpriteAndCamera = spriteWorldPosition.distanceTo(cameraWorldPosition);
		let xxx = 2 * Math.tan(THREE.Math.degToRad(camera.fov) / 2) * worldDistanceBetweenSpriteAndCamera;
		// todo: camera.getEffectiveFOV()
		if (xxx) {
			sprite.getWorldScale(spriteWorldScale);
			let spriteHeightInPixels = spriteWorldScale.y * renderer.domElement.height / xxx;
			if (spriteHeightInPixels) {
				return Math.round(spriteHeightInPixels / sprite.material.map.height);
			}
		}
	}
	return 0;
}
