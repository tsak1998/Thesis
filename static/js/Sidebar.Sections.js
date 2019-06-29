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
    // material
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
    materialCategoryRow.dom.hidden= true;


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



    customMat.add(ERow);
    customMat.add(GRow);
    customMat.dom.hidden = true;

    var matButtonRow = new UI.Row();
    matBtn = new UI.Button('Define Material').onClick( function () {
        var value = material.getValue();
		if ( value == 'con' ){

		} else if ( value == 'stl' ){

		}else if ( value == 'cstm' ) {
		    id = editor.sectMaterials.sectMaterials.length+1
		    E_ = E.getValue();
		    G_ = G.getValue();
		    editor.sectMaterials.sectMaterials.push({'id':id,'E':E_,'G':G_})
		    data = editor.sectMaterials.sectMaterials
		    headers = ['id', 'E', 'G']
		    matDiv = document.getElementById( 'material-tab' )
		    child = document.getElementById( 'mat_table' )
		    matDiv.removeChild(child);
            matDiv.appendChild(buildTable(data, headers, 'mat_table'));
		};
		editor.storage.set( editor.toJSON() );
        editor.signals.savingFinished.dispatch();
    });
    matButtonRow.add(matBtn)

    editor.signals.savingFinished.add(function(){
        matDiv = document.getElementById( 'material-tab' )
        matDiv.appendChild (materialRow.dom )
        matDiv.appendChild( materialCategoryRow.dom )
        matDiv.appendChild( customMat.dom )
        matDiv.appendChild( matButtonRow.dom )
        data  = editor.sectMaterials.sectMaterials
        headers = ['id', 'E', 'G']
        matDiv.appendChild(buildTable(data, headers, 'mat_table'));
    });

    material.onChange( function () {

		var value = this.getValue();
		if ( value == 'con' ){
		    customMat.dom.hidden = true;
			materialCategoryRow.dom.hidden = false;
			sectType.setOptions( options_concrete );
			materialCategory.setOptions( optionsConcreteCategory );
		} else if ( value == 'stl' ){
		    customMat.dom.hidden = true;
		    materialCategoryRow.dom.hidden = false;
			sectType.setOptions( options_steel );
			materialCategory.setOptions( optionsSteelCategory );
		}else {
		    materialCategoryRow.dom.hidden = true;
		    customMat.dom.hidden = false;
		};
	} );


    ////

    var options_sect = {
		'RECT' : 'RECTANGLE',
		'T' : 'T',
		'Γ ' : 'Γ',
		'HEA': 'HEA',
		'IPE': 'IPE',
		'Custom': 'CUSTOM'
	};

    var sectTypeRow = new UI.Row();
	var sectType = new UI.Select().setWidth( '150px' );
	sectTypeRow.add( new UI.Text( 'Type' ).setWidth( '90px' ) );
    sectType.setOptions( options_sect );

	var sectCategoryRow = new UI.Row();
	var sectCategory = new UI.Select().setWidth( '150px' );
	sectCategoryRow.add( new UI.Text( 'Category' ).setWidth( '90px' ) );
	sectCategoryRow.dom.hidden = true;

    var options_HEA = {
		'HEA200' : 'HEA 200'

	};

	var options_IPE = {
		'IPE120' : 'IPE 120'

	};

    sectType.onChange( function () {

		var value = this.getValue();
		if ( value == 'RECT' ){
		    sectCategoryRow.dom.hidden = true;
		    customSect.dom.hidden = true;
		    tContainer.dom.hidden = true;
            rectContainer.dom.hidden = false;
		} else if ( value == 'T' ){
		    sectCategoryRow.dom.hidden = true;
		    customSect.dom.hidden = true;
		    rectContainer.dom.hidden = true;
            tContainer.dom.hidden = false;
		}else if ( value == 'Custom' ) {
		    sectCategoryRow.dom.hidden = true;
		    tContainer.dom.hidden = true;
            rectContainer.dom.hidden = true;
		    customSect.dom.hidden = false;
		};
	} );



    //Rectangle Sect


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

    rectContainer = new UI.Panel();

    rectContainer.add( hRow );
    rectContainer.add( bRow );
    rectContainer.dom.hidden = true;

    //t sect
    var h1Row = new UI.Row();
	var h1 = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {


	} );


	h1Row.add( new UI.Text( 'h' ).setWidth( '90px' ) );
	h1Row.add( h1 );

	var b1Row = new UI.Row();
	var b1 = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );

	b1Row.add( new UI.Text('b').setWidth( '90px' ) );
	b1Row.add( b1 );

	var t1Row = new UI.Row();
	var t1 = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );

	t1Row.add( new UI.Text('t1').setWidth( '90px' ) );
	t1Row.add( t1 );


	var t2Row = new UI.Row();
	var t2 = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );

	t2Row.add( new UI.Text('t2').setWidth( '90px' ) );
	t2Row.add( t2 );

    tContainer = new UI.Panel();

    var dRow = new UI.Row();
	var d = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );

	dRow.add( new UI.Text('d').setWidth( '90px' ) );
	dRow.add( d );

    tContainer = new UI.Panel();

    tContainer.add( h1Row );
    tContainer.add( b1Row );
    tContainer.add( t1Row );
    tContainer.add( t2Row );
    tContainer.add( dRow );
    tContainer.dom.hidden = true;

    // material Id
    var materialIdRow = new UI.Row();
	var materialId = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {


	} );
	materialIdRow.add( new UI.Text( 'Material Id' ).setWidth( '90px' ) );
	materialIdRow.add( materialId );
    // custom Sect
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

    customSect.add(ARow);
    customSect.add(IxRow);
    customSect.add(IyRow);
    customSect.add(IzRow);

    customSect.dom.hidden = true;

    var sectButtonRow = new UI.Row();
	var sectButton = new UI.Button( 'Define Section' ).onClick( function () {
        var value = sectType.getValue();
		if ( value == 'RECT' ){

		} else if ( value == 'T' ){

		}else if ( value == 'Custom' ) {
            mat_id = materialId.getValue();

            A_ = A.getValue();
            Ix_ = Ix.getValue();
            Iy_ = Iy.getValue();
            Iz_ = Iz.getValue();
            sect_id = editor.sections.sections.length+1
            editor.sections.sections.push({'id': sect_id, 'Material Id': mat_id, 'type': value, 'dimensions': 'ed', 'A': A_, 'Ix': Ix_, 'Iy': Iy_, 'Iz': Iz_})
            data = editor.sections.sections
            headers = ['id', 'Material Id', 'type', 'dimensions', 'A', 'Ix', 'Iy', 'Iz']
            sectDiv = document.getElementById( 'section-tab' )
            child = document.getElementById( 'sect_table' )
            sectDiv.removeChild(child);
            sectDiv.appendChild(buildTable(data, headers, 'sect_table'));
            editor.storage.set( editor.toJSON() );
            editor.signals.savingFinished.dispatch();
		};


	});

	sectButtonRow.add( sectButton );




	// section related
	editor.signals.savingFinished.add(function(){
        sectDiv = document.getElementById( 'section-tab' )
        //sectDiv.appendChild (Row.dom )
        sectDiv.appendChild( sectTypeRow.dom );
        sectDiv.appendChild( materialIdRow.dom );
        sectDiv.appendChild( customSect.dom );
        sectDiv.appendChild( rectContainer.dom );
        sectDiv.appendChild( tContainer.dom );
        sectDiv.appendChild( sectButtonRow.dom );
        //sectDiv.appendChild( matButtonRow.dom )
		data  = editor.sections.sections
		console.log(data)
        headers = ['id', 'Material id', 'type', 'dimensions', 'A', 'Ix', 'Iy', 'Iz']
        sectDiv.appendChild(buildTable(data, headers, 'sect_table'));
        //buildTable(data)
    })



    var buttonRow = new UI.Row();
    btn = new UI.Button('Build Section')
    btn.setId('openerSections')
    buttonRow.add(btn)
    container.add( buttonRow );

    /*

    */
	materialRow.add( new UI.Text( 'Material' ).setWidth( '90px' ) );
	materialRow.add( material );

	//container.add( materialRow );

	materialCategoryRow.add( new UI.Text( 'Material Category' ).setWidth( '90px' ) );
	materialCategoryRow.add( materialCategory );

	//container.add( materialCategoryRow );

	// section types


	//sectType.setOptions( options );

	sectTypeRow.add( sectType );

	container.add( sectTypeRow );

    container.add(customSect)
	//container.add( new Sidebar.Settings.Shortcuts( editor ) );




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
				//1editor.sections.sections = JSON.parse(e).data
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