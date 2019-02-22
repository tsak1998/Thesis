/**
 * @author mrdoob / http://mrdoob.com/
 */

Menubar.View = function ( editor ) {

	var container = new UI.Panel();
	container.setClass( 'menu' );
	var strings = editor.strings;

	var title = new UI.Panel();
	title.setClass( 'title' );
	title.setTextContent( strings.getKey( 'menubar/view' ) );
	container.add( title );

	var options = new UI.Panel();
	options.setClass( 'options' );
	container.add( options );

	/*
	// VR mode

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( 'VR mode' );
	option.onClick( function () {

		if ( WEBVR.isAvailable() === true ) {

			editor.signals.enterVR.dispatch();

		} else {

			alert( 'WebVR not available' );

		}

	} );
	options.add( option );
	*/


	// Toggle node IDs

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/view/toggle_node_labels' ) );
	option.onClick( function () {
		var c = editor.sceneHelpers.children;
		for (var i = 0; i < c.length; i++) {
			if (c[i].name == 'nelabels') {
				var d = c[i].children;
				for (var j = 0; j < d.length; j++) {
					if (d[j].name == 'nlabels') {
						if (d[j].visible == true) {
							d[j].visible = false;
							editor.signals.sceneGraphChanged.dispatch();
							break;
						} else {
							d[j].visible = true;
							editor.signals.sceneGraphChanged.dispatch();
							break;
						}				
					}
				}
			}
		} 
	} );
	options.add( option );



	// Toggle beam IDs

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/view/toggle_beam_labels' ) );
	option.onClick( function () {
		var c = editor.sceneHelpers.children;
		for (var i = 0; i < c.length; i++) {
			if (c[i].name == 'nelabels') {
				var d = c[i].children;
				for (var j = 0; j < d.length; j++) {
					if (d[j].name == 'blabels') {
						if (d[j].visible == true) {
							d[j].visible = false;
							editor.signals.sceneGraphChanged.dispatch();
							break;
						} else {
							d[j].visible = true;
							editor.signals.sceneGraphChanged.dispatch();
							break;
						}				
					}
				}
			}
		} 
	} );
	options.add( option );

	// Toggle column IDs

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/view/toggle_column_labels' ) );
	option.onClick( function () {
		var c = editor.sceneHelpers.children;
		for (var i = 0; i < c.length; i++) {
			if (c[i].name == 'nelabels') {
				var d = c[i].children;
				for (var j = 0; j < d.length; j++) {
					if (d[j].name == 'clabels') {
						if (d[j].visible == true) {
							d[j].visible = false;
							editor.signals.sceneGraphChanged.dispatch();
							break;
						} else {
							d[j].visible = true;
							editor.signals.sceneGraphChanged.dispatch();
							break;
						}				
					}
				}
			}
		} 
	} );
	options.add( option );
	
	options.add( new UI.HorizontalRule() );


	// Toggle column IDs

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/view/toggle_grid' ) );
	option.onClick( function () {
		var c = editor.sceneHelpers.children;
		for (var i = 0; i < c.length; i++) {
			
			if (c[i].constructor.name == 'GridHelper') {
				if (c[i].visible == true) {
					c[i].visible = false;
			} else {
					c[i].visible = true;
			}				}
		} 
		editor.signals.sceneGraphChanged.dispatch();
	} );
	options.add( option );

	return container;

};
