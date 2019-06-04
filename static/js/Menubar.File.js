/**
 * @author mrdoob / http://mrdoob.com/
 */

Menubar.File = function ( editor ) {

	var NUMBER_PRECISION = 6;

	function parseNumber( key, value ) {

		return typeof value === 'number' ? parseFloat( value.toFixed( NUMBER_PRECISION ) ) : value;

	}

	//

	var config = editor.config;
	var strings = editor.strings;

	var container = new UI.Panel();
	container.setClass( 'menu' );

	var title = new UI.Panel();
	title.setClass( 'title' );
	title.setTextContent( strings.getKey( 'menubar/file' ) );
	container.add( title );

	var options = new UI.Panel();
	options.setClass( 'options' );
	container.add( options );

	// New

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/new' ) );
	option.onClick( function () {

		if ( confirm( 'Any unsaved data will be lost. Are you sure?' ) ) {

			editor.clear();

		}

	} );
	options.add( option );

	//

	options.add( new UI.HorizontalRule() );

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( 'Load' );
	
	option.onClick( function () {
		
		if ( confirm( 'Any unsaved data will be lost. Are you sure?' ) ) {

			editor.clear();
				
			$.ajax({
				type: "POST",
				url: "/load",
				data: {},
				dataType: 'text',
				success: function (e) {
					var data = e.split("|");
					var nodes = JSON.parse(data[0]);
					var elements = JSON.parse(data[1]);
					var pointLoads = JSON.parse(data[2]);
					drawNodes( editor, nodes.data );
					drawElements( editor, elements.data );
					drawPointLoads( editor, pointLoads.data );		
				},
				error: function(xhr, status, error) {
					console.log(xhr, status, error);	
				}
			});	
			
		}		
	
	});
	options.add( option );

	options.add( new UI.HorizontalRule() );

	//
	//Save

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/save' ) );
	
	option.onClick( function () {
		data1 = []
		nodes = [];
		elements = [];
		loads = [];
		for (i=0; i<editor.scene.children.length; i++){
			obj = editor.scene.children[i]
			if (obj.userData.type == 'element') {
				elements.push( obj.userData );
			} else if (obj.userData.type == 'node') {
				nodes.push( obj.userData );
			} else if (obj.userData.type == 'p_load' || obj.userData.type == 'p_moment') {
				loads.push( obj.userData );
			}
		}
		data1.push(elements);
		data1.push(nodes);
		data1.push(loads);
		var sections = editor.sections.sections;
		data1.push(sections )


		data1 = JSON.stringify( data1 );
		console.log(data1)
		$.ajax({
			type: "POST",
			url: '/save',
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: data1,

		});
	});
	options.add( option );
	//

	options.add( new UI.HorizontalRule() );

	// Import DXF

	var form = document.createElement( 'form' );
	form.style.display = 'none';
	document.body.appendChild( form );

	var fileInput = document.createElement( 'input' );
	fileInput.multiple = false;
	fileInput.type = 'file';
	fileInput.accept = 'application/dxf';
	fileInput.addEventListener( 'change', function ( event ) {

		if ( confirm( 'Any unsaved data will be lost. Are you sure?' ) ) {

			editor.clear();
		
			$.ajax({
				type: 'POST',
				timeout: 20000,
				url: '/readDXF',
				data: fileInput.files[0],
				processData: false,
				contentType: 'application/dxf',
				dataType: 'text',
				success: function(e) {
					var nodelm = e.split("|");
					//console.log(nodelm[0]);
					//console.log(nodelm[1]);
					var nodes = JSON.parse(nodelm[0]);
					var elements = JSON.parse(nodelm[1]);
					drawNodes( editor, nodes.data );
					drawElements( editor, elements.data );
					
				},
				error: function(xhr, status, error) {
					console.log(xhr, status, error);
				}
			});
		}
		form.reset();
	});
	form.appendChild( fileInput );

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/importdxf' ) );
	option.onClick( function () {

		fileInput.click();

	});
	options.add( option );

	//

	options.add( new UI.HorizontalRule() );




	// periodically save to the database 
	var intervalID = setInterval(function(){
		data1 = []
		var model = editor.scene.children;

		//model = JSON.stringify( model );

		var sections = editor.userData.sections;

		var pointloads = editor.userData.point_loads;

		//sections = JSON.stringify( sections );

		data1.push( model )
		data1.push( sections )
		data1.push( pointloads )

		data1 = JSON.stringify( data1 );

		$.ajax({
			type: "POST",
			url: '/autosave',
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: data1,

		});

	}, 120000);








	// Export Geometry
/*
	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/export/geometry' ) );
	option.onClick( function () {

		var object = editor.selected;

		if ( object === null ) {

			alert( 'No object selected.' );
			return;

		}

		var geometry = object.geometry;

		if ( geometry === undefined ) {

			alert( 'The selected object doesn\'t have geometry.' );
			return;

		}

		var output = geometry.toJSON();

		try {

			output = JSON.stringify( output, parseNumber, '\t' );
			output = output.replace( /[\n\t]+([\d\.e\-\[\]]+)/g, '$1' );

		} catch ( e ) {

			output = JSON.stringify( output );

		}

		saveString( output, 'geometry.json' );

	} );
	options.add( option );

	// Export Object

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/export/object' ) );
	option.onClick( function () {

		var object = editor.selected;

		if ( object === null ) {

			alert( 'No object selected' );
			return;

		}

		var output = object.toJSON();

		try {

			output = JSON.stringify( output, parseNumber, '\t' );
			output = output.replace( /[\n\t]+([\d\.e\-\[\]]+)/g, '$1' );

		} catch ( e ) {

			output = JSON.stringify( output );

		}

		saveString( output, 'model.json' );

	} );
	options.add( option );
*/
	// Export Scene

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/export/scene' ) );
	option.onClick( function () {

		var output = editor.scene.toJSON();

		try {

			output = JSON.stringify( output, parseNumber, '\t' );
			output = output.replace( /[\n\t]+([\d\.e\-\[\]]+)/g, '$1' );

		} catch ( e ) {

			output = JSON.stringify( output );

		}

		saveString( output, 'scene.json' );

	} );
	options.add( option );

	//

	options.add( new UI.HorizontalRule() );
/*
	// Export DAE

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/export/dae' ) );
	option.onClick( function () {

		var exporter = new THREE.ColladaExporter();

		exporter.parse( editor.scene, function ( result ) {

			saveString( result.data, 'scene.dae' );

		} );

	} );
	options.add( option );

	// Export GLB

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/export/glb' ) );
	option.onClick( function () {

		var exporter = new THREE.GLTFExporter();

		exporter.parse( editor.scene, function ( result ) {

			saveArrayBuffer( result, 'scene.glb' );

			// forceIndices: true, forcePowerOfTwoTextures: true
			// to allow compatibility with facebook
		}, { binary: true, forceIndices: true, forcePowerOfTwoTextures: true } );

	} );
	options.add( option );

	// Export GLTF

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/export/gltf' ) );
	option.onClick( function () {

		var exporter = new THREE.GLTFExporter();

		exporter.parse( editor.scene, function ( result ) {

			saveString( JSON.stringify( result, null, 2 ), 'scene.gltf' );

		} );


	} );
	options.add( option );

	// Export OBJ

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/export/obj' ) );
	option.onClick( function () {

		var object = editor.selected;

		if ( object === null ) {

			alert( 'No object selected.' );
			return;

		}

		var exporter = new THREE.OBJExporter();

		saveString( exporter.parse( object ), 'model.obj' );

	} );
	options.add( option );

	// Export STL (ASCII)

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/export/stl' ) );
	option.onClick( function () {

		var exporter = new THREE.STLExporter();

		saveString( exporter.parse( editor.scene ), 'model.stl' );

	} );
	options.add( option );

	// Export STL (Binary)

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/export/stl_binary' ) );
	option.onClick( function () {

		var exporter = new THREE.STLExporter();

		saveArrayBuffer( exporter.parse( editor.scene, { binary: true } ), 'model-binary.stl' );

	} );
	options.add( option );

	//
*/
	// options.add( new UI.HorizontalRule() );

	// Publish

	var option = new UI.Row();
	option.setClass( 'option' );
	option.setTextContent( strings.getKey( 'menubar/file/publish' ) );
	option.onClick( function () {

		var zip = new JSZip();

		//

		var output = editor.toJSON();
		output.metadata.type = 'App';
		delete output.history;

		var vr = output.project.vr;

		output = JSON.stringify( output, parseNumber, '\t' );
		output = output.replace( /[\n\t]+([\d\.e\-\[\]]+)/g, '$1' );

		zip.file( 'app.json', output );

		//

		var title = config.getKey( 'project/title' );

		var manager = new THREE.LoadingManager( function () {

			save( zip.generate( { type: 'blob' } ), ( title !== '' ? title : 'untitled' ) + '.zip' );

		} );

		var loader = new THREE.FileLoader( manager );
		loader.load( 'js/libs/app/index.html', function ( content ) {

			content = content.replace( '<!-- title -->', title );

			var includes = [];

			if ( vr ) {

				includes.push( '<script src="js/WebVR.js"></script>' );

			}

			content = content.replace( '<!-- includes -->', includes.join( '\n\t\t' ) );

			var editButton = '';

			if ( config.getKey( 'project/editable' ) ) {

				editButton = [
					'',
					'			var button = document.createElement( \'a\' );',
					'			button.href = \'https://threejs.org/editor/#file=\' + location.href.split( \'/\' ).slice( 0, - 1 ).join( \'/\' ) + \'/app.json\';',
					'			button.style.cssText = \'position: absolute; bottom: 20px; right: 20px; padding: 12px 14px; color: #fff; border: 1px solid #fff; border-radius: 4px; text-decoration: none;\';',
					'			button.target = \'_blank\';',
					'			button.textContent = \'EDIT\';',
					'			document.body.appendChild( button );',
					''
				].join( '\n' );
			}

			content = content.replace( '\n\t\t\t/* edit button */\n', editButton );

			zip.file( 'index.html', content );

		} );
		loader.load( 'js/libs/app.js', function ( content ) {

			zip.file( 'js/app.js', content );

		} );
		loader.load( '../build/three.min.js', function ( content ) {

			zip.file( 'js/three.min.js', content );

		} );

		if ( vr ) {

			loader.load( '../examples/js/vr/WebVR.js', function ( content ) {

				zip.file( 'js/WebVR.js', content );

			} );

		}

	} );
	options.add( option );

	//

	var link = document.createElement( 'a' );
	link.style.display = 'none';
	document.body.appendChild( link ); // Firefox workaround, see #6594

	function save( blob, filename ) {

		link.href = URL.createObjectURL( blob );
		link.download = filename || 'data.json';
		link.click();

		// URL.revokeObjectURL( url ); breaks Firefox...

	}

	function saveArrayBuffer( buffer, filename ) {

		save( new Blob( [ buffer ], { type: 'application/octet-stream' } ), filename );

	}

	function saveString( text, filename ) {

		save( new Blob( [ text ], { type: 'text/plain' } ), filename );

	}

	return container;

};
