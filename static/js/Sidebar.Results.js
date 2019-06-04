/**
 * @author mrdoob / http://mrdoob.com/
 */


Sidebar.Results = function ( editor ) {

	var config = editor.config;
	var signals = editor.signals;
	var strings = editor.strings;

	var container = new UI.Panel();
	container.setBorderTop( '0' );
	container.setPaddingTop( '20px' );

    var options = new UI.Panel();
	options.setClass( 'options' );
	//container.add( options );
    //supports radio buttons
    title = new UI.Text('Reactions').setWidth( '150px' ) 
    container.add( title )
    container.add( new UI.Break() );
    container.add( new UI.Break() );
    var mqnRow = new UI.Row();
    var mqn = new UI.Button( 'Reactions', 'openerReactions' )
        
    mqnRow.add( mqn );

	container.add( mqnRow );

    
    container.add( new UI.HorizontalRule() );
    title = new UI.Text('Results on Members').setWidth( '150px' ) 
    container.add( title )
    container.add( new UI.Break() );
    container.add( new UI.Break() );

    var mqnRow = new UI.Row();
    var mqn = new UI.Button( 'MQN', 'openerMqn' )
        
    // mqn.id = 'opener'
    mqnRow.add( mqn );

	container.add( mqnRow );
    
    var displRow = new UI.Row();
    var displ = new UI.Button( 'Displacements', 'openerDisplacements' )
    displRow.add( displ );

    container.add( displRow );
    
    container.add( new UI.HorizontalRule() );
    title = new UI.Text('Results on Structure').setWidth( '150px' ) 
    container.add( title )
    container.add( new UI.Break() );
    container.add( new UI.Break() );
    
    var globalDisplRow = new UI.Row();
	var globalDispl = new UI.Checkbox().onChange(  function () {

	} );
	

	globalDisplRow.add( new UI.Text( 'Displacements' ).setWidth( '100px' ) );
	globalDisplRow.add( globalDispl );

	container.add( globalDisplRow );

	var mqnStructRow = new UI.Row();
	var mqnStruct = new UI.Checkbox().onChange(  function () {

	} );
	

	mqnStructRow.add( new UI.Text( 'MQN' ).setWidth( '100px' ) );
	mqnStructRow.add( mqnStruct );

	container.add( mqnStructRow );

	

	return container;

};
