/**
 * @author dforrer / https://github.com/dforrer
 * Developed as part of a project at University of Applied Sciences and Arts Northwestern Switzerland (www.fhnw.ch)
 */

/**
 * @param object THREE.Object3D
 * @constructor
 */

var RemoveObjectCommand = function ( object ) {

	Command.call( this );

	this.type = 'RemoveObjectCommand';
	this.name = 'Remove Object';

	this.object = object;
	this.parent = ( object !== undefined ) ? object.parent : undefined;
	if ( this.parent !== undefined ) {

		this.index = this.parent.children.indexOf( this.object );

	}

};

function render() {

	editor.sceneHelpers.updateMatrixWorld();
	editor.scene.updateMatrixWorld();

	editor.renderer.render( editor.scene, editor.camera );

	if ( editor.renderer instanceof THREE.RaytracingRenderer === false ) {

		editor.renderer.render( editor.sceneHelpers, editor.camera );

	}

}

RemoveObjectCommand.prototype = {

	execute: function () {

		var scope = this.editor;
		this.object.traverse( function ( child ) {

			scope.removeHelper( child );

		} );

		this.parent.remove( this.object );
		this.editor.select( this.parent );

		// the label does whatever the object does
		label = editor.sceneHelpers.getObjectByName( this.object.name )
		this.editor.sceneHelpers.remove( label) ;
		

		this.editor.signals.objectRemoved.dispatch( this.object );
		this.editor.signals.sceneGraphChanged.dispatch();
		
		// render()
	},

	undo: function () {

		var scope = this.editor;

		this.object.traverse( function ( child ) {

			if ( child.geometry !== undefined ) scope.addGeometry( child.geometry );
			if ( child.material !== undefined ) scope.addMaterial( child.material );

			scope.addHelper( child );

		
			
				
		} );

		this.parent.children.splice( this.index, 0, this.object );
		this.object.parent = this.parent;
		this.editor.select( this.object );
		
		let label = new SpriteText(this.object.userData.nn, 0.025);
		label.color = 'red';
		label.name = this.object.name
		if ( label.name.slice(0, 4) == 'Node' ){
			label.position.set( parseFloat(this.object.position.x)+0.1, parseFloat(this.object.position.y)+0.2, parseFloat(this.object.position.z)+0.1);
			this.editor.sceneHelpers.add( label) ;
		} else{
			nn1 = 'Node ' + this.object.userData.nodei;
			nn2 = 'Node ' + this.object.userData.nodej;
			node_i = this.editor.scene.getObjectByName( nn1 );
			node_j = this.editor.scene.getObjectByName( nn2 );
			
			x_lbl = (parseFloat(node_i.position.x)+parseFloat(node_j.position.x))/2+0.1
			y_lbl = (parseFloat(node_i.position.y)+parseFloat(node_j.position.y))/2+0.2
			z_lbl = (parseFloat(node_i.position.z)+parseFloat(node_j.position.z))/2+0.1
			label.position.set( x_lbl, y_lbl, z_lbl)
			console.log(label.position)
			this.editor.sceneHelpers.add( label);
		}
		
		
		

		

		this.editor.signals.objectAdded.dispatch( this.object );
		this.editor.signals.sceneGraphChanged.dispatch();

	},

	toJSON: function () {

		var output = Command.prototype.toJSON.call( this );
		output.object = this.object.toJSON();
		output.index = this.index;
		output.parentUuid = this.parent.uuid;

		return output;

	},

	fromJSON: function ( json ) {

		Command.prototype.fromJSON.call( this, json );

		this.parent = this.editor.objectByUuid( json.parentUuid );
		if ( this.parent === undefined ) {

			this.parent = this.editor.scene;

		}

		this.index = json.index;

		this.object = this.editor.objectByUuid( json.object.object.uuid );
		if ( this.object === undefined ) {

			var loader = new THREE.ObjectLoader();
			this.object = loader.parse( json.object );

		}

	}

};
