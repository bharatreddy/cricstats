// Written by Bharat Kunduri
// Based on the D3 Scatter Plot Example --> http://bl.ocks.org/weiglemc/6185069
var callback = function (dataGraph) {
  
  // var dataset = new Array ();
  // for (var i = 0; i < dataGraph.length; i++) {
  //   dataset[i] = [ dataGraph[i]['Batsman'], dataGraph[i]['Bowler'], 
  //   dataGraph[i]['StrikeRate'], dataGraph[i]['Matches'], dataGraph[i]['Dismissed'] ];
  // }
console.log(dataGraph)
var width = 960,
    height = 500

var svg = d3.select("#d3GraphPlyr").append("svg")
    .attr("width", width)
    .attr("height", height);

var force = d3.layout.force()
    .gravity(.05)
    .distance(100)
    .charge(-100)
    .size([width, height]);  

// force.nodes(json.nodes)
//      .links(json.links)
//      .start();

//   var link = svg.selectAll(".link")
//       .data(json.links)
//     .enter().append("line")
//       .attr("class", "link");

//   var node = svg.selectAll(".node")
//       .data(json.nodes)
//     .enter().append("g")
//       .attr("class", "node")
//       .call(force.drag);

  // node.append("image")
  //     .attr("xlink:href", "https://github.com/favicon.ico")
  //     .attr("x", -8)
  //     .attr("y", -8)
  //     .attr("width", 16)
  //     .attr("height", 16);

  // node.append("text")
  //     .attr("dx", 12)
  //     .attr("dy", ".35em")
  //     .text(function(d) { return d.name });

  // force.on("tick", function() {
  //   link.attr("x1", function(d) { return d.Batsman.x; })
  //       .attr("y1", function(d) { return d.Batsman.y; })
  //       .attr("x2", function(d) { return d.Bowler.x; })
  //       .attr("y2", function(d) { return d.Bowler.y; });

  //   node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

};
d3.json("/dataGraph", callback);
dataset = callback;
// window.open('www.yourdomain.com','_blank');
// var data = [[5,3], [10,17], [15,4], [2,8]];
// console.log( data )