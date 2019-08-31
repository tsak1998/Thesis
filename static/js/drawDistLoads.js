function drawDistLoads( editor, distLoads ){
    for (a=0; a<distLoads.length; a++){
        var distLoad = distLoads[a];
		     
        element = editor.scene.getObjectByName( 'Element '+distLoad.en );
        nodei = editor.scene.getObjectByName( 'Node '+String(element.userData.nodei) );
        
        l = element.userData.length
        start = distLoad.c;
        end = distLoad.l;
        xLocal = element.userData.xLocal
        xi = nodei.position.x
        yi = nodei.position.y
        zi = nodei.position.z
           
        p1 = new THREE.Vector2(l*start, 0);
        p2 = new THREE.Vector2(l*start, 1);
        t1 = new THREE.Vector2(l*end, 1);
        t2 = new THREE.Vector2(l*end, 0);
        
        var loadShape = new THREE.Shape([p1, p2, t1, t2]);     
    
        var geometry = new THREE.ShapeGeometry( loadShape );
        var material = new THREE.MeshBasicMaterial({'color': 0xD3D3D3,
                                                    'transparent':true,
                                                    'opacity': 0.5,
                                                    'side': THREE.DoubleSide});
                                
        var mesh = new THREE.Mesh( geometry, material );
        mesh.name = 'Distload' + String(a)
        mesh.userData = {'type': 'd_load',
                        'en': distLoad.en,
                        'p_1_x':0,
                        'p_2_x':0,
                        'p_1_y':0,
                        'p_2_y':0,
                        'p_1_z':distLoad.p_1_z,
                        'p_2_z':distLoad.p_2_z,
                        'c': distLoad.c,
                        'l': distLoad.l}
        
        mesh.applyMatrix(element.matrix);
        editor.execute( new AddObjectCommand(mesh) );
        
   
		
    }
};