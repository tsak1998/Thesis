/**
 * @author dforrer / https://github.com/dforrer
 * Developed as part of a project at University of Applied Sciences and Arts Northwestern Switzerland (www.fhnw.ch)
 */

/**
 * @param object THREE.Object3D
 * @constructor
 */

var AddObjectCommand = function ( object ) {

    Command.call( this );

    this.type = 'AddObjectCommand';

    this.object = object;
    if ( object !== undefined ) {

        this.name = 'Add Object: ' + object.name;

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

AddObjectCommand.prototype = {


    execute: function () {
    
        this.editor.addObject( this.object );
        //to add the label and loads 
        
        /*
        console.log( this.object )
        for (i = 0; i<this.object.extra.length; i++){
            this.editor.sceneHelpers.add( this.object.extra[i] );
            console.log( this.object.extra[i] )
        }
    */
        //this.editor.select( this.object );
        

    },

    undo: function () {

        this.editor.removeObject( this.object );
		// this.editor.sceneHelpers.remove( this.editor.sceneHelpers.getObjectByName( this.object.name ) );
		this.editor.sceneHelpers.getObjectByName( this.object.name ).visible = false;
        // render();
        this.editor.deselect();

    },

    toJSON: function () {

        var output = Command.prototype.toJSON.call( this );
        output.object = this.object.toJSON();

        return output;

    },

    fromJSON: function ( json ) {

        Command.prototype.fromJSON.call( this, json );

        this.object = this.editor.objectByUuid( json.object.object.uuid );

        if ( this.object === undefined ) {

            var loader = new THREE.ObjectLoader();
            this.object = loader.parse( json.object );

        }

    }

};