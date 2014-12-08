// Written by Bharat Kunduri
// Based on the D3 Scatter Plot Example --> http://bl.ocks.org/weiglemc/6185069
var callback = function (dataUser) {
  
  var dataset = new Array ();
  for (var i = 0; i < dataUser.length; i++) {
    dataset[i] = [ dataUser[i]['nflwrs'], dataUser[i]['nrepos'], dataUser[i]['login'] ];
  }

  var data = dataUser.slice();
  var nRepoFn = function(d) { return d.nrepos; }
  var dataXFn = function(d) { return d.nflwrs; }

  var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 375 - margin.top - margin.bottom;

  // setup x 
  var xValue = function(d) { return d.nflwrs;}, // data -> value
      xScale = d3.scale.linear().range([0, width]), // value -> display
      xMap = function(d) { return xScale(xValue(d));}, // data -> display
      xAxis = d3.svg.axis().scale(xScale).orient("bottom");
  // setup y
  var yValue = function(d) { return d.nrepos;}, // data -> value
      yScale = d3.scale.linear().range([height, 0]), // value -> display
      yMap = function(d) { return yScale(yValue(d));}, // data -> display
      yAxis = d3.svg.axis().scale(yScale).orient("left");
  // add the graph canvas to the body of the webpage
  var svg = d3.select("#d3plotBatsman").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  // add the tooltip area to the webpage
  var tooltip = d3.select("#d3plotBatsman").append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);
  // don't want dots overlapping axis, so add in buffer to data domain
  xScale.domain([d3.min(data, xValue)-1, d3.max(data, xValue)+1000]);
  yScale.domain([d3.min(data, yValue)-1, d3.max(data, yValue)+1]);

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
      .text("Num. Followers");
// y-axis
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Num. Repos");
// draw dots
  svg.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", function(d) { return xValue(d)/500. })
      .attr("cx", xMap)
      .attr("cy", yMap)
      .on("mouseover", function(d) {
          tooltip.transition()
               .duration(200)
               .style("opacity", 1.);
          tooltip.html(d.login + "<br/> Followers : " + xValue(d) 
          + "<br/> Repositories : " + yValue(d) )
               .style("left", 800 + "px")
               .style("top", 75 + "px");
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(500)
               .style("opacity", 0);
      })
      .on("click", function(d) 
      { 
              window.open('https://github.com/'+d.login,'_blank'); 
      }); 

};
d3.json("/dataUser", callback);
dataset = callback;
// window.open('www.yourdomain.com','_blank');
// var data = [[5,3], [10,17], [15,4], [2,8]];
// console.log( data )