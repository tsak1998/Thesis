/**
 * @author mrdoob / http://mrdoob.com/
 */


Sidebar.Sections = function ( editor ) {
	
	var config = editor.config;
	var signals = editor.signals;
	var strings = editor.strings;
	
	sectCount = 0;
	
	var sections = [];
    var history = editor.history;


	var container = new UI.Panel();
	container.setBorderTop( '0' );
	container.setPaddingTop( '20px' );
	container.setPaddingBottom( '20px' );

	// material and section types

	var options = {
		'con': 'Concrete',
		'stl': 'Steel'
	};

	var materialRow = new UI.Row();
	var material = new UI.Select().setWidth( '150px' );
	material.setOptions( options );

	if ( config.getKey( 'language' ) !== undefined ) {

		material.setValue( '' );

	}


	var sectTypeRow = new UI.Row();
	var sectType = new UI.Select().setWidth( '150px' );

	var options_concrete = {
		'rect' : 'RECTANGLE',
		'T' : 'T'
		
	};

	var options_steel = {
		'hea200' : 'HEA 200',
		'ipe120' : 'IPE 120'
		
	};


	material.onChange( function () {

		var value = this.getValue();
		if ( value == 'con' ){
			sectType.setOptions( options_concrete )
		} else if ( value == 'stl' ){
			sectType.setOptions( options_steel )
		}
	} );

	materialRow.add( new UI.Text( 'Material' ).setWidth( '90px' ) );
	materialRow.add( material );

	container.add( materialRow );

	// section types

		
	//sectType.setOptions( options );

	sectTypeRow.add( new UI.Text( 'Type' ).setWidth( '90px' ) );
	sectTypeRow.add( sectType );

	container.add( sectTypeRow );

	//container.add( new Sidebar.Settings.Shortcuts( editor ) );

	//section dimensions

	var hRow = new UI.Row();
	var h = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {


	} );


	hRow.add( new UI.Text( 'h' ).setWidth( '90px' ) );
	hRow.add( h );

	var bRow = new UI.Row();
	var b = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );
	
	bRow.add( new UI.Text('b').setWidth( '90px' ) );
	bRow.add( b );


	var h1Row = new UI.Row();
	var h1 = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );
	
	h1Row.add( new UI.Text('h1').setWidth( '90px' ) );
	h1Row.add( h1 );


	var b1Row = new UI.Row();
	var b1 = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );
	
	b1Row.add( new UI.Text('b1').setWidth( '90px' ) );
	b1Row.add( b1 );




	sectType.onChange( function () {
		container.remove( outliner );
		container.remove( tableTextRow );
		container.remove( buttonRow );

		var value = this.getValue();

		//add material conditions 
		if ( value == 'rect' ){
			container.add( h1Row );
			container.add( b1Row );
			container.remove( h1Row );
			container.remove( b1Row );
			container.add( hRow );
			container.add( bRow );
		}else if ( value == 'T' ) {
			container.add( hRow );
			container.add( bRow );
			container.add( h1Row );
			container.add( b1Row );

		}
	

		container.add( buttonRow );
		container.add( tableTextRow );
		container.add( outliner );
		
		

	} );

	
	var buttonRow = new UI.Row();
	var btn = new UI.Button( 'Define Section' ).onClick( function () {
		if (material.getValue() == 'con'){
			if (sectType.getValue() == 'rect'){
				sectCount += 1
				section = {
					'section_id' : sectCount,
					'material' : 'C20/25',
					'sect_type' : sectType.getValue(),
					'h' : h.getValue(),
					'b' : b.getValue()
				}
			}else if (sectType.getValue() == 'T'){
				sectCount += 1
				section = {
					'section_id' : sectCount,
					'material' : 'C20/25',
					'sect_type' : sectType.getValue(),
					'h' : h.getValue(),
					'b' : b.getValue(),
					'h1' : h1.getValue(),
					'b1' : b1.getValue()
				}

			}
		}else if (material.getValue() == 'stl'){
			sectCount += 1
			section = {
				'section_id' : sectCount,
				'material' : 'S255',
				'sect_type' : sectType.getValue(),

			}

		}
		editor.sections.sections.push(section)
		
		refreshUI();
	});

	buttonRow.add( btn );
	container.add( buttonRow );


	//
    //container.add( new UI.Break(), new UI.Break() );
	var tableTextRow = new UI.Row();

	tableText = new UI.Text( 'SECTIONS' );
	tableTextRow.add( tableText )

	container.add( tableTextRow );

	//

    container.add( new UI.Break(), new UI.Break() );
    

	var ignoreObjectSelectedSignal = false;

	var outliner = new UI.Outliner( editor );
	outliner.onChange( function () {

		//ignoreObjectSelectedSignal = true;

		//editor.history.goToState( parseInt( outliner.getValue() ) );

		//ignoreObjectSelectedSignal = false;

    } );
    
    container.add( outliner );
    
    //
    xRow = ( new UI.Text( 'x').setWidth( '90px' ) );
	
	outliner.setOptions( xRow );
	outliner.add( xRow );


	
	var refreshUI = function () {

		var options = [];
		var enumerator = 1;

		function buildOption( object ) {

			var option = document.createElement( 'div' );
			option.value = object;
			return option;

		}

		( function addObjects( objects ) {

			for ( var i = 0, l = objects.length; i < l; i ++ ) {
				console.log(objects[i])
				var object = '  ' + String(objects[ i ].section_id) + '  ' + String(objects[ i ].material) + '  ' + String(objects[ i ].sect_type);
				var option = buildOption( object );
				option.innerHTML = '&nbsp;' + object;

				options.push( option );

			}

		} )( editor.sections.sections );



		outliner.setOptions( options );

	};
	
	window.setTimeout( function(){
		$.ajax({
			type: "POST",
			url: "/loadsections",
			dataType: 'text',
			success: function (e) {
				console.log(JSON.parse(e).data)
				editor.sections.sections = JSON.parse(e).data
				refreshUI()						
			},
			error: function(xhr, status, error) {
				console.log(xhr, status, error);	
			}
		});
	}
		, 1500);
	
	

	// events

	signals.editorCleared.add( refreshUI );

	signals.historyChanged.add( refreshUI );
	signals.historyChanged.add( function ( cmd ) {

		outliner.setValue( cmd !== undefined ? cmd.id : null );

	} );


    //
	return container;

};