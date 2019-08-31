/**
 * @author mrdoob / http://mrdoob.com/
 */
Sidebar.Sections = function ( editor ) {
	
	signals = editor.signals
	sectCount = 0;

	var container = new UI.Panel();
	container.setBorderTop( '0' );
	container.setPaddingTop( '20px' );
	container.setPaddingBottom( '20px' );

	
	
	var materialRow_ = new UI.Row();
	var material_ = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {


	} );

	materialRow_.add( new UI.Text('Material Id').setWidth( '90px' ) );
	materialRow_.add( material_ );
	container.add(materialRow_)

	var ARow_ = new UI.Row();
	var A_ = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );

	ARow_.add( new UI.Text('A').setWidth( '90px' ) );
	ARow_.add( A_ );
	container.add(ARow_)


	var IxRow_ = new UI.Row();
	var Ix_ = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );

	IxRow_.add( new UI.Text('Ix').setWidth( '90px' ) );
	IxRow_.add( Ix_ );
	container.add(IxRow_)

	var IyRow_ = new UI.Row();
	var Iy_ = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );

	IyRow_.add( new UI.Text('Iy').setWidth( '90px' ) );
	IyRow_.add( Iy_ );
	container.add(IyRow_)

	var IzRow_ = new UI.Row();
	var Iz_ = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );

	IzRow_.add( new UI.Text('Iz').setWidth( '90px' ) );
	IzRow_.add( Iz_ );
	container.add(IzRow_);

	var buttonRow = new UI.Row();
    btn = new UI.Button('Define Section').onClick( function (){
		console.log(';akiii')
		sect = new THREE.Object3D();
        sect.name = 'Section ' + String(editor.sections.children.length+1)
        sect.userData = {'id': editor.sections.children.length+1,
                        'section_id': editor.sections.children.length+1,
                        'material': parseInt(material_.getValue()),
                        'dimensions': 'custom',
                        'type': 'custom',
                        'A': parseFloat(A_.getValue()),
                        'Ix': parseFloat(Ix_.getValue()),
                        'Iy': parseFloat(Iy_.getValue()),
                        'Iz': parseFloat(Iz_.getValue())};

		editor.sections.add( sect );
		refreshUI();
	});
    buttonRow.add(btn);
	container.add( buttonRow );
		
		
	
	function buildOption( object, draggable ) {

		var option = document.createElement( 'div' );
		option.draggable = draggable;
		option.innerHTML = buildHTML( object );
		option.value = object.id;

		return option;

	}

	function escapeHTML( html ) {

		return html
			.replace( /&/g, '&amp;' )
			.replace( /"/g, '&quot;' )
			.replace( /'/g, '&#39;' )
			.replace( /</g, '&lt;' )
			.replace( />/g, '&gt;' );

	}

	function getMaterialName( material ) {

		if ( Array.isArray( material ) ) {

			var array = [];

			for ( var i = 0; i < material.length; i ++ ) {

				array.push( material[ i ].name );

			}

			return array.join( ',' );

		}

		return material.name;

	}

	function getScript( uuid ) {

		if ( editor.scripts[ uuid ] !== undefined ) {

			return ' <span class="type Script"></span>';

		}

		return '';

	}

	var ignoreObjectSelectedSignal = false;

	function buildHTML( object ) {

		var html = '<span class="type ' + object.type + '"></span> ' + escapeHTML( object.name );

		if ( object instanceof THREE.Mesh ) {

			var geometry = object.geometry;
			var material = object.material;

			html += ' <span class="type ' + geometry.type + '"></span> ' + escapeHTML( geometry.name );
			html += ' <span class="type ' + material.type + '"></span> ' + escapeHTML( getMaterialName( material ) );

		}

		html += getScript( object.uuid );

		return html;

	}

	var outliner = new UI.Outliner( editor );
	outliner.setId( 'outliner' );
	outliner.onChange( function () {
		editor.selected = null
		outliner.value = null
		ignoreObjectSelectedSignal = true;
        valueId = parseInt( outliner.getValue() );
		object = editor.sections.getObjectById( valueId );
		updateSectionProperties( object.userData );

	} );


	container.add( outliner );
	container.add( new UI.Break() );
	
	var Sections = new THREE.Object3D()
    Sections.name = 'Sections'
	function refreshUI() {
		var ar = editor.sections.children;
		
		var options = [];

		options.push( buildOption( Sections, false ) );

		( function addObjects( objects, pad ) {

			for ( var i = 0, l = objects.length; i < l; i ++ ) {

				var object = objects[ i ];

				var option = buildOption( object, true );
				option.style.paddingLeft = ( pad * 10 ) + 'px';
				options.push( option );

				// addObjects( object.children, pad + 1 );

			}

		} )
		(ar, 1 );

		outliner.setOptions( options );
		
		if ( editor.selected !== null ) {

			outliner.setValue( editor.selected.id );

		}

	}
	signals.editorCleared.add( refreshUI );

	signals.savingFinished.add( refreshUI );

	signals.objectChanged.add( function ( object ) {

		var options = outliner.options;

		for ( var i = 0; i < options.length; i ++ ) {

			var option = options[ i ];

			if ( option.value === object.id ) {

				option.inumbererHTML = buildHTML( object );
				return;

			};

		};

	} );

	signals.objectSelected.add( function ( object ) {

	    if (object!=null){
	        outliner.setValue( null );
        };
		if ( ignoreObjectSelectedSignal === true ) return;

		outliner.setValue( object !== null ? object.id : null );

	} );

	refreshUI();

	var sectIdRow = new UI.Row();
	var sectId = new UI.Number().setPrecision( 0 ).setWidth( '30px' )//.onChange( update );
	sectId.min = 1;
	sectId.max = 100;
	sectId.step = 100;
	sectId.dom.value = '';

	sectIdRow.add( new UI.Text( 'Section Id').setWidth( '90px' ) );
	sectIdRow.add( sectId );

	container.add( sectIdRow );
	// position

	var materialIdRow = new UI.Row();
	var materialId = new UI.Number().setPrecision( 1 ).setWidth( '50px' )//.onChange( update );
	materialId.dom.disabled = true;
	materialId.dom.value = '';
	materialIdRow.add( new UI.Text( 'Material').setWidth( '90px' ) );
	materialIdRow.add( materialId );

	container.add( materialIdRow )

	var dimensionsRow = new UI.Row();
	var dimensions = new UI.Number().setPrecision( 1 ).setWidth( '50px' )//.onChange( update );
	dimensions.dom.disabled = true;
	dimensions.dom.value = '';
	dimensionsRow.add( new UI.Text( 'Dimensions').setWidth( '90px' ) );
	dimensionsRow.add( dimensions );

	container.add( dimensionsRow )
	
	var typeRow = new UI.Row();
	var type = new UI.Number().setPrecision( 1 ).setWidth( '50px' )//.onChange( update );
	type.dom.disabled = true;
	type.dom.value = '';
	typeRow.add( new UI.Text( 'Type').setWidth( '90px' ) );
	typeRow.add( type );

    container.add( dimensionsRow )

    var ARow = new UI.Row();
	var A = new UI.Number().setPrecision( 1 ).setWidth( '50px' )//.onChange( update );
	A.dom.disabled = true;
	A.dom.value = '';
	ARow.add( new UI.Text( 'Area').setWidth( '90px' ) );
	ARow.add( A );

	container.add( ARow );

	var IxRow = new UI.Row();
	var Ix = new UI.Number().setPrecision( 1 ).setWidth( '50px' )//.onChange( update );
	Ix.dom.disabled = true;
	Ix.dom.value = '';
	IxRow.add( new UI.Text( 'Ix').setWidth( '90px' ) );
	IxRow.add( Ix );

	container.add( IxRow );

	var IyRow = new UI.Row();
	var Iy = new UI.Number().setPrecision( 1 ).setWidth( '50px' )//.onChange( update );
	Iy.dom.disabled = true;
	Iy.dom.value = '';
	IyRow.add( new UI.Text( 'Iy').setWidth( '90px' ) );
	IyRow.add( Iy );

	container.add( IyRow );

	var IzRow = new UI.Row();
	var Iz = new UI.Number().setPrecision( 1 ).setWidth( '50px' )//.onChange( update );
	Iz.dom.disabled = true;
	Iz.dom.value = '';
	IzRow.add( new UI.Text( 'Iz').setWidth( '90px' ) );
	IzRow.add( Iz );

	container.add( IzRow );

	var updateSectionProperties = function(values){
		sectId.dom.value = values.section_id;
        materialId.dom.value = values.material;
        dimensions.dom.value = values.dimensions;
		type.dom.value = values.type;
		A.dom.value = values.A;
		Ix.dom.value = values.Ix;
		Iy.dom.value = values.Iy;
		Iz.dom.value = values.Iz;
        
	};
	
		
	return container;

};