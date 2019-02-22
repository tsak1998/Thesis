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

	var projectTab = new UI.Text( strings.getKey( 'sidebar/project' ) ).setTextTransform( 'uppercase' );
	projectTab.onClick( function () { select( 'PROJECT' ) } );
	
	var projectTab2 = new UI.Text( strings.getKey( 'sidebar/createElement' ) ).setTextTransform( 'uppercase' );
	projectTab2.onClick( function () { select( 'ELEMENTS' ) } );


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
	tabs.add( sceneTab, projectTab, sectionsTab, projectTab2, supportsTab, pointLoadsTab, settingsTab );
	container.add( tabs );

	//

	var scene = new UI.Span().add(
		new Sidebar.Scene( editor ),
		new Sidebar.Properties( editor ),
	
	);
	container.add( scene );


	var project = new UI.Span().add(
		new Sidebar.Project( editor )
	);
	container.add( project );

	var sections = new UI.Span().add(
		new Sidebar.Sections( editor )
	);
	container.add( sections );
	
	var project2 = new UI.Span().add(
		new Sidebar.Yellow( editor )
	);
	container.add( project2 );
	
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
		projectTab.setClass( '' );
		projectTab2.setClass( '' );
		supportsTab.setClass( '' );
		sectionsTab.setClass( '' );
		pointLoadsTab.setClass( '' );
		settingsTab.setClass( '' );

		scene.setDisplay( 'none' );
		project.setDisplay( 'none' );
		project2.setDisplay( 'none' );
		supports.setDisplay( 'none' );
		sections.setDisplay( 'none' );
		pointLoads.setDisplay( 'none' );
		settings.setDisplay( 'none' );

		switch ( section ) {
			case 'SCENE':
				sceneTab.setClass( 'selected' );
				scene.setDisplay( '' );
				break;
			case 'PROJECT':
				projectTab.setClass( 'selected' );
				project.setDisplay( '' );
				break;
			case 'SECTIONS':
				sectionsTab.setClass( 'selected' );
				sections.setDisplay( '' );
				break;
			case 'ELEMENTS':
				projectTab2.setClass( 'selected' );
				project2.setDisplay( '' );
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
