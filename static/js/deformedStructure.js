function drawDeformedStructure(nodal_displ, local_displ){
    for (i=1; i<9; i++){
        elmnt = editor.scene.getObjectByName( 'Element '+String(i) );
        node_i = editor.scene.getObjectByName( 'Node '+String(elmnt.userData.nodei) )
        node_j = editor.scene.getObjectByName( 'Node '+String(elmnt.userData.nodej) )
        for (j=0; j<8; j++){
            if (nodal_displ[j].number == node_i.userData.nn){
                node_i_d = nodal_displ[j]
            } else if (nodal_displ[j].number == node_j.userData.nn){
                node_j_d = nodal_displ[j]
            }  
        };
        x1 = node_i.userData.coord_y + 3*node_i_d.uy
        y1 = node_i.userData.coord_z + 3*node_i_d.uz
        z1 = node_i.userData.coord_x + 3*node_i_d.ux

        x2 = node_j.userData.coord_y + 3*node_j_d.uy
        y2 = node_j.userData.coord_z + 3*node_j_d.uz
        z2 = node_j.userData.coord_x + 3*node_j_d.ux

        helpLine = new THREE.Line3(new THREE.Vector3(x1, y1, z1), new THREE.Vector3(x2, y2, z2))
        length = helpLine.distance()
        
		dirVector = new THREE.Vector3()
		helpLine.delta( dirVector )
		dirVector.normalize()
		middle = new THREE.Vector3()
        helpLine.delta( middle )
        
        matrixTemp = transform( x1, y1, z1, x2, y2, z2, 0, length )

		dirVector1 = new THREE.Vector3(matrixTemp.elements[0],matrixTemp.elements[3],matrixTemp.elements[6])
		dirVector2 = new THREE.Vector3(matrixTemp.elements[1],matrixTemp.elements[4],matrixTemp.elements[7])
		dirVector3 = new THREE.Vector3(matrixTemp.elements[2],matrixTemp.elements[5],matrixTemp.elements[8])

        //transformMatrix.makeBasis(dirVector, yLocal, zLocal)
        transformMatrix = new THREE.Matrix4()
		transformMatrix.makeBasis(dirVector1, dirVector2, dirVector3)	
        transformMatrix.setPosition(new THREE.Vector3(x1, y1, z1))
        
        d = local_displ[elmnt.userData.en]
        var vertices = [new THREE.Vector3(0,0,0),
                        
                        new THREE.Vector3(length,0,0)];
        
        var curve = new THREE.CatmullRomCurve3( vertices );
        var points = curve.getPoints( 50 );

        
       
        
        var geometry = new THREE.BufferGeometry().setFromPoints( points );
        line = new THREE.Line( geometry, new THREE.LineBasicMaterial({'color' : 0xff0000}) );
        line.applyMatrix( transformMatrix )
        editor.sceneHelpers.add( line )
    }
}

function transform( xi, yi, zi, xj, yj, zj, bt, length ) {

    var mt3 = new THREE.Matrix3();
   
    var xl = xj - xi;
    var yl = yj - yi;
    var zl = zj - zi;

    var cx = xl / length;
    var cy = yl / length;
    var cz = zl / length;
    
    coa = Math.cos( bt );
    sia = -Math.pow( Math.pow( 1 - coa, 2 ) ,0.5 );

    var up = Math.pow ( Math.pow( cx,2 ) + Math.pow( cz, 2 ) ,0.5 );

    var m11, m12, m13, m21, m22, m23, m31, m32, m33

    if (up !== 0 )
    {
        m11 = cx;
        m12 = cy;
        m13 = cz;
        m21 = (-cx * cy * coa - cz * sia) / up;
        m22 = up * coa;
        m23 = (-cy * cz * coa + cx * sia) / up;
        m31 = (cx * cy * sia - cz * coa) / up;
        m32 = -up * sia;
        m33 = (cy * cz * sia + cx * coa) / up;
    } else {
        m11 = 0;
        m12 = cy;
        m13 = 0;
        m21 = -cy * coa;
        m22 = 0;
        m23 = sia;
        m31 = cy * sia;
        m32 = 0;
        m33 = coa;
        }  

    mt3.set( m11, m12, m13,
             m21, m22, m23,
             m31, m32, m33);

    return mt3;
}