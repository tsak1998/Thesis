 function drawMqn(elementsResults){
    
    
  // Original Trace to select (heatmap)
  elm = parseInt(document.getElementById('element').value)
  type = document.getElementById('value').value
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

  Plotly.newPlot('graphMqn', data, layout, {displayModeBar: false});

  $(function(){
   $("#value").change(function(){
        var val = this.value;


        elm = parseInt(document.getElementById('element').value)

        x_ = elementsResults[elm]['x']
        y_ = elementsResults[elm][val]

        var data_update1 = {y: [y_],
                            x: [x_],
                            };
        var layout_update = {width:640,
                              height: 400,
                                title: 'Element '+elm+' '+val};
        Plotly.update('graphMqn', data_update1, layout_update, 0); 
  });

});

$(function(){

   $("#element").change(function(){
		var val = this.value;
        type = document.getElementById('value').value
        x_ = elementsResults[val]['x']
        y_ = elementsResults[val][type]
        var data_update1 = {y: [y_],
                            x: [x_],
                            };
        var layout_update = {width:640,
                             height: 400,
                                title: 'Element '+val+' '+type};
        Plotly.update('graphMqn', data_update1, layout_update, 0); 
	  });

});
}