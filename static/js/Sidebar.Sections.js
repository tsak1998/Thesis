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

	var optionsMaterial = {
		'con': 'Concrete',
		'stl': 'Steel',
		'cstm': 'Custom'
	};

	var materialRow = new UI.Row();
	var material = new UI.Select().setWidth( '150px' );
	material.setOptions( optionsMaterial );
	material.setValue( '' );

	

	var materialCategoryRow = new UI.Row();
	var materialCategory = new UI.Select().setWidth( '150px' );
	materialCategory.setOptions( optionsConcreteCategory );
	materialCategory.setValue( '' );

	

	/*
	var options = {
		'con': 'Concrete',
		'stl': 'Steel'
	};
	var materialRow = new UI.Row();
	var material = new UI.Select().setWidth( '150px' );
	material.setOptions( options );
	material.setValue( '' );
	*/

	var sectTypeRow = new UI.Row();
	var sectType = new UI.Select().setWidth( '150px' );

	var options_concrete = {
		'rect' : 'RECTANGLE',
		'T' : 'T',
		'L' : 'L'
		
	};

	var options_steel = {
		'hea200' : 'HEA 200',
		'ipe120' : 'IPE 120'
		
	};

	var optionsConcreteCategory = {
		'c20/25': 'C20/25',
		'c25/30': 'C25/30'
	};

	var optionsSteelCategory = {
		's225': 'S225'
	};

    // custom section properties
    var customMat = new UI.Panel();
    var customSect = new UI.Panel();
    var ERow = new UI.Row();
	var E = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {


	} );


	ERow.add( new UI.Text( 'E' ).setWidth( '90px' ) );
	ERow.add( E );

	var GRow = new UI.Row();
	var G = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {


	} );


	GRow.add( new UI.Text( 'G' ).setWidth( '90px' ) );
	GRow.add( G );

	var ARow = new UI.Row();
	var A = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {


	} );


	ARow.add( new UI.Text( 'A' ).setWidth( '90px' ) );
	ARow.add( A );

	var IxRow = new UI.Row();
	var Ix = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {


	} );


	IxRow.add( new UI.Text( 'Ix' ).setWidth( '90px' ) );
	IxRow.add( Ix );

	var IyRow = new UI.Row();
	var Iy = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {


	} );


	IyRow.add( new UI.Text( 'Iy' ).setWidth( '90px' ) );
	IyRow.add( Iy );

	var IzRow = new UI.Row();
	var Iz = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {


	} );


	IzRow.add( new UI.Text( 'Iz' ).setWidth( '90px' ) );
	IzRow.add( Iz );

    customMst.add(ERow);
    customMst.add(GRow);
    customSect.add(ARow);
    customSect.add(IxRow);
    customSect.add(IyRow);
    customSect.add(IzRow);
    customMst.dom.hidden=true;
    customSect.dom.hidden=true;



	material.onChange( function () {

		var value = this.getValue();
		if ( value == 'con' ){
		    customSect.dom.hidden=true;
			sectType.setOptions( options_concrete );
			materialCategory.setOptions( optionsConcreteCategory );
		} else if ( value == 'stl' ){
		    customSect.dom.hidden=true;
			sectType.setOptions( options_steel );
			materialCategory.setOptions( optionsSteelCategory );
		}else {
		    customSect.dom.hidden=false;
		};
	} );

	materialRow.add( new UI.Text( 'Material' ).setWidth( '90px' ) );
	materialRow.add( material );

	container.add( materialRow );

	materialCategoryRow.add( new UI.Text( 'Material Category' ).setWidth( '90px' ) );
	materialCategoryRow.add( materialCategory );

	container.add( materialCategoryRow );

	// section types

		
	//sectType.setOptions( options );

	sectTypeRow.add( new UI.Text( 'Type' ).setWidth( '90px' ) );
	sectTypeRow.add( sectType );

	container.add( sectTypeRow );

    container.add(customSect)
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

    rectContainer = new UI.Panel();
    tContainer = new UI.Panel();

    rectContainer.add( hRow );
    rectContainer.add( bRow );
    rectContainer.dom.hidden = true;
    tContainer.add( h1Row );
    tContainer.add( b1Row );
    tContainer.dom.hidden = true;

    container.add(rectContainer);
    container.add(tContainer);


	sectType.onChange( function () {
		container.remove( outliner );
		container.remove( tableTextRow );
		container.remove( buttonRow );

		var value = this.getValue();

		//add material conditions 
		if ( value == 'rect' ){
		    tContainer.dom.hidden = true;
            rectContainer.dom.hidden = false;
		}else if ( value == 'T' ) {
		    tContainer.dom.hidden = false;
            rectContainer.dom.hidden = false;


		}
	

		container.add( buttonRow );
		container.add( tableTextRow );
		container.add( outliner );
		
		

	} );


	var buttonRow = new UI.Row();
	var btn = new UI.Button( 'Define Section' ).onClick( function () {
		if (material.getValue() == 'con'){
			sectCount += 1
			if (sectType.getValue() == 'rect'){
				
				section = {
					'section_id' : sectCount,
					'material' : material.getValue(),
					'material_category' : materialCategory.getValue(),
					'sect_type' : sectType.getValue(),
					'h' : h.getValue(),
					'b' : b.getValue()
				}
			}else if (sectType.getValue() == 'T'){
				
				section = {
					'section_id' : sectCount,
					'material' : material.getValue(),
					'material_category' : materialCategory.getValue(),
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
				'material' : material.getValue(),
				'material_category' : materialCategory.getValue(),
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

    container.add( new UI.Break() );
    

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
				editor.sections.sections = JSON.parse(e).data
				sectCount = editor.sections.sections.length
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