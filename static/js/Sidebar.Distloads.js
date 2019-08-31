Sidebar.DistLoads = function(editor){
	
	var signals = editor.signals;

    var container = new UI.Panel();
	container.setBorderTop( '0' );
	container.setPaddingTop( '20px' );
	container.setPaddingBottom( '20px' );
    
    var directions = {
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
    var startRatioRow = new UI.Row();
    var startRatio = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' )
    

	startRatioRow.add( new UI.Text( 'Start(b/L)' ).setWidth( '90px' ) );
    startRatioRow.add( startRatio );

    container.add( startRatioRow );

    var endRatioRow = new UI.Row();
	var endRatio = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' ).onChange( function () {

	} );

	endRatioRow.add( new UI.Text( 'End(b/L)' ).setWidth( '90px' ) );
    endRatioRow.add( endRatio );

    container.add( endRatioRow );

    //Load values (Px,Py,Pz,...)
	var loadRow = new UI.Row();
	var loadInp = new UI.Input( '' ).setLeft( '100px' ).setWidth( '50px' ).onChange( function () {

    } );
    // load.value = 'Px,Py,Pz,Mx,My,Mz'

	loadRow.add( new UI.Text( 'Load Value' ).setWidth( '90px' ) );
    loadRow.add( loadInp );
    
    container.add(loadRow)

    var objectRow = new UI.Row();
	var object = new UI.Input( '' ).setLeft( '100px' ).setWidth( '100px' ).onChange( function () {

	} );
    

	objectRow.add( new UI.Text( 'Member' ).setWidth( '90px' ) );
    objectRow.add( object );

    container.add( objectRow)

    var buttonRow = new UI.Row();
    
    var btn = new UI.Button( 'Add Load' ).onClick( function () {
        
        elmnts = object.getValue().split(",");
        
        for (j=0;j<elmnts.length;j++){
            
            element = editor.scene.getObjectByName( 'Element '+elmnts[j] );
            nodei = editor.scene.getObjectByName( 'Node '+String(element.userData.nodei) );
            
            l = element.userData.length
            start = parseFloat(startRatio.getValue());
            end = parseFloat(endRatio.getValue());
            xLocal = element.userData.xLocal
            xi = nodei.position.x
            yi = nodei.position.y
            zi = nodei.position.z

            v1 = parseFloat(loadInp.getValue())
            v2 = parseFloat(loadInp.getValue())
            
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
            mesh.userData = {'type': 'd_load',
                            'en': element.userData.en,
                            'p_1_x':0,
                            'p_2_x':0,
                            'p_1_y':0,
                            'p_2_y':0,
                            'p_1_z':v1,
                            'p_2_z':v2,
                            'c': start,
                            'l': end}
            
            mesh.applyMatrix(element.matrix);
            editor.execute( new AddObjectCommand(mesh) );
        }
    });

    buttonRow.add( btn );
    
    container.add( buttonRow );

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
		if ( editor.selected != null){
			signals.objectDeselected.dispatch( editor.selected )
		};
		ignoreObjectSelectedSignal = true;
        valueId = parseInt( outliner.getValue())

		if (valueId == pLoads.id){

        }else{
           editor.selectById( valueId );
           //updateElementProperties(editor.selected.userData)

        }

		ignoreObjectSelectedSignal = false;

	} );

	outliner.onDblClick( function () {
        valueId = parseInt( outliner.getValue())
        if (valueId == pLoads.id){

        }else{
			
		   editor.focusById( valueId );
		   if ( editor.selected != null){
			signals.objectSelected.dispatch( editor.selected )
		};
        }

	} );


   container.add( outliner );


    var pLoads = new THREE.Object3D()
    pLoads.name = 'Dist Loads'
	function refreshUI() {
	    p_loads = []
        for (i=0; i<editor.scene.children.length; i++){
			obj = editor.scene.children[i]
			if (obj.userData.type == 'd_load') {
				p_loads.push( obj );
			}
		};
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



	};
	
	signals.editorCleared.add( refreshUI );

	signals.sceneGraphChanged.add( refreshUI );

	signals.objectChanged.add( function ( object ) {

		var options = outliner.options;

		for ( var i = 0; i < options.length; i ++ ) {

			var option = options[ i ];

			if ( option.value === object.id ) {

				option.inumbererHTML = buildHTML( object );
				return;

			}

		}

	} );

	signals.objectSelected.add( function ( object ) {

	    if (object!=null){

	        if(object.userData.type == 'element'){
                //updateElementProperties(object.userData)
            }
        }
		if ( ignoreObjectSelectedSignal === true ) return;

		outliner.setValue( object !== null ? object.id : null );

	} );
	

	refreshUI();

    return container
};