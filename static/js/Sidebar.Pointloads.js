/**
 * @author mrdoob / http://mrdoob.com/
 */

Sidebar.PointLoads = function ( editor ) {

	var config = editor.config;
	var signals = editor.signals;
    var strings = editor.strings;
    
    var point_loads = [];

    var load_id = 0;


	var container = new UI.Panel();
	container.setBorderTop( '0' );
	container.setPaddingTop( '20px' );
	container.setPaddingBottom( '20px' );

	// load on where

	var type = {
		'onNode': 'ON NODE',
		'onMember': 'ON MEMBER'
	};

	
	var loadTypeRow = new UI.Row();
	var loadType = new UI.Select().setWidth( '150px' );
    loadType.setOptions( type );

    loadTypeRow.add( new UI.Text( 'On' ).setWidth( '90px' ) );
	loadTypeRow.add( loadType );

    container.add( loadTypeRow );

    //load type (moment, force)
    var type2 = {
		'load': 'LOAD',
		'moment': 'MOMENT'
	};

	
	var loadTypeRow2 = new UI.Row();
	var loadType2 = new UI.Select().setWidth( '150px' );
    loadType2.setOptions( type2 );

    loadTypeRow2.add( new UI.Text( 'Load Type' ).setWidth( '90px' ) );
	loadTypeRow2.add( loadType2 );

    container.add( loadTypeRow2 );
    //load direction
    var directions = {
		'x': 'X',
        'y': 'Y',
        'z': 'Z'
	};

	
	var directionRow = new UI.Row();
	var direction = new UI.Select().setWidth( '150px' );
    direction.setOptions( directions );

    directionRow.add( new UI.Text( 'Direction' ).setWidth( '90px' ) );
	directionRow.add( direction );

    container.add( directionRow );
    

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

	loadRow.add( new UI.Text( 'Load Value' ).setWidth( '90px' ) );
    loadRow.add( loadInp );
    
    container.add(loadRow)

    var objectRow = new UI.Row();
	var object = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' ).onChange( function () {

	} );
    

	objectRow.add( new UI.Text( 'Node/Member' ).setWidth( '90px' ) );
    objectRow.add( object );

    container.add( objectRow)

    var buttonRow = new UI.Row();
    
    var btn = new UI.Button( 'Add Load' ).onClick( function () {
        elements = object.getValue().split(",");

        for ( var i = 0, l = elements.length; i < l; i ++ ) {
            load_id+=1;
            
            if (loadType.getValue()=='onNode'){
                name = 'Node '+String( elements[i] );
                obj = editor.scene.getObjectByName( name );
                xDir = new THREE.Vector3()
                yDir = new THREE.Vector3()
                zDir = new THREE.Vector3()
                obj.matrix.extractBasis( xDir, yDir, zDir)
                m = new THREE.Matrix4()
                m.copyPosition( obj.matrix ) 
                c = 0
                positionOffset = new THREE.Vector3( xDir.x*c*obj.userData.length, xDir.z*c*obj.userData.length, xDir.y*c*obj.userData.length)
            }else{
                name = 'Element '+String( elements[i] );
                obj = editor.scene.getObjectByName( name );
                
                // direction vector
                xDir = new THREE.Vector3()
                yDir = new THREE.Vector3()
                zDir = new THREE.Vector3()
                obj.matrix.extractBasis( xDir, yDir, zDir)
                m = new THREE.Matrix4()
                m.copyPosition( obj.matrix ) 
                c = parseFloat(lengthRatio.getValue())
                positionOffset = new THREE.Vector3( xDir.x*c*obj.userData.length, xDir.z*c*obj.userData.length, xDir.y*c*obj.userData.length)
                
            }
            
            
            
            
            if (loadType2.getValue()=='load') {
                
             
                var positions = [0, 0, 0, -0.07, -0.05, 0, 0.07, -0.05, 0, 0, 0, 0, 0, -1, 0];
                var material = new THREE.LineBasicMaterial({
                    color: 0x0000ff
                });
                
                var geometry = new THREE.BufferGeometry();

                // itemSize = 3 because there are 3 values (components) per vertex

                geometry.addAttribute( 'position', new THREE.Float32BufferAttribute( positions, 3 ) )
                geometry.computeBoundingSphere();
                
                line = new THREE.Line( geometry, member_material );
                line.name = 'Point Load '+String(load_id)
                line.material.linewidth = 3
                line.applyMatrix(m)
                line.position.x += positionOffset.x
                line.position.y += positionOffset.y
                line.position.z += positionOffset.z
                if (direction.getValue()=='x') {
                //  block of code to be executed if condition1 is true
                } else if (direction.getValue()=='y') {
                //  block of code to be executed if the condition1 is false and condition2 is true
                } else {
                //  block of code to be executed if the condition1 is false and condition2 is false
                }
                editor.execute( new AddObjectCommand(line) )
            } else {
                var curve = new THREE.EllipseCurve(
                    0, 0,             // ax, aY
                    0.2, 0.2,            // xRadius, yRadius
                    0,  Math.PI, // aStartAngle, aEndAngle
                    true             // aClockwise
                );
                var points = curve.getSpacedPoints( 30 );
                t = points.length
                end = points[t-1]
                
                points.push(new THREE.Vector2(-0.13, -0.05))
                points.push(new THREE.Vector2(-0.27, -0.05))
                points.push(new THREE.Vector2(end.x, end.y))
                var geometry = new THREE.BufferGeometry().setFromPoints( points );
                var material = new THREE.LineBasicMaterial( { color : 0xff0000 } );
                var line = new THREE.Line( geometry, material );
                line.name = 'Moment Load '+String(load_id)
                line.applyMatrix(m)
                line.position.x += positionOffset.x
                line.position.y += positionOffset.y
                line.position.z += positionOffset.z
                editor.execute( new AddObjectCommand(line) )
            }
               
            
        }

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
