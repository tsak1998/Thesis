function drawNodes( editor, nodes ){
    
    
    for (a=0; a<nodes.length; a++) {
        
        node = nodes[a];
        
        // check if the node is supported
        dofs = [node.dof_dx, node.dof_dy, node.dof_dz, node.dof_rx, node.dof_ry, node.dof_rz];
        supported = false;
        
        for (j=0; j<dofs.length; j++) {
            
            if( dofs[j]==0){
                supported = true;
                
            };
            j++
        };
        if (supported==false){
            var geometry = new THREE.SphereGeometry( 0.05, 12, 12, 0, Math.PI * 2, 0, Math.PI );
            var node_material = new THREE.MeshStandardMaterial();
            var mesh = new THREE.Mesh( geometry, node_material );
            //mesh.matrixAutoUpdate = false;
            mesh.name = 'Node ' + String(node.nn);
            mesh.userData = {'nn' : node.nn,
                                'type': 'node',
                                'coord_x': node.coord_x,
                                'coord_y' : node.coord_y, 
                                'coord_z' : node.coord_z};

            mesh.userData.dof_dx = 1;
            mesh.userData.dof_dy = 1;
            mesh.userData.dof_dz = 1;
            mesh.userData.dof_rx = 1;
            mesh.userData.dof_ry = 1;
            mesh.userData.dof_rz = 1;
            

            mesh.position.set(node.coord_y, node.coord_z, node.coord_x);
            let label = new makeTextSprite(mesh.userData.nn, );
            label.name = mesh.name
            mesh.add(label)
            editor.execute( new AddObjectCommand( mesh ) );
        }else {
            var geometry = new THREE.BoxGeometry( 0.15, 0.15, 0.15 );
            var node_material = new THREE.MeshStandardMaterial();
            var mesh = new THREE.Mesh( geometry, node_material );
            //mesh.matrixAutoUpdate = false;
            mesh.name = 'Node ' + String(node.nn);
            mesh.userData = {'nn' : node.nn,
                                'type': 'node',
                                'coord_x': node.coord_x,
                                'coord_y' : node.coord_y, 
                                'coord_z' : node.coord_z};

            mesh.userData.dof_dx = node.dof_dx;
            mesh.userData.dof_dy = node.dof_dy;
            mesh.userData.dof_dz = node.dof_dz;
            mesh.userData.dof_rx = node.dof_rx;
            mesh.userData.dof_ry = node.dof_ry;
            mesh.userData.dof_rz = node.dof_rz;

            mesh.position.set(node.coord_x, node.coord_y, node.coord_z);
            let label = new makeTextSprite(mesh.userData.nn, );
            label.name = mesh.name
            mesh.add(label)
            editor.execute( new AddObjectCommand( mesh ) );
        }
   };
};