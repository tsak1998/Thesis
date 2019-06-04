function drawElements( editor, elements ){

    for (i=0; i<elements.length; i++){
        var element = elements[i];
        var nodeI = editor.scene.getObjectByName( 'Node '+ String(element.nodei) );
        var nodeJ = editor.scene.getObjectByName( 'Node '+ String(element.nodej) );
		
        xi = nodeI.position.x
		yi = nodeI.position.y
		zi = nodeI.position.z
		xj = nodeJ.position.x
		yj = nodeJ.position.y
		zj = nodeJ.position.z


		// dummy line for calculations
		helpLine = new THREE.Line3(new THREE.Vector3(xi, yi, zi), new THREE.Vector3(xj, yj, zj))
		length = helpLine.distance()
		dirVector = new THREE.Vector3()
		helpLine.delta( dirVector )
		dirVector.normalize()
		middle = new THREE.Vector3()
		helpLine.delta( middle )
		// helper vector
		helpVector = new THREE.Vector3(0, 1, 0)
		//calculate the desired axis
		if (dirVector.x==0 & dirVector.z==0){
			zLocal = new THREE.Vector3(0,0,1)
			yLocal = new THREE.Vector3(1,0,0)
		} else {
			zLocal = new THREE.Vector3()
			zLocal.crossVectors(dirVector, helpVector)
			yLocal = new THREE.Vector3()
			yLocal.crossVectors(dirVector, zLocal)
		}
		transformMatrix = new THREE.Matrix4()
		transformMatrix.makeBasis(dirVector, yLocal, zLocal)	
		transformMatrix.setPosition(new THREE.Vector3(xi, yi, zi)) 
		
		var positions = [];
		positions.push(0, 0, 0, length, 0, 0)
		var geometry = new THREE.BufferGeometry();
		geometry.addAttribute( 'position', new THREE.Float32BufferAttribute( positions, 3 ) )
		
		line = new THREE.Line( geometry, member_material );
		line.material.linewidth = 6
		line.name = 'Element ' + String(element.en);
		line.userData = {'en' : element.en,
						 'type':  'element',
						 'nodei' : nodeI.userData.nn,
						  'nodej' : nodeJ.userData.nn,
						  'elem_type': 'beam',
						  'length' : length ,
						  'section_id' : element.section_id }
		
		//line.position.set((parseFloat(nodes[0].position.x)+parseFloat(nodes[1].position.x))/2, (parseFloat(nodes[0].position.y)+parseFloat(nodes[1].position.y))/2, (parseFloat(nodes[0].position.z)+parseFloat(nodes[1].position.z))/2)
		
		//let label = new makeTextSprite(line.userData.en, );
		
		//label.name = line.name
		

		x_lbl = (xj-xi)/2
		y_lbl = (zj-zi)/2
		z_lbl = (yj-yi)/2
		//console.log(middle)
		
		line.applyMatrix( transformMatrix )
		
		
		
		editor.execute( new AddObjectCommand( line ) );
		
    }
};