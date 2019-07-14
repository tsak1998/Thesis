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
        elements_ = object.getValue().split(",");

        for ( var j = 0; j < elements_.length; j ++ ) {
            load_id+=1;
            value = parseFloat(loadInp.getValue());
            
            if (loadType.getValue()=='onNode'){
                name = 'Node '+String( elements_[j] );
                console.log(j, elements_[j])
                obj = editor.scene.getObjectByName( name );
                objectId = obj.userData.nn
                xDir = new THREE.Vector3()
                yDir = new THREE.Vector3()
                zDir = new THREE.Vector3()
                obj.matrix.extractBasis( xDir, yDir, zDir)
                m = new THREE.Matrix4()
                m.copyPosition( obj.matrix ) 
                c = 0
                positionOffset = new THREE.Vector3( xDir.x*c*obj.userData.length, xDir.z*c*obj.userData.length, xDir.y*c*obj.userData.length)
                c =99999
            }else{
                name = 'Element '+String( elements_[j] );
                obj = editor.scene.getObjectByName( name );
                objectId = obj.userData.en
                // direction vector
                xDir = new THREE.Vector3()
                yDir = new THREE.Vector3()
                zDir = new THREE.Vector3()
                obj.matrix.extractBasis( xDir, yDir, zDir)
                m = new THREE.Matrix4()
                m.copyPosition( obj.matrix ) 
                c = parseFloat(lengthRatio.getValue())
                positionOffset = new THREE.Vector3( xDir.x*c*obj.userData.length, xDir.y*c*obj.userData.length, xDir.z*c*obj.userData.length)
                
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
                line.applyMatrix(obj.matrix)
                line.position.x += positionOffset.x
                line.position.y += positionOffset.y
                line.position.z += positionOffset.z
                if (direction.getValue()=='y') {
                    if (value>0) {
                        line.rotateZ( -Math.PI/2 )
                    }else{
                        line.rotateZ( Math.PI/2 )
                    }
                } else if (direction.getValue()=='x') {
                    if (value>0) {
                        line.rotateX( Math.PI/2 )
                    }else{
                        line.rotateX( -Math.PI/2 )
                    }
                } else {
                    if (value>0) {
                       
                    }else{
                        line.rotateX( Math.PI )
                    }
                }
                line.userData = {'nn' : objectId,
                            'type': 'p_load',
                            'c': c,
                            'direction' : direction.getValue(),
                            'value': parseFloat(loadInp.getValue())}
                
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
                if (direction.getValue()=='y') {
                    if (value>0) {
                        line.rotateY( -Math.PI/2 )
                    }else{
                        line.rotateY( Math.PI/2 )
                    }
                } else if (direction.getValue()=='x') {
                    if (value>0) {
                       
                    }else{
                        line.rotateX( Math.PI )
                    }
                } else {
                    if (value>0) {
                        line.rotateX( Math.PI/2 )
                    }else{
                        line.rotateX( -Math.PI/2 )
                    }
                }
                line.userData = {'nn' : objectId,
                                'type': 'p_moment',
                                'c': c,
                                'direction' : direction.getValue(),
                                'value': parseFloat(loadInp.getValue())}
            }
            
            editor.execute( new AddObjectCommand(line) )
            console
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
    
    function buildOption( object, draggable ) {

		var option = document.createElement( 'div' );
		option.draggable = draggable;
		option.innerHTML = buildHTML( object );
		option.value = object.id;

		return option;

	}

	function escapeHTML( html ) {

		return html
			.replace( /&/g, '&amp;' )
			.replace( /"/g, '&quot;' )
			.replace( /'/g, '&#39;' )
			.replace( /</g, '&lt;' )
			.replace( />/g, '&gt;' );

	}

	function getMaterialName( material ) {

		if ( Array.isArray( material ) ) {

			var array = [];

			for ( var i = 0; i < material.length; i ++ ) {

				array.push( material[ i ].name );

			}

			return array.join( ',' );

		}

		return material.name;

	}

	function getScript( uuid ) {

		if ( editor.scripts[ uuid ] !== undefined ) {

			return ' <span class="type Script"></span>';

		}

		return '';

	}

	var ignoreObjectSelectedSignal = false;

	function buildHTML( object ) {

		var html = '<span class="type ' + object.type + '"></span> ' + escapeHTML( object.name );

		if ( object instanceof THREE.Mesh ) {

			var geometry = object.geometry;
			var material = object.material;

			html += ' <span class="type ' + geometry.type + '"></span> ' + escapeHTML( geometry.name );
			html += ' <span class="type ' + material.type + '"></span> ' + escapeHTML( getMaterialName( material ) );

		}

		html += getScript( object.uuid );

		return html;

	}

	var outliner = new UI.Outliner( editor );
	outliner.setId( 'outliner' );
	outliner.onChange( function () {

		ignoreObjectSelectedSignal = true;
        valueId = parseInt( outliner.getValue())

		 if (valueId == pLoads.id){

        }else{
           editor.selectById( valueId );
           updatePloadProperties(editor.selected.userData)

        }

		ignoreObjectSelectedSignal = false;

	} );

	outliner.onDblClick( function () {
        valueId = parseInt( outliner.getValue())
        if (valueId == pLoads.id){

        }else{
           editor.focusById( valueId );
        }

	} );

	container.add( outliner );
	container.add( new UI.Break() );


    /*
	var nodeXRow = new UI.Row();
	var nodeX = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {



	} );


	nodeXRow.add( new UI.Text('x').setWidth( '90px' ) );
	nodeXRow.add( nodeX );

	container.add( nodeXRow );
	*/


    var pLoads = new THREE.Object3D()
    pLoads.name = 'Point Loads'
	function refreshUI() {
	    p_loads = []
        for (i=0; i<editor.scene.children.length; i++){
			obj = editor.scene.children[i]
			if (obj.userData.type == 'p_load') {
				p_loads.push( obj );
			}
		}
		var camera = editor.camera;
		var scene = editor.scene;

		var options = [];


		options.push( buildOption( pLoads, false ) );

		( function addObjects( objects, pad ) {

			for ( var i = 0, l = objects.length; i < l; i ++ ) {

				var object = objects[ i ];

				var option = buildOption( object, true );
				option.style.paddingLeft = ( pad * 10 ) + 'px';
				options.push( option );

				// addObjects( object.children, pad + 1 );

			}

		} )
		(p_loads, 1 );

		outliner.setOptions( options );

		if ( editor.selected !== null ) {

			outliner.setValue( editor.selected.id );

		}

		if ( scene.background ) {

			//backgroundColor.setHexValue( scene.background.getHex() );

		}



	}

	var nodeIdRow = new UI.Row();
	var nodeId = new UI.Number().setPrecision( 0 ).setWidth( '30px' )//.onChange( update );
	nodeId.dom.disabled = true;
	nodeId.dom.value = '';

	nodeIdRow.add( new UI.Text( 'Node Id').setWidth( '90px' ) );
	nodeIdRow.add( nodeId );

	container.add( nodeIdRow );

	// position

	var objectPositionRow = new UI.Row();
	var objectPositionX = new UI.Number().setPrecision( 3 ).setWidth( '50px' )//.onChange( update );
	objectPositionX.dom.disabled = true;
	objectPositionX.dom.value = '';
	var objectPositionY = new UI.Number().setPrecision( 3 ).setWidth( '50px' )//.onChange( update );
	objectPositionY.dom.disabled = true;
	objectPositionY.dom.value = '';
	var objectPositionZ = new UI.Number().setPrecision( 3 ).setWidth( '50px' )//.onChange( update );
    objectPositionZ.dom.disabled = true;
    objectPositionZ.dom.value = '';
	objectPositionRow.add(  new UI.Text( 'Coordinates').setWidth( '90px' ) );
	objectPositionRow.add( objectPositionX, objectPositionY, objectPositionZ );

    container.add(objectPositionRow)

    //dofs

    var dofsRow = new UI.Row();
	var dofX = new UI.Number().setPrecision( 0 ).setWidth( '30px' )//.onChange( update );
	dofX.dom.disabled = true;
	dofX.max = 1;
	dofX.min = 0;
	dofX.dom.value = '';
	var dofY = new UI.Number().setPrecision( 1 ).setWidth( '30px' )//.onChange( update );
	dofY.dom.disabled = true;
	dofY.max = 1;
	dofY.min = 0;
	dofY.dom.value = '';
	var dofZ = new UI.Number().setPrecision( 1 ).setWidth( '30px' )//.onChange( update );
    dofZ.dom.disabled = true;
    dofZ.max = 1;
	dofZ.min = 0;
	dofZ.dom.value = '';
    var dofRX = new UI.Number().setPrecision( 1 ).setWidth( '30px' )//.onChange( update );
	dofRX.dom.disabled = true;
    dofRX.max = 1;
	dofRX.min = 0;
	dofRX.dom.value = '';
	var dofRY = new UI.Number().setPrecision( 1 ).setWidth( '30px' )//.onChange( update );
	dofRY.dom.disabled = true;
	dofRY.max = 1;
	dofRY.min = 0;
	dofRY.dom.value = '';
	var dofRZ = new UI.Number().setPrecision( 1 ).setWidth( '30px' )//.onChange( update );
    dofRZ.dom.disabled = true;
    dofRZ.max = 1;
	dofRZ.min = 0;
	dofRZ.dom.value = '';
	dofsRow.add(  new UI.Text( 'Dofs').setWidth( '90px' ) );
	dofsRow.add( dofX, dofY, dofZ, dofRX, dofRY, dofRZ);

    container.add(dofsRow)

    refreshUI();

    var updatePloadProperties = function(values){
        nodeId.dom.value = values.nn
        objectPositionX.dom.value = values.coord_x
        objectPositionY.dom.value = values.coord_y
        objectPositionZ.dom.value = values.coord_z
        dofX.dom.value = values.dof_dx
        dofY.dom.value = values.dof_dy
        dofZ.dom.value = values.dof_dz
        dofRX.dom.value = values.dof_rx
        dofRY.dom.value = values.dof_ry
        dofRZ.dom.value = values.dof_rz
    }

    signals.editorCleared.add( refreshUI );

	signals.sceneGraphChanged.add( refreshUI );

	signals.objectChanged.add( function ( object ) {

		var options = outliner.options;

		for ( var i = 0; i < options.length; i ++ ) {

			var option = options[ i ];

			if ( option.value === object.id ) {

				option.innerHTML = buildHTML( object );
				return;

			}

		}

	} );

	signals.objectSelected.add( function ( object ) {

	    if (object!=null){

	        if(object.userData.type == 'node'){
                updatePloadProperties(object.userData)
            }
        }
		if ( ignoreObjectSelectedSignal === true ) return;

		outliner.setValue( object !== null ? object.id : null );

	} );

	function updateRenderer() {

		createRenderer( THREE.WebGLRenderer, true, false, false, false);

	}

	function createRenderer( type, antialias, shadows, gammaIn, gammaOut ) {



		var renderer = new rendererTypes[ type ]( { antialias: antialias} );
		renderer.gammaInput = gammaIn;
		renderer.gammaOutput = gammaOut;
		if ( shadows && renderer.shadowMap ) {

			renderer.shadowMap.enabled = true;
			// renderer.shadowMap.type = THREE.PCFSoftShadowMap;

		}

		signals.rendererChanged.dispatch( renderer );

	}

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
