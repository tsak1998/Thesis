 function drawDisplacements(elementsResults, deformed){
    console.log(deformed)
  for (j=1; j<9; j++){
    elmnt = elementsResults[j]
    vertices = []
    for (i=0; i<50; i++){
     
        vec = new THREE.Vector3(elmnt['x'][i] ,10*elmnt['uz'][i], 10*elmnt['uy'][i])
        vertices.push(vec)
      }
      
      var curve = new THREE.CatmullRomCurve3( vertices );

      var points = curve.getPoints( 100 );
      
      var geometry = new THREE.BufferGeometry().setFromPoints( points );

      var material = new THREE.LineBasicMaterial( { color : 0xff0000 } );

      // Create the final object to add to the scene
      curveObject = new THREE.Line( geometry, material );
      elmnt = editor.scene.getObjectByName('Element '+String(j))
      //curveObject.applyMatrix(elmnt.matrix)
      //editor.sceneHelpers.add(curveObject)
    }
   
   

    
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
    var layout = {width:640,
                  height: 400,
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
          var layout_update = {width:640,
                                height: 400,
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
          var layout_update = {width:640,
                                height: 400,
                                  title: 'Element '+val+' '+type};
          Plotly.update('graphDisplacements', data_update1, layout_update, 0); 
      });

  });
}