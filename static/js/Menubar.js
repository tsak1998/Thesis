/**
 * @author mrdoob / http://mrdoob.com/
 */

var Menubar = function ( editor ) {

	var container = new UI.Panel();
	container.setId( 'menubar' );

	container.add( new Menubar.File( editor ) );

	container.add( new Menubar.View( editor ) );

	container.add( new Menubar.Run( editor ) );
	
	container.add( new Menubar.Status( editor ) );

	return container;

};
