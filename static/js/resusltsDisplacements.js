 function drawDisplacements(elementsResults){
    uxi = [0, -0.115,-0.0737,0.005]
    uxj = [0.005, -0.115,-0.0737,0]
    for (j=1; j<5; j++){

      
      vertices = []
      vec = new THREE.Vector3(elementsResults[j].x[0]+uxi[j],elementsResults[j].uz[0], elementsResults[j].uy[0])
      vertices.push(vec)
      for (i=1; i<49; i++){
        vec = new THREE.Vector3(elementsResults[j].x[i],elementsResults[j].uz[i], elementsResults[j].uy[i])
        vertices.push(vec)
      }
      vec = new THREE.Vector3(elementsResults[j].x[49]+uxj[j],elementsResults[j].uz[49], elementsResults[j].uy[49])
      vertices.push(vec)
      var curve = new THREE.SplineCurve( vertices );

      var points = curve.getPoints( 50 );

      var geometry = new THREE.BufferGeometry().setFromPoints( points );

      var material = new THREE.LineBasicMaterial( { color : 0xff0000 } );

      // Create the final object to add to the scene
      curveObject = new THREE.Line( geometry, material );
      elmnt = editor.scene.getObjectByName('Element '+String(j))
      curveObject.applyMatrix(elmnt.matrix)
      editor.sceneHelpers.add(curveObject)
    }
    veci =  new THREE.Vector3(0,0,0)
    veci_ =  new THREE.Vector3(0.09514121916372137,0, 0.030792018706813248 )
    vecj_ = new THREE.Vector3(3.988195873785236, -0.3292969600376067,1.3887318170349765 )
    vecj = new THREE.Vector3(3.998724521260001,-0.3338,1.39107724697  )

    var curve = new THREE.SplineCurve( [veci, veci_, vecj_, vecj_] );

      var points = curve.getPoints( 50 );

      var geometry = new THREE.BufferGeometry().setFromPoints( points );

      var material = new THREE.LineBasicMaterial( { color : 0xff0000 } );

      // Create the final object to add to the scene
      curveObject = new THREE.Line( geometry, material );
      elmnt = editor.scene.getObjectByName('Element '+String(j))
      //curveObject.applyMatrix(elmnt.matrix)
      editor.sceneHelpers.add(curveObject)

    // Original Trace to select (heatmap)
    elm = parseInt(document.getElementById('element2').value)
    type = document.getElementById('value2').value
    x_ = elementsResults[elm]['x']
    y_ = elementsResults[elm][type]
    var orgTrace = {
      y: y_,
      x: x_,
      fill: 'tozeroy',
      type: 'scatter'
    };

    var data = [orgTrace];

    var height = 100;
    var layout = {width:730,
                  height: 500,
                  title: 'Element '+elm+' '+type,
                  displayModeBar: false};

    Plotly.newPlot('graphDisplacements', data, layout, {displayModeBar: false});

    $(function(){
    $("#value2").change(function(){
          var val = this.value;


          elm = parseInt(document.getElementById('element2').value)

          x_ = elementsResults[elm]['x']
          y_ = elementsResults[elm][val]

          var data_update1 = {y: [y_],
                              x: [x_],
                              };
          var layout_update = {width: 730,
                                  height: 500,
                                  title: 'Element '+elm+' '+val};
          Plotly.update('graphDisplacements', data_update1, layout_update, 0); 
    });

  });

  $(function(){

    $("#element2").change(function(){
      var val = this.value;
          type = document.getElementById('value2').value
          x_ = elementsResults[val]['x']
          y_ = elementsResults[val][type]
          var data_update1 = {y: [y_],
                              x: [x_],
                              };
          var layout_update = {width: 730,
                                  height: 500,
                                  title: 'Element '+val+' '+type};
          Plotly.update('graphDisplacements', data_update1, layout_update, 0); 
      });

  });
}