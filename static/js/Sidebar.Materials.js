/**
 * @author mrdoob / http://mrdoob.com/
 */
Sidebar.Materials = function ( editor ) {
	
	signals = editor.signals
	sectCount = 0;

	var container = new UI.Panel();
	container.setBorderTop( '0' );
	container.setPaddingTop( '20px' );
	container.setPaddingBottom( '20px' );

	
	
	var E_Row = new UI.Row();
	var E_ = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {


	} );

	E_Row.add( new UI.Text('E(kPa)').setWidth( '90px' ) );
	E_Row.add( E_ );
	container.add( E_Row );

	var GRow_ = new UI.Row();
	var G_ = new UI.Input( '' ).setLeft( '100px' ).onChange( function () {

	} );

	GRow_.add( new UI.Text('G(kPa)').setWidth( '90px' ) );
	GRow_.add( G_ );
	container.add(GRow_);


	var buttonRow = new UI.Row();
    btn = new UI.Button('Define Material').onClick( function (){
		mat = new THREE.Object3D();
        mat.name = 'Material ' + String(editor.sectMaterials.children.length+1)
        mat.userData = {'id': editor.sectMaterials.children.length+1,
                        'material_id': editor.sectMaterials.children.length+1,
                        'type': 'custom',
                        'E': parseFloat(E_.getValue()),
                        'G': parseFloat(G_.getValue())};

		editor.sectMaterials.add( mat );
		editor.storage.set( editor.toJSON() );
        editor.signals.savingFinished.dispatch();
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
		object = editor.sectMaterials.getObjectById( valueId );
		updateMaterialProperties( object.userData );

	} );


	container.add( outliner );
	container.add( new UI.Break() );
	
	var Materials = new THREE.Object3D()
    Materials.name = 'Materials'
	function refreshUI() {
		var ar = editor.sectMaterials.children;
		
		var options = [];

		options.push( buildOption( Materials, false ) );

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

	var materialIdRow = new UI.Row();
	var materialId = new UI.Number().setPrecision( 1 ).setWidth( '50px' )//.onChange( update );
	materialId.dom.disabled = true;
	materialId.dom.value = '';
	materialIdRow.add( new UI.Text( 'Material Id').setWidth( '90px' ) );
	materialIdRow.add( materialId );

	container.add( materialIdRow )

	
	var typeRow = new UI.Row();
	var type = new UI.Number().setPrecision( 1 ).setWidth( '50px' )//.onChange( update );
	type.dom.disabled = true;
	type.dom.value = '';
	typeRow.add( new UI.Text( 'Type').setWidth( '90px' ) );
	typeRow.add( type );

    container.add( typeRow )

    var ERow = new UI.Row();
	var E = new UI.Number().setPrecision( 2 ).setWidth( '50px' )//.onChange( update );
	E.dom.disabled = true;
	E.dom.value = '';
	ERow.add( new UI.Text( 'E').setWidth( '90px' ) );
	ERow.add( E );

	container.add( ERow );

	var GRow = new UI.Row();
	var G = new UI.Number().setPrecision( 2 ).setWidth( '50px' )//.onChange( update );
	G.dom.disabled = true;
	G.dom.value = '';
	GRow.add( new UI.Text( 'G').setWidth( '90px' ) );
	GRow.add( G );

	container.add( GRow );

	
	var updateMaterialProperties = function(values){
        materialId.dom.value = values.material_id;
		type.dom.value = values.type;
		E.dom.value = values.E;
		G.dom.value = values.G;
        
	};
	
		
	return container;

};