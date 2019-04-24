/**
 * @author mrdoob / http://mrdoob.com/
 */

Sidebar.PointLoads = function ( editor ) {

	var config = editor.config;
	var signals = editor.signals;
    var strings = editor.strings;
    
    var point_loads = [];


	var container = new UI.Panel();
	container.setBorderTop( '0' );
	container.setPaddingTop( '20px' );
	container.setPaddingBottom( '20px' );

	// load type

	var type = {
		'onNode': 'ON NODE',
		'onMember': 'ON MEMBER'
	};

	
	var loadTypeRow = new UI.Row();
	var loadType = new UI.Select().setWidth( '150px' );
    loadType.setOptions( type );

    loadTypeRow.add( new UI.Text( 'Load Type' ).setWidth( '90px' ) );
	loadTypeRow.add( loadType );

    container.add( loadTypeRow );

    

    //dp/l ratio for the point load on member
    var lengthRatioRow = new UI.Row();
	var lengthRatio = new UI.Select().setWidth( '150px' );

    var lengthRatioRow = new UI.Row();
	var lengthRatio = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' ).onChange( function () {

	} );

	lengthRatioRow.add( new UI.Text( 'Position of Load(x/L)' ).setWidth( '90px' ) );
    lengthRatioRow.add( lengthRatio );

    container.add( lengthRatioRow );

    //Load values (Px,Py,Pz,...)
	var loadRow = new UI.Row();
	var loadInp = new UI.Input( '' ).setLeft( '100px' ).setWidth( '150px' ).onChange( function () {

    } );
    // load.value = 'Px,Py,Pz,Mx,My,Mz'

	loadRow.add( new UI.Text( 'Load Values' ).setWidth( '90px' ) );
    loadRow.add( loadInp );
    
    container.add(loadRow)

	

    
    var buttonRow = new UI.Row();
    
    var btn = new UI.Button( 'Define Load' ).onClick( function () {

        load_values = loadInp.getValue().split(",")
        point_loads.push({'id' : point_loads.length+1,
            'type': loadType.getValue(),
            'c': lengthRatio.getValue(),
            'p_x': parseFloat(load_values[0]),
            'p_y': parseFloat(load_values[1]),
            'p_z': parseFloat(load_values[2]),
            'm_x': parseFloat(load_values[3]),
            'm_y': parseFloat(load_values[4]),
            'm_z': parseFloat(load_values[5])
        });
    
		refreshUI();
		

	} );
	
    

	buttonRow.add( btn );

    container.add( buttonRow );
    var outliner = new UI.Outliner( editor );
	outliner.onChange( function () {

		//ignoreObjectSelectedSignal = true;

		//editor.history.goToState( parseInt( outliner.getValue() ) );

		//ignoreObjectSelectedSignal = false;

    } );
    
    container.add( outliner );

    container.add( new UI.HorizontalRule() );

    var loadIDRow = new UI.Row();
	var loadID = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' ).onChange( function () {

	} );
	

	loadIDRow.add( new UI.Text( 'Load ID' ).setWidth( '90px' ) );
    loadIDRow.add( loadID );

    container.add( loadIDRow )

    var objectRow = new UI.Row();
	var object = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' ).onChange( function () {

	} );
    

	objectRow.add( new UI.Text( 'Node/Member' ).setWidth( '90px' ) );
    objectRow.add( object );

    container.add( objectRow)

	var buttonRow = new UI.Row();
    
    var btn = new UI.Button( 'Add Load' ).onClick( function () {

        // loop for multiple loads and for the load values
        elements = object.getValue().split(",");

        load_id = parseInt(loadID.getValue());
        
        load = point_loads[load_id-1]
        
        for ( var i = 0, l = elements.length; i < l; i ++ ) {

            if (load.c==''){
                name = 'Node '+String( elements[i] );
                obj = editor.scene.getObjectByName( name );
                load_position = [obj.position.x, obj.position.z, obj.position.y] 
                console.log('yel')
            }else{
                name = 'Element '+String( elements[i] );
                obj = editor.scene.getObjectByName( name );
                
                position = obj.geometry.attributes.position.array
                // direction vector
                CXx = (position[3]-position[0])/obj.userData.length
                CYx = (position[5]-position[2])/obj.userData.length
                CZx = (position[4]-position[1])/obj.userData.length
    
                console.log(CXx, CYx, CZx)
                load_position = [position[0]+CXx*load.c*obj.userData.length, position[1]+CZx*load.c*obj.userData.length, position[2] +CYx*load.c*obj.userData.length]
                console.log('yellow')
                console.log(load_position)
            }
            
            // Px
            var point_load = new THREE.Group();
            

            point_load.name = 'Point Load '+String(load_id)

            var material = new THREE.MeshBasicMaterial( {color: 0xffff00} );
            
            
            
            

            if (load.p_x==0) {
               
            } else if (load.p_x>0) {
                var material = new THREE.MeshBasicMaterial( {color: 0xffff00} );
                var geometry = new THREE.ConeGeometry( 0.02, 0.15, 32 );

                var cone = new THREE.Mesh( geometry, material );
                cone.rotation.z = -Math.PI/2;
                cone.position.set( load_position[0]-0.05, load_position[1], load_position[2] );
                var positions = [ load_position[0]-0.05, load_position[1], load_position[2], load_position[0] -1, load_position[1], load_position[2] ];
                line_material = new THREE.LineBasicMaterial( { color: 0x0000ff } );
    
                var geometry = new THREE.BufferGeometry();
    
                // itemSize = 3 because there are 3 values (components) per vertex
    
                geometry.addAttribute( 'position', new THREE.Float32BufferAttribute( positions, 3 ) )
                geometry.computeBoundingSphere();
            
                line = new THREE.Line( geometry, line_material );
    
                point_load.add(line);
                point_load.add(cone);
            } else {
                var material = new THREE.MeshBasicMaterial( {color: 0xffff00} );
                var geometry = new THREE.ConeGeometry( 0.02, 0.15, 32 );
                
                var cone = new THREE.Mesh( geometry, material );
                cone.rotation.z = Math.PI/2;
                cone.position.set( load_position[0]+0.05, load_position[1], load_position[2] );
                var positions = [ load_position[0]+0.05, load_position[1], load_position[2], load_position[0] +1, load_position[1], load_position[2] ];

                line_material = new THREE.LineBasicMaterial( { color: 0x0000ff } );
    
                var geometry = new THREE.BufferGeometry();
    
                // itemSize = 3 because there are 3 values (components) per vertex
    
                geometry.addAttribute( 'position', new THREE.Float32BufferAttribute( positions, 3 ) )
                geometry.computeBoundingSphere();
            
                line = new THREE.Line( geometry, line_material );
    
                point_load.add(line);
                point_load.add(cone);

            };

           

            if (load.p_y==0) {
               
            } else if (load.p_y>0) {
                var material = new THREE.MeshBasicMaterial( {color: 0xffff00} );
                var geometry = new THREE.ConeGeometry( 0.02, 0.15, 32 );
                
                var cone = new THREE.Mesh( geometry, material );
                cone.rotation.x = Math.PI/2;
                cone.rotation.y = Math.PI;
                
                cone.position.set( load_position[0], load_position[1], load_position[2] -0.05 );
                var positions = [ load_position[0], load_position[1], load_position[2] -0.05, load_position[0] , load_position[1], load_position[2]-1 ];
                line_material = new THREE.LineBasicMaterial( { color: 0x0000ff } );
    
                var geometry = new THREE.BufferGeometry();
    
                // itemSize = 3 because there are 3 values (components) per vertex
    
                geometry.addAttribute( 'position', new THREE.Float32BufferAttribute( positions, 3 ) )
                geometry.computeBoundingSphere();
            
                line = new THREE.Line( geometry, line_material );
    
                point_load.add(line)
                point_load.add(cone)
            } else {
                var material = new THREE.MeshBasicMaterial( {color: 0xffff00} );
                var geometry = new THREE.ConeGeometry( 0.02, 0.15, 32 );
                
                var cone = new THREE.Mesh( geometry, material );
                cone.rotation.x = -Math.PI/2;
                cone.rotation.y = -Math.PI;
                cone.position.set( load_position[0], load_position[1], load_position[2]+0.05 );
                var positions = [ load_position[0], load_position[1], load_position[2]+0.05, load_position[0], load_position[1], load_position[2]+1 ];

                line_material = new THREE.LineBasicMaterial( { color: 0x0000ff } );
    
                var geometry = new THREE.BufferGeometry();
    
                // itemSize = 3 because there are 3 values (components) per vertex
    
                geometry.addAttribute( 'position', new THREE.Float32BufferAttribute( positions, 3 ) )
                geometry.computeBoundingSphere();
            
                line = new THREE.Line( geometry, line_material );
    
                point_load.add(line)
                point_load.add(cone)

            };

            
            //mesh.updateMatrix();
            
            editor.execute( new AddObjectCommand( point_load ) );
            
            render();
        };

               
		
		

    } );
    
    
	

	buttonRow.add( btn );

	container.add( buttonRow );
        
    var refreshUI = function () {

		var options = [];
		var enumerator = 1;

		function buildOption( object ) {

			var option = document.createElement( 'div' );
			option.value = object;
			return option;

		}

		( function addObjects( objects ) {

			for ( var i = 0, l = objects.length; i < l; i ++ ) {

                var object = '  ' + String(objects[ i ].id) + '  |  ' + String(objects[ i ].c) + ', ' + String(objects[ i ].p_x)+', '+String(objects[ i ].p_y)+ ', ' + String(objects[ i ].p_z) + ', '+String(objects[ i ].m_x)+', '+String(objects[ i ].m_y)+', '+String(objects[ i ].m_z);
				var option = buildOption( object );
				option.innerHTML = '&nbsp;' + object;

				options.push( option );

			}

        } )( point_loads );
        outliner.setOptions( options );
    };

    refreshUI(); 

	
/*
    var ballGeo = new THREE.SphereGeometry(10,35,35);
    var material = new THREE.MeshPhongMaterial({color: 0xF7FE2E}); 
    var ball = new THREE.Mesh(ballGeo, material);

    var pendulumGeo = new THREE.CylinderGeometry(1, 1, 50, 16);
    ball.updateMatrix();
    pendulumGeo.merge(ball.geometry, ball.matrix);

    var pendulum = new THREE.Mesh(pendulumGeo, material);
    editor.execute( new AddObjectCommand(pendulum) );
*/
	//console.log(Viewport.transformControls.object)
	
	nodes = [];

	buttonRow.add( btn );

    container.add( buttonRow );


    

	return container;

};
