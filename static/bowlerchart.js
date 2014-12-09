// Written by Bharat Kunduri
// Based on the D3 Scatter Plot Example --> http://bl.ocks.org/weiglemc/6185069
var callback = function (dataBowler) {
  
  var dataset = new Array ();
  for (var i = 0; i < dataBowler.length; i++) {
    dataset[i] = [ dataBowler[i]['Matches'], dataBowler[i]['Runs'], dataBowler[i]['Balls'], 
    dataBowler[i]['Name'], dataBowler[i]['RunRate'], dataBowler[i]['Wickets'] ];
  }

  var data = dataBowler.slice();
  var nRepoFn = function(d) { return d.Wickets; }
  var dataXFn = function(d) { return d.RunRate; }

  var margin = {top: 20, right: 10, bottom: 30, left: 60},
    width = 960 - margin.left - margin.right,
    height = 375 - margin.top - margin.bottom;

  // setup x 
  var xValue = function(d) { return d.RunRate;}, // data -> value
      xScale = d3.scale.linear().range([0, width]), // value -> display
      xMap = function(d) { return xScale(xValue(d));}, // data -> display
      xAxis = d3.svg.axis().scale(xScale).orient("bottom");
  // setup y
  var yValue = function(d) { return d.Wickets;}, // data -> value
      yScale = d3.scale.linear().range([height, 0]), // value -> display
      yMap = function(d) { return yScale(yValue(d));}, // data -> display
      yAxis = d3.svg.axis().scale(yScale).orient("left");
  // add the graph canvas to the body of the webpage
  var svg = d3.select("#d3plotBowler").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  // add the tooltip area to the webpage
  var tooltip = d3.select("#d3plotBowler").append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);
  // don't want dots overlapping axis, so add in buffer to data domain
  xScale.domain([d3.min(data, xValue), d3.max(data, xValue)+1]);
  yScale.domain([d3.min(data, yValue), d3.max(data, yValue)+10]);

// x-axis
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("RunRate");
// y-axis
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .attr("font-family", "sans-serif")
      .attr("font-size", "20px")
      .style("text-anchor", "end")
      .text("Wickets");
// draw dots
// Set up fill color for dots
// setup fill color
// var cValue = function(d) { return d.Matches;},
//     color = d3.scale.category10();
  var outageThresholds = [ 1, 10, 25, 50, 100 ];
  var interpolateColor = d3.interpolateHcl("#F0F8FF", "#08457E");
  var thresholdColors = d3.range(outageThresholds.length + 1).map(function(d, i) { return interpolateColor(i / outageThresholds.length); })
  // ['rgb(253,208,162)','rgb(253,174,107)','rgb(253,141,60)','rgb(241,105,19)','rgb(217,72,1)','rgb(140,45,4)'];
  var outColor = d3.scale.threshold()
                 .domain(outageThresholds)
                 .range(thresholdColors);
  var commasFormatter = d3.format(",");

  svg.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", function(d) { return 10. })
      .attr("cx", xMap)
      .attr("cy", yMap)
      .style("fill", function(d) { return outColor(d.Matches);}) 
      .on("mouseover", function(d) {
          tooltip.transition()
               .duration(200)
               .style("opacity", 1.);
          tooltip.html(d.Name + "<br/> Matches : " + d.Matches + "<br/> Balls : " + d.Balls
          + "<br/> Wickets : " + d.Wickets + "<br/> Runs : " + d.Runs + "<br/> Runrate : " + d.RunRate )
               .style("left", 725 + "px")
               .style("top", 70 + "px");
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(500)
               .style("opacity", 0);
      });
      // now build the legend
      legend = svg.selectAll(".lentry")
                          .data(outColor.domain())
                          .enter()
                          .append("g")
                          .attr("class","leg")
     legend.append("rect")
              .attr("y", function(d,i) { return(i*40)})
              .attr("x", function(d,i) { return(775)})
              .attr("width","20px")
              .attr("height","40px")
              .attr("fill", function(d) { return outColor(d) ; })
              .attr("stroke","#7f7f7f")
              .attr("stroke-width","0.5");
    legend.append("text")
              .attr("class", "legText")
              .text(function(d, i) { return commasFormatter(outageThresholds[i])+" Matches" ; })
              .attr("x", 800)
              .attr("fill", "#fff")
              .attr("y", function(d, i) { return (40 * i) + 20 + 4; });

      // .on("click", function(d) 
      // { 
      //         window.open('https://github.com/'+d.Name,'_blank'); 
      // }); 

};
d3.json("/dataBowler", callback);
dataset = callback;
// window.open('www.yourdomain.com','_blank');
// var data = [[5,3], [10,17], [15,4], [2,8]];
// console.log( data )