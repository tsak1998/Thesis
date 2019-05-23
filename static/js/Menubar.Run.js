/**
 * @author mrdoob / http://mrdoob.com/
 */

Menubar.Run = function ( editor ) {

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
	title.setTextContent( 'Run' );
	container.add( title );

	var options = new UI.Panel();
	options.setClass( 'options' );
	container.add( options );

	// rUN
	/**
 * Posts javascript data to a url using form.submit().  
 * Note: Handles json and arrays.
 * @param {string} path - url where the data should be sent.
 * @param {string} data - data as javascript object (JSON).
 * @param {object} options -- optional attributes
 *  { 
 *    {string} method: get/post/put/etc,
 *    {string} arrayName: name to post arraylike data.  Only necessary when root data object is an array.
 *  }
 * @example postToUrl('/UpdateUser', {Order {Id: 1, FirstName: 'Sally'}});
 */
	function postToUrl(path, data, options) {
		if (options === undefined) {
			options = {};
		}

		var method = options.method || "post"; // Set method to post by default if not specified.

		var form = document.createElement("form");
		form.setAttribute("method", method);
		form.setAttribute("action", path);

		function constructElements(item, parentString) {
			for (var key in item) {
				if (item.hasOwnProperty(key) && item[key] != null) {
					if (Object.prototype.toString.call(item[key]) === '[object Array]') {
						for (var i = 0; i < item[key].length; i++) {
							constructElements(item[key][i], parentString + key + "[" + i + "].");
						}
					} else if (Object.prototype.toString.call(item[key]) === '[object Object]') {
						constructElements(item[key], parentString + key + ".");
					} else {
						var hiddenField = document.createElement("input");
						hiddenField.setAttribute("type", "hidden");
						hiddenField.setAttribute("name", parentString + key);
						hiddenField.setAttribute("value", item[key]);
						form.appendChild(hiddenField);function postToUrl(path, data, options) {
							if (options === undefined) {
								options = {};
							}
						
							var method = options.method || "post"; // Set method to post by default if not specified.
						
							var form = document.createElement("form");
							form.setAttribute("method", method);
							form.setAttribute("action", path);
						
							function constructElements(item, parentString) {
								for (var key in item) {
									if (item.hasOwnProperty(key) && item[key] != null) {
										if (Object.prototype.toString.call(item[key]) === '[object Array]') {
											for (var i = 0; i < item[key].length; i++) {
												constructElements(item[key][i], parentString + key + "[" + i + "].");
											}
										} else if (Object.prototype.toString.call(item[key]) === '[object Object]') {
											constructElements(item[key], parentString + key + ".");
										} else {
											var hiddenField = document.createElement("input");
											hiddenField.setAttribute("type", "hidden");
											hiddenField.setAttribute("name", parentString + key);
											hiddenField.setAttribute("value", item[key]);
											form.appendChild(hiddenField);
										}
									}
								}
							}
						
							//if the parent 'data' object is an array we need to treat it a little differently
							if (Object.prototype.toString.call(data) === '[object Array]') {
								if (options.arrayName === undefined) console.warn("Posting array-type to url will doubtfully work without an arrayName defined in options.");
								//loop through each array item at the parent level
								for (var i = 0; i < data.length; i++) {
									constructElements(data[i], (options.arrayName || "") + "[" + i + "].");
								}
							} else {
								//otherwise treat it normally
								constructElements(data, "");
							}
						
							document.body.appendChild(form);
							form.submit();
						};
						
					}
				}
			}
		}

		//if the parent 'data' object is an array we need to treat it a little differently
		if (Object.prototype.toString.call(data) === '[object Array]') {
			if (options.arrayName === undefined) console.warn("Posting array-type to url will doubtfully work without an arrayName defined in options.");
			//loop through each array item at the parent level
			for (var i = 0; i < data.length; i++) {
				constructElements(data[i], (options.arrayName || "") + "[" + i + "].");
			}
		} else {
			//otherwise treat it normally
			constructElements(data, "");
		}

		document.body.appendChild(form);
		form.submit();
	};

	var option = new UI.Row();
    option.setClass( 'option' );
    option.setTextContent( 'Run' );
	option.setId( 'run' );
    option.onClick( function () {

        if ( confirm( 'Run analysis' ) ) {
                        
			data1 = []
			var model = editor.scene.children;
	
			//model = JSON.stringify( model );
	
			var sections = editor.sections;
	
			//sections = JSON.stringify( sections );
	
			data1.push( model )
			data1.push( sections )
	
	
			data1 = JSON.stringify( data1 );
	
			$.ajax({
				type: "POST",
				url: '/yellow',
				contentType: "application/json; charset=utf-8",
				dataType: "json",
				data: data1,
	
			});

        }

    } );
    options.add( option );

	//

	options.add( new UI.HorizontalRule() );

	// Import


	return container;

};
