/**
 * @author mrdoob / http://mrdoob.com/
 */

var Sidebar = function ( editor ) {

	var strings = editor.strings;

	var container = new UI.Panel();
	container.setId( 'sidebar' );
	//

	var sceneTab = new UI.Text( strings.getKey( 'sidebar/scene' ) ).setTextTransform( 'uppercase' );
	sceneTab.onClick( function () { select( 'SCENE' ) } );

	var nodesTab = new UI.Text( strings.getKey( 'sidebar/project' ) ).setTextTransform( 'uppercase' );
	nodesTab.onClick( function () { select( 'NODES' ) } );
	
	var elementsTab = new UI.Text( strings.getKey( 'sidebar/createElement' ) ).setTextTransform( 'uppercase' );
	elementsTab.onClick( function () { select( 'ELEMENTS' ) } );


	var supportsTab = new UI.Text( 'supports' ).setTextTransform( 'uppercase' );
	supportsTab.onClick( function () { select( 'SUPPORTS' ) } );

	var sectionsTab = new UI.Text( 'sections' ).setTextTransform( 'uppercase' );
	sectionsTab.onClick( function () { select( 'SECTIONS' ) } );

	var pointLoadsTab = new UI.Text( 'point loads' ).setTextTransform( 'uppercase' );
	pointLoadsTab.onClick( function () { select( 'POINT LOADS' ) } );

	var settingsTab = new UI.Text( strings.getKey( 'sidebar/settings' ) ).setTextTransform( 'uppercase' );
	settingsTab.onClick( function () { select( 'SETTINGS' ) } );

	var tabs = new UI.Div();
	tabs.setId( 'tabs' );
	tabs.add( sceneTab, nodesTab, sectionsTab, elementsTab, supportsTab, pointLoadsTab, settingsTab );
	container.add( tabs );

	//

	var scene = new UI.Span().add(
		new Sidebar.Scene( editor ),
		new Sidebar.Properties( editor ),
	
	);
	container.add( scene );


	var nodes = new UI.Span().add(
		new Sidebar.Nodes( editor )
	);
	container.add( nodes );

	var sections = new UI.Span().add(
		new Sidebar.Sections( editor )
	);
	container.add( sections );
	
	var elements = new UI.Span().add(
		new Sidebar.Elements( editor )
	);
	container.add( elements );
	
	var supports = new UI.Span().add(
		new Sidebar.Supports( editor )
	);
	container.add( supports );

	


	var pointLoads = new UI.Span().add(
		new Sidebar.PointLoads( editor )
	);
	container.add( pointLoads );
	
	

	var settings = new UI.Span().add(
		new Sidebar.Settings( editor ),
		new Sidebar.History( editor )
	);
	container.add( settings );

	//

	function select( section ) {

		sceneTab.setClass( '' );
		nodes.setClass( '' );
		elements.setClass( '' );
		supportsTab.setClass( '' );
		sectionsTab.setClass( '' );
		pointLoadsTab.setClass( '' );
		settingsTab.setClass( '' );

		scene.setDisplay( 'none' );
		nodes.setDisplay( 'none' );
		elements.setDisplay( 'none' );
		supports.setDisplay( 'none' );
		sections.setDisplay( 'none' );
		pointLoads.setDisplay( 'none' );
		settings.setDisplay( 'none' );

		switch ( section ) {
			case 'SCENE':
				sceneTab.setClass( 'selected' );
				scene.setDisplay( '' );
				break;
			case 'NODES':
				nodes.setClass( 'selected' );
				nodes.setDisplay( '' );
				break;
			case 'SECTIONS':
				sectionsTab.setClass( 'selected' );
				sections.setDisplay( '' );
				break;
			case 'ELEMENTS':
				elements.setClass( 'selected' );
				elements.setDisplay( '' );
				break;
			case 'SUPPORTS':
				supportsTab.setClass( 'selected' );
				supports.setDisplay( '' );
				break;
			
			case 'POINT LOADS':
				pointLoadsTab.setClass( 'selected' );
				pointLoads.setDisplay( '' );
				break;
			case 'SETTINGS':
				settingsTab.setClass( 'selected' );
				settings.setDisplay( '' );
				break;
		}

	}

	select( 'SCENE' );

	return container;

};
