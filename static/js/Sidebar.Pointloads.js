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

	var options = {
		'onNode': 'ON NODE',
		'onMember': 'ON MEMBER'
	};

	
	var loadTypeRow = new UI.Row();
	var loadType = new UI.Select().setWidth( '150px' );
    loadType.setOptions( options );

    var objectRow = new UI.Row();
	var object = new UI.Input( '' ).setLeft( '100px' ).setWidth( '90px' ).onChange( function () {

	} );
	

	objectRow.add( new UI.Text( 'Node/Member' ).setWidth( '50px' ) );
    objectRow.add( object );

    //dp/l ratio for the point load on member
    var lengthRatioRow = new UI.Row();
	var lengthRatio = new UI.Select().setWidth( '150px' );
    lengthRatio.setOptions( options );

    var lengthRatioRow = new UI.Row();
	var lengthRatio = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' ).onChange( function () {

	} );
	

	lengthRatioRow.add( new UI.Text( 'Position of Load(x/L)' ).setWidth( '90px' ) );
    lengthRatioRow.add( lengthRatio );


    //Load values (Px,Py,Pz,...)
	var PxRow = new UI.Row();
	var Px = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' ).onChange( function () {

	} );
	

	PxRow.add( new UI.Text( 'Px' ).setWidth( '90px' ) );
	PxRow.add( Px );

	

	var PyRow = new UI.Row();
	var Py = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' ).onChange( function () {

		

	} );
	

	PyRow.add( new UI.Text( 'Py' ).setWidth( '90px' ) );
	PyRow.add( Py );

	


	var PzRow = new UI.Row();
	var Pz = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' ).onChange( function () {

		 

	} );
	

	PzRow.add( new UI.Text('Pz').setWidth( '90px' ) );
	PzRow.add( Pz );


    var MxRow = new UI.Row();
	var Mx = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' ).onChange( function () {

	} );
	

	MxRow.add( new UI.Text( 'Mx' ).setWidth( '90px' ) );
	MxRow.add( Mx );



	var MyRow = new UI.Row();
	var My = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' ).onChange( function () {

		

	} );
	

	MyRow.add( new UI.Text( 'My' ).setWidth( '90px' ) );
	MyRow.add( My );




	var MzRow = new UI.Row();
	var Mz = new UI.Input( '' ).setLeft( '100px' ).setWidth( '40px' ).onChange( function () {

		
	} );
	

	MzRow.add( new UI.Text('Mz').setWidth( '90px' ) );
	MzRow.add( Mz );
    
   
	loadType.onChange( function () {
        container.add( objectRow );

        var value = this.getValue();
        
        if (value == 'onNode'){
            container.add( lengthRatioRow );
            container.remove( lengthRatioRow );

            container.add( PxRow );
            container.add( PyRow );
            container.add( PzRow );
            container.add( MxRow );
            container.add( MyRow );
            container.add( MzRow );
            
        }else if ( value == 'onMember'){
            container.add( lengthRatioRow );
            container.add( PxRow );
            container.add( PyRow );
            container.add( PzRow );
            container.add( MxRow );
            container.add( MyRow );
            container.add( MzRow );

        }

	
	} );

	loadTypeRow.add( new UI.Text( 'Load Type' ).setWidth( '90px' ) );
	loadTypeRow.add( loadType );

    container.add( loadTypeRow );


	var buttonRow = new UI.Row();
	var btn = new UI.Button( 'Add Load' ).onClick( function () {
        
		var dir = new THREE.Vector3( 1, 2, 0 );

        //normalize the direction vector (convert to vector of length 1)
        dir.normalize();

        var origin = new THREE.Vector3( 0, 0, 0 );
        var length = 1;
        var hex = 0xffff00;

        var arrowHelper = new THREE.ArrowHelper( dir, origin, length, hex );

        //hack around, remove node, append arrow as child and
        //add again with the editor.execute()
        // refine AddObjectCommand, undo, redo, delete for object children
        name = 'Node_'+String( object.getValue() )
        node = editor.scene.getObjectByName( name )

        editor.execute( new RemoveObjectCommand( node ) );
        node.extra.push( arrowHelper )

        pointLoad = {'nn': node.userData.nn,
                    'p_x': Px.getValue() ,
                    'p_y': Py.getValue() ,
                    'p_z': Pz.getValue() ,
                    'm_x': Mx.getValue() ,
                    'm_y': My.getValue() ,
                    'm_z': Mz.getValue()

                    }
        point_loads.push( pointLoad )
        editor.userData.point_loads = point_loads

        console.log( editor.userData )
        

                              
                         
        
        
        editor.execute( new AddObjectCommand( node ) );
        //for ease arrow will be removed from input box
        render();
        

     } );
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


    function render() {

        editor.sceneHelpers.updateMatrixWorld();
        editor.scene.updateMatrixWorld();
    
        editor.renderer.render( editor.scene, editor.camera );
    
        if ( editor.renderer instanceof THREE.RaytracingRenderer === false ) {
    
            editor.renderer.render( editor.sceneHelpers, editor.camera );
    
        }
    
    }
    
    



    

	return container;

};
