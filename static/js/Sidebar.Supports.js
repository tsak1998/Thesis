/**
 * @author mrdoob / http://mrdoob.com/
 */


Sidebar.Supports = function ( editor ) {

	var config = editor.config;
	var signals = editor.signals;
	var strings = editor.strings;

	var container = new UI.Panel();
	container.setBorderTop( '0' );
	container.setPaddingTop( '20px' );

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

	//dofs radio buttons


	var dofXRow = new UI.Row();
	var dofX = new UI.Checkbox();
	dofX.dom.id = 'dx';

	dofXRow.add( new UI.Text( 'Dx' ).setWidth( '90px' ) );
	dofXRow.add( dofX );

	container.add( dofXRow );

	var dofYRow = new UI.Row();
	var dofY = new UI.Checkbox();
	dofY.dom.id = 'dy';

	dofYRow.add( new UI.Text( 'Dy' ).setWidth( '90px' ) );
	dofYRow.add( dofY );

	container.add( dofYRow );

	var dofZRow = new UI.Row();
	var dofZ = new UI.Checkbox();
	dofZ.dom.id = 'dz';

	dofZRow.add( new UI.Text( 'Dz' ).setWidth( '90px' ) );
	dofZRow.add( dofZ );

	container.add( dofZRow );

	var dofRxRow = new UI.Row();
	var dofRx = new UI.Checkbox();
	dofRx.dom.id = 'rx';

	dofRxRow.add( new UI.Text( 'Rx' ).setWidth( '90px' ) );
	dofRxRow.add( dofRx );

	container.add( dofRxRow );

	var dofRyRow = new UI.Row();
	var dofRy = new UI.Checkbox();
	dofRy.dom.id = 'ry';

	dofRyRow.add( new UI.Text( 'Ry' ).setWidth( '90px' ) );
	dofRyRow.add( dofRy );

	container.add( dofRyRow );

	var dofRzRow = new UI.Row();
	var dofRz = new UI.Checkbox();
	dofRz.dom.id = 'rz';

	dofRzRow.add( new UI.Text( 'Rz' ).setWidth( '90px' ) );
	dofRzRow.add( dofRz );

	container.add( dofRzRow );
	
	//node

	var nodeRow = new UI.Row();
	var node = new UI.Input( '' ).setLeft( '100px' )
	
	nodeRow.add( new UI.Text('Node').setWidth( '90px' ) );
	nodeRow.add( node );

	container.add( nodeRow );


	var buttonRow = new UI.Row();
	var btn = new UI.Button( 'Define Support' ).onClick( function () {
		nodes = node.getValue().split(",");
		console.log(nodes)
		for(j=0; j<nodes.length; j++){
			name = 'Node '+nodes[j];
			node_ = editor.scene.getObjectByName( name );
			editor.scene.remove( node_ );

			var geometry = new THREE.BoxGeometry( 0.15, 0.15, 0.15 );
			var material = new THREE.MeshBasicMaterial( {color: 0xffff00} );
			var cone = new THREE.Mesh( geometry, material );
			cone.name = node_.name
			cone.applyMatrix( node_.matrix );
			cone.userData = node_.userData;

			var label = node_.children[0].clone();
			cone.add(label);
			cone.parent = editor.scene;
			cone.userData.dof_dx = dofX.getValue() ? 0 : 1;
			cone.userData.dof_dy = dofY.getValue() ? 0 : 1;
			cone.userData.dof_dz = dofZ.getValue() ? 0 : 1;
			cone.userData.dof_rx = dofRx.getValue() ? 0 : 1;
			cone.userData.dof_ry = dofRy.getValue() ? 0 : 1;
			cone.userData.dof_rz = dofRz.getValue() ? 0 : 1;

			editor.execute( new AddObjectCommand( cone ) );
		}
	} );
	

	buttonRow.add( btn );

    container.add( buttonRow );


	return container;

};
