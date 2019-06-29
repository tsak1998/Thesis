/**
 * @author mrdoob / http://mrdoob.com/
 */


Sidebar.Elements = function ( editor ) {

	var config = editor.config;
	var signals = editor.signals;
	var strings = editor.strings;
	var nodeCount = 1;
	var elemCount = 1;

	var container = new UI.Panel();
	container.setBorderTop( '0' );
	container.setPaddingTop( '20px' );

	//count lines and nodes

	
	//labels for objects

	function makeTextSprite( message, parameters )
    {
        if ( parameters === undefined ) parameters = {};
        var fontface = parameters.hasOwnProperty("fontface") ? parameters["fontface"] : "Arial";
        var fontsize = parameters.hasOwnProperty("fontsize") ? parameters["fontsize"] : 70;
        var borderThickness = parameters.hasOwnProperty("borderThickness") ? parameters["borderThickness"] : 4;
        var borderColor = parameters.hasOwnProperty("borderColor") ?parameters["borderColor"] : { r:0, g:0, b:0, a:1.0 };
        var backgroundColor = parameters.hasOwnProperty("backgroundColor") ?parameters["backgroundColor"] : { r:0, g:0, b:200, a:0.5 };
        var textColor = parameters.hasOwnProperty("textColor") ?parameters["textColor"] : { r:0, g:0, b:0, a:1.0 };

        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        context.font = "Bold " + fontsize + "px " + fontface;
        var metrics = context.measureText( message );
        var textWidth = metrics.width;

        context.fillStyle   = "rgba(" + backgroundColor.r + "," + backgroundColor.g + "," + backgroundColor.b + "," + backgroundColor.a + ")";
        context.strokeStyle = "rgba(" + borderColor.r + "," + borderColor.g + "," + borderColor.b + "," + borderColor.a + ")";

        context.lineWidth = borderThickness;

        context.fillStyle = "rgba("+textColor.r+", "+textColor.g+", "+textColor.b+", 1.0)";
        context.fillText( message, borderThickness, fontsize + borderThickness);

        var texture = new THREE.Texture(canvas) 
        texture.needsUpdate = true;

        var spriteMaterial = new THREE.SpriteMaterial( { map: texture, useScreenCoordinates: false } );
        var sprite = new THREE.Sprite( spriteMaterial );
        sprite.scale.set(0.4, 0.4,0.4);
        return sprite;  
    }
	// materials

	node_material = new THREE.MeshStandardMaterial() 
	member_material = new THREE.LineBasicMaterial( { color: 0x0000ff } );

	//element type

	var elemTypeRow = new UI.Row();
	var elemType = new UI.Select().setWidth( '150px' );
	var elemTypeOpt = {
		'beam'  : 'BEAM',
		'truss' : 'TRUSS'
	}
	elemType.setOptions( elemTypeOpt )
	elemTypeRow.add (new UI.Text( 'Element Type' ).setWidth( '90px' ))
	elemTypeRow.add( elemType )
	container.add( elemTypeRow )

	//element section

	var elemSectRow = new UI.Row();
	var elemSect = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

		
	} );
	

	elemSectRow.add( new UI.Text( 'Section ID' ).setWidth( '90px' ) );
	elemSectRow.add( elemSect );

	container.add( elemSectRow );


	// nodes

	var node_iRow= new UI.Row();
	var node_i = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

		
	} );
	
	
	node_iRow.add( new UI.Text( 'Node i' ).setWidth( '90px' ) );
	node_iRow.add( node_i );

	container.add( node_iRow );

	var node_jRow= new UI.Row();
	var node_j = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );
	

	node_jRow.add( new UI.Text( 'Node j' ).setWidth( '90px' ) );
	node_jRow.add( node_j );

	container.add( node_jRow );

	nodes  = [];
	var buttonRow = new UI.Row();
	var btn = new UI.Button( 'Pick Nodes' ).onClick( function () {
		nodes=[]
		{

		//document.addEventListener( "mousedown", onMouseDown, false );
		
		document.addEventListener( "click", onMouseUp, false );
		

	}

	function onMouseUp(event){
		if ( editor.selected == null ) {


		}else if(nodes.length<2) {
			if (nodes[0]==editor.selected){
				
			}else{
				nodes.push(editor.selected)
				if (nodes.length ==1){
					node_i.dom.value = nodes[0].userData.nn}
				else {
					node_j.dom.value = nodes[1].userData.nn}
				
				}
				
			}
		else {
			document.removeEventListener( "click", onMouseUp, false );
			
		}
	}
		
	} );

	buttonRow.add( btn );

	container.add( buttonRow );

	//

	var buttonRow = new UI.Row();
	var btn = new UI.Button( 'Create Element' ).onClick( function () {
		xi = nodes[0].position.x
		yi = nodes[0].position.y
		zi = nodes[0].position.z
		xj = nodes[1].position.x
		yj = nodes[1].position.y
		zj = nodes[1].position.z

		xHelp = xi
		yHelp = 0
		zHelp = zi

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
			zLocal = new THREE.Vector3(0,0,-1)
			yLocal = new THREE.Vector3(-1,0,0)
		} else if(dirVector.x!=0 & dirVector.y!=0 & dirVector.z==0){
			zLocal = new THREE.Vector3()
			zLocal.crossVectors(helpVector, dirVector)
			yLocal = new THREE.Vector3()
			yLocal.crossVectors(dirVector, zLocal)
		} else if(dirVector.x==0 & dirVector.y!=0 & dirVector.z!=0){
			yLocal = new THREE.Vector3()
			yLocal.crossVectors(dirVector, helpVector)
			zLocal = new THREE.Vector3()
			zLocal.crossVectors(yLocal, dirVector)
		}else if(dirVector.y==0){
			zLocal = new THREE.Vector3()
			zLocal.crossVectors(dirVector, helpVector)
			yLocal = new THREE.Vector3()
			yLocal.crossVectors(dirVector, zLocal)
		}else{
			zLocal = new THREE.Vector3()
			zLocal.crossVectors(helpVector, dirVector)
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
		line.name = 'Element ' + String(elemCount);
		line.userData = {'en' : elemCount,
						 'type':  'element',
						 'nodei' : nodes[0].userData.nn,
						  'nodej' : nodes[1].userData.nn,
						  'elem_type': elemType.getValue(),
						  'length' : length ,
						  'section_id' : parseInt(elemSect.getValue()) }
		
		//line.position.set((parseFloat(nodes[0].position.x)+parseFloat(nodes[1].position.x))/2, (parseFloat(nodes[0].position.y)+parseFloat(nodes[1].position.y))/2, (parseFloat(nodes[0].position.z)+parseFloat(nodes[1].position.z))/2)
		
		//let label = new makeTextSprite(line.userData.en, );
		
		//label.name = line.name
		

		//console.log(middle)
		
		line.applyMatrix( transformMatrix )
		
		var axes = new THREE.AxesHelper(2);
		axes.material.linewidth = 5;
		
		axes.applyMatrix(transformMatrix)
		editor.sceneHelpers.add(axes);
		editor.execute( new AddObjectCommand( line ) );
		
		
	
		elemCount+=1
		
		
	
		
	} );
	

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

		ignoreObjectSelectedSignal = true;
        valueId = parseInt( outliner.getValue())

		 if (valueId == Nodes.id){

        }else{
           editor.selectById( valueId );
           updateNodeProperties(editor.selected.userData)

        }

		ignoreObjectSelectedSignal = false;

	} );

	outliner.onDblClick( function () {
        valueId = parseInt( outliner.getValue())
        if (valueId == Nodes.id){

        }else{
           editor.focusById( valueId );
        }

	} );

	container.add( outliner );
	container.add( new UI.Break() );

    var elementIdRow = new UI.Row();
	var elementId = new UI.Number().setPrecision( 0 ).setWidth( '30px' )//.onChange( update );
	elementId.dom.disabled = true;
	elementId.dom.value = '';

	elementIdRow.add( new UI.Text( 'Element Id').setWidth( '90px' ) );
	elementIdRow.add( elementId );

	container.add( elementIdRow );

    var sectIdRow = new UI.Row();
	var sectId = new UI.Number().setPrecision( 0 ).setWidth( '30px' )//.onChange( update );
	sectId.dom.disabled = true;
	sectId.dom.value = '';

	sectIdRow.add( new UI.Text( 'Section Id').setWidth( '90px' ) );
	sectIdRow.add( sectId );

	container.add( elementIdRow );
	// position

	var nodeIRow = new UI.Row();
	var nodeI = new UI.Number().setPrecision( 1 ).setWidth( '50px' )//.onChange( update );
	nodeI.dom.disabled = true;
	nodeI.dom.value = '';
	nodeIRow.add( new UI.Text( 'Node i').setWidth( '90px' ) );
	nodeIRow.add( nodeI );

	container.add(nodeIRow)

	var nodeJRow = new UI.Row();
	var nodeJ = new UI.Number().setPrecision( 1 ).setWidth( '50px' )//.onChange( update );
	nodeJ.dom.disabled = true;
	nodeJ.dom.value = '';
	nodeJRow.add( new UI.Text( 'Node j').setWidth( '90px' ) );
	nodeJRow.add( nodeJ );

    container.add(nodeJRow)

    var lengthRow = new UI.Row();
	var length = new UI.Number().setPrecision( 1 ).setWidth( '50px' )//.onChange( update );
	length.dom.disabled = true;
	length.dom.value = '';
	lengthRow.add( new UI.Text( 'Node j').setWidth( '90px' ) );
	lengthRow.add( length );

    container.add(lengthRow)
    /*
	var nodeXRow = new UI.Row();
	var nodeX = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {



	} );


	nodeXRow.add( new UI.Text('x').setWidth( '90px' ) );
	nodeXRow.add( nodeX );

	container.add( nodeXRow );
	*/

    var array = editor.scene.children
    var len = array.length
    var Nodes = new THREE.Object3D()
    Nodes.name = 'Nodes'
	function refreshUI() {
	    nodes_ = []
        for (i=0; i<len; i++){
			obj = array[i]
			if (obj.userData.type == 'node') {
				nodes_.push( obj );
			}
		}

		var options = [];


		options.push( buildOption( Nodes, false ) );

		( function addObjects( objects, pad ) {

			for ( var i = 0, l = objects.length; i < l; i ++ ) {

				var object = objects[ i ];

				var option = buildOption( object, true );
				option.style.paddingLeft = ( pad * 10 ) + 'px';
				options.push( option );

				// addObjects( object.children, pad + 1 );

			}

		} )
		(nodes_, 1 );

		outliner.setOptions( options );

		if ( editor.selected !== null ) {

			outliner.setValue( editor.selected.id );

		}




	}
	refreshUI();

	return container;

};
