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

	//supports radio buttons

    var fixedRow = new UI.Row();
	var fixed = new UI.Checkbox().onChange( update );
	fixed.dom.id = 'fixed';

	fixedRow.add( new UI.Text( 'Fixed' ).setWidth( '90px' ) );
	fixedRow.add( fixed );

	container.add( fixedRow );

	var pinnedRow = new UI.Row();
	var pinned = new UI.Checkbox().onChange( update );
	pinned.dom.id = 'pinned';

	pinnedRow.add( new UI.Text( 'Pinned' ).setWidth( '90px' ) );
	pinnedRow.add( pinned );

	container.add( pinnedRow );

	var rollerRow = new UI.Row();
	var roller = new UI.Checkbox().onChange( update );
	roller.dom.id = 'roller';

	rollerRow.add( new UI.Text( 'Roller' ).setWidth( '90px' ) );
	rollerRow.add( roller );

	container.add( rollerRow );
	
	//node

	var nodeRow = new UI.Row();
	var node = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );
	
	nodeRow.add( new UI.Text('Node').setWidth( '90px' ) );
	nodeRow.add( node );

	container.add( nodeRow );

	var buttonRow = new UI.Row();
	var btn = new UI.Button( 'Pick Node' ).onClick( function () {
		nodes=[]

		{

		//document.addEventListener( "mousedown", onMouseDown, false );
		
		document.addEventListener( "click", onMouseUp, false );
		

	}

	function onMouseUp(event){
		if ( editor.selected == null ) {


		}else if(nodes.length<1) {
			if (nodes[0]==editor.selected){
				
			}else{
				nodes.push(editor.selected)
				node.dom.value = editor.selected.userData.id
				}
				
			}
		else {
			document.removeEventListener( "click", onMouseUp, false );
		
		
		}

	}
		
	} );
	

	buttonRow.add( btn );

	container.add( buttonRow );
	

	var buttonRow = new UI.Row();
	var btn = new UI.Button( 'Define Support' ).onClick( function () {
		if ( supportType == 'fixed' ){
			nodes[0].userData.dof_dx = 0
			nodes[0].userData.dof_dy = 0
			nodes[0].userData.dof_dz = 0
			nodes[0].userData.dof_rx = 0
			nodes[0].userData.dof_ry = 0
			nodes[0].userData.dof_rz = 0
		}else if ( supportType == 'pinned' ){
			nodes[0].userData.dof_dx = 0
			nodes[0].userData.dof_dy = 0
			nodes[0].userData.dof_dz = 0
			nodes[0].userData.dof_rx = 1
			nodes[0].userData.dof_ry = 1
			nodes[0].userData.dof_rz = 1

		}else if ( supportType == 'roller' ){
			nodes[0].userData.dof_dx = 0
			nodes[0].userData.dof_dy = 1
			nodes[0].userData.dof_dz = 0
			nodes[0].userData.dof_rx = 1
			nodes[0].userData.dof_ry = 1
			nodes[0].userData.dof_rz = 1

		}

		nodes[0].userData.supportType = supportType
		
	} );
	

	buttonRow.add( btn );

    container.add( buttonRow );

	
    function update() {

		
		if (this.dom.id == 'fixed'){
			supportType = 'fixed'
			pinned.dom.checked = false
			roller.dom.checked = false
		}else if (this.dom.id == 'pinned'){
			supportType = 'pinned'
			fixed.dom.checked = false
			roller.dom.checked = false
		}else if (this.dom.id == 'roller'){
			supportType = 'roller'
			fixed.dom.checked = false
			pinned.dom.checked = false
		}
			
		

	}


	return container;

};
