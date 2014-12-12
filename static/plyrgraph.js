// Written by Bharat Kunduri
// Based on the D3 Scatter Plot Example --> http://bl.ocks.org/weiglemc/6185069
var callback = function (dataGraph) {
  
  var links = new Array ();
  for (var i = 0; i < dataGraph.length; i++) {
    // links[i] = [ dataGraph[i]['source'], dataGraph[i]['target'], 
    // dataGraph[i]['StrikeRate'], dataGraph[i]['Matches'], dataGraph[i]['Dismissed'] ];
    currGraph = {}
    currGraph['source'] = dataGraph[i]['Batsman']
    currGraph['target'] = dataGraph[i]['Bowler']
    currGraph['Matches'] = dataGraph[i]['Matches']
    currGraph['Runs'] = dataGraph[i]['Runs']
    currGraph['Balls'] = dataGraph[i]['Balls']
    currGraph['StrikeRate'] = dataGraph[i]['StrikeRate']
    currGraph['Dismissed'] = dataGraph[i]['Dismissed']
    links[i] = currGraph
  }

  var nodes = {};

  // Compute the distinct nodes from the links.
  links.forEach(function(link) {
    link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
    link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
  });
  var width = 960,
    height = 500;

  var force = d3.layout.force()
    .nodes(d3.values(nodes))
    .links(links)
    .size([width, height])
    .linkDistance(200)
    .charge(-300)
    .on("tick", tick)
    .start();

  var svg = d3.select("#d3GraphPlyr").append("svg")
    .attr("width", width)
    .attr("height", height);

// Per-type markers, as they don't inherit styles.
svg.append("defs").selectAll("marker")
    .data(["connectionstyle"])
  .enter().append("marker")
    .attr("id", function(d) { return d; })
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 12)
    .attr("refY", 0.15)
    .attr("markerWidth", 3)
    .attr("markerHeight", 3)
    .attr("orient", "auto")
  .append("path")
    .attr("d", "M0,-5L10,0L0,5");

// add the tooltip area to the webpage
  var tooltip = d3.select("#d3GraphPlyr").append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);

// The link/paths between players
var path = svg.append("g").selectAll("path")
    .data(force.links())
  .enter().append("path")
    .attr("class", "link")
    .style("stroke", "steelblue")
    .attr("marker-end", function(d) { return "url(#" + "connectionstyle" + ")"; })
    .style('stroke-width', 5)
    .on("mouseover", function(d) {
          tooltip.transition()
               .duration(200)
               .style("opacity", 1.);
          tooltip.html( "Matches " + d.Matches 
            + "<br/> Dismissals : " + d.Dismissed
            + "<br/> Runs : " + d.Runs
            + "<br/> Balls : " + d.Balls
            + "<br/> StrikeRate : " + d.StrikeRate )
               .style("left", 725 + "px")
               .style("top", 70 + "px");
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(500)
               .style("opacity", 0);
      });



var circle = svg.append("g").selectAll("circle")
    .data(force.nodes())
  .enter().append("circle")
    .attr("r", 8)
    .call(force.drag);

var text = svg.append("g").selectAll("text")
    .data(force.nodes())
  .enter().append("text")
    .attr("x", 12)
    .attr("y", ".31em")
    .attr("font-size","12")
    .text(function(d) { return d.name; });

// Use elliptical arc path segments to doubly-encode directionality.
function tick() {
  path.attr("d", linkArc);
  circle.attr("transform", transform);
  text.attr("transform", transform);
}

function linkArc(d) {
  var dx = d.target.x - d.source.x,
      dy = d.target.y - d.source.y,
      dr = Math.sqrt(dx * dx + dy * dy);
  return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
}

function transform(d) {
  return "translate(" + d.x + "," + d.y + ")";
}

};
d3.json("/dataGraph", callback);
links = callback;
// window.open('www.yourdomain.com','_blank');
// var data = [[5,3], [10,17], [15,4], [2,8]];
// console.log( data )