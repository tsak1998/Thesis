function drawElements( editor, elements ){
    for (a=0; a<elements.length; a++){
		var element = elements[a];
		
        var node_I = editor.scene.getObjectByName( 'Node '+ String(element.nodei) );
        var node_J = editor.scene.getObjectByName( 'Node '+ String(element.nodej) );
        xi = node_I.position.x
		yi = node_I.position.y
		zi = node_I.position.z
		xj = node_J.position.x
		yj = node_J.position.y
		zj = node_J.position.z


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
		} else if(dirVector.y==0){
			zLocal = new THREE.Vector3()
			zLocal.crossVectors(helpVector, dirVector)
			yLocal = new THREE.Vector3()
			yLocal.crossVectors(dirVector, zLocal)
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
		
		var xm = (xi + xj) / 2;
        var ym = (yi + yj) / 2;
        var zm = (zi + zj) / 2;

		var arrowHelper;
        var localAxes = new THREE.Object3D();
        var origin = new THREE.Vector3( xm, ym, zm );        
        var alength = 0.5;
		var hex;

		axesMatrix = new THREE.Matrix4()
		axesMatrix.makeBasis(dirVector, yLocal, zLocal)	
		axesMatrix.setPosition(new THREE.Vector3(xm, ym, zm)) 
		
        hex = 0xff0000;
        arrowHelper = new THREE.ArrowHelper( dirVector, origin, alength, hex );
        localAxes.add ( arrowHelper );
         
        hex = 0x0000ff;
        arrowHelper = new THREE.ArrowHelper( yLocal, origin, alength, hex );
        localAxes.add ( arrowHelper );

        //var yDir = new THREE.Vector3().crossVectors( xDir, zDir );
       
        hex = 0x00ff00;
        arrowHelper = new THREE.ArrowHelper( zLocal, origin, alength, hex );
		localAxes.add ( arrowHelper );
		//axes matrix
		
		

		line = new THREE.Line( geometry, new THREE.LineBasicMaterial({'color' : 0x404040}) );
		
		line.material.linewidth = 1
		line.name = 'Element ' + String(element.en);
		localAxes.name = line.name+'axis';
		line.userData = {'en' : element.en,
						 'type':  'element',
						 'nodei' : node_I.userData.nn,
						  'nodej' : node_J.userData.nn,
						  'elem_type': 'beam',
						  'length' : length ,
						  'section_id' : element.section_id,
						  'fixity_dx_i': 0,
						  'fixity_dy_i': 0,
						  'fixity_dz_i': 0,
						  'fixity_rx_i': 0,
						  'fixity_ry_i': 0,
						  'fixity_rz_i': 0,
						  'fixity_dx_j': 0,
						  'fixity_dy_j': 0,
						  'fixity_dz_j': 0,
						  'fixity_rx_j': 0,
						  'fixity_ry_j': 0,
						  'fixity_rz_j': 0,

						  'label_position' : new THREE.Vector3( xm, ym, zm),
						  'xLocal' : dirVector,
						  'yLocal' : yLocal,
						  'zLocal': zLocal,

						 };

		
	
		line.applyMatrix( transformMatrix )
		editor.execute( new AddObjectCommand( line ) );
		


		
    }
};