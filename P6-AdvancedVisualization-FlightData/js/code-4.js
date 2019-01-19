function draw_flightStatusYears(data){
  var svg = dimple.newSvg('#chart_general_flights',"100%",400);



  var chart_ = new dimple.chart(svg,data);

  var x = chart_.addCategoryAxis("x","year");
  x.dateParseFormat = "%Y"; 
  x.overrideMax = 2010;
  x.minX = 2006;


  var a = chart_.addMeasureAxis("y","weather_ct_prop_by_year");
  var b = chart_.addMeasureAxis("y","carrier_ct_prop_by_year");
  var c = chart_.addMeasureAxis("y","nas_ct_prop_by_year");
  var d = chart_.addMeasureAxis("y","security_ct_prop_by_year");
  var e = chart_.addMeasureAxis("y","late_aircraft_ct_prop_by_year");
  var f = chart_.addMeasureAxis("y","arr_flights_prop_by_year");
  var g = chart_.addMeasureAxis("y","arr_del15_prop_by_year");




  a.showGridlines = false;
  b.showGridlines = false;
  c.showGridlines = false;
  d.showGridlines = false;
  e.showGridlines = false;
  f.showGridlines = false;
  g.showGridlines = false;



  b.hidden = true;
  c.hidden = true;
  d.hidden = true;
  e.hidden = true;
  f.hidden = true;
  g.hidden = true;

  chart_.defaultColors = [
            new dimple.color("green"),
            new dimple.color("yellow"),
            new dimple.color("red"),
            new dimple.color("blue"),
            new dimple.color("black"),
            new dimple.color("orange"),
            new dimple.color("grey")
      ]; 

  var s1 = chart_.addSeries("Weather",dimple.plot.line,[x,a]);
  chart_.addSeries("Carrier",dimple.plot.line,[x,b]);
  chart_.addSeries("NAS",dimple.plot.line,[x,c]);
  chart_.addSeries("Security",dimple.plot.line,[x,d]);
  chart_.addSeries("Late Aircraft",dimple.plot.line,[x,e]);
  var s2 = chart_.addSeries("On-Time",dimple.plot.line,[x,f]);
  chart_.addSeries("Late by 15mins+",dimple.plot.line,[x,g]);


  x.title = "";
  a.title = "";
  b.title = "";
  c.title = "";
  d.title = "";
  e.title = "";
  f.title = "";
  g.title = "";

  a.overrideMax = 100;
  a.minY = 0
  b.overrideMax = 100;
  b.minY = 0
  c.overrideMax = 100;
  c.minY = 0
  d.overrideMax = 100;
  d.minY = 0
  e.overrideMax = 100;
  e.minY = 0
  f.overrideMax = 100;
  f.minY = 0
  g.overrideMax = 100;
  g.minY = 0

  chart_.addLegend(750,0,380,30,"right");
  chart_.draw();




}


function draw_flightStatusMonths(data){
  var svg = dimple.newSvg('#chart_general_flights',"100%",400);



  var chart_ = new dimple.chart(svg,data);

  var x = chart_.addCategoryAxis("x","month");
  x.dateParseFormat = "%m"; 
  x.overrideMax = 12;
  x.minX = 1;
  ///x.tickFormat="%Y";
  //x.timeField = "date";
  //x.addOrderRule("year");


  var a = chart_.addMeasureAxis("y","weather_ct_prop_by_month");
  var b = chart_.addMeasureAxis("y","carrier_ct_prop_by_month");
  var c = chart_.addMeasureAxis("y","nas_ct_prop_by_month");
  var d = chart_.addMeasureAxis("y","security_ct_prop_by_month");
  var e = chart_.addMeasureAxis("y","late_aircraft_ct_prop_by_month");
  var f = chart_.addMeasureAxis("y","arr_flights_prop_by_month");
  var g = chart_.addMeasureAxis("y","arr_del15_prop_by_month");




  a.showGridlines = false;
  b.showGridlines = false;
  c.showGridlines = false;
  d.showGridlines = false;
  e.showGridlines = false;
  f.showGridlines = false;
  g.showGridlines = false;



  b.hidden = true;
  c.hidden = true;
  d.hidden = true;
  e.hidden = true;
  f.hidden = true;
  g.hidden = true;

  chart_.defaultColors = [
            new dimple.color("green"),
            new dimple.color("yellow"),
            new dimple.color("red"),
            new dimple.color("blue"),
            new dimple.color("black"),
            new dimple.color("orange"),
            new dimple.color("grey")
      ]; 


  chart_.addSeries("Weather",dimple.plot.line,[x,a]);
  chart_.addSeries("Carrier",dimple.plot.line,[x,b]);
  chart_.addSeries("NAS",dimple.plot.line,[x,c]);
  chart_.addSeries("Security",dimple.plot.line,[x,d]);
  chart_.addSeries("Late Aircraft",dimple.plot.line,[x,e]);
  chart_.addSeries("On-Time",dimple.plot.line,[x,f]);
  chart_.addSeries("Late by 15mins+",dimple.plot.line,[x,g]);

  a.tickFormat = "00.00";
  x.title = "";
  a.title = "";
  b.title = "";
  c.title = "";
  d.title = "";
  e.title = "";
  f.title = "";
  g.title = "";

  a.overrideMax = 100;
  a.minY = 0
  b.overrideMax = 100;
  b.minY = 0
  c.overrideMax = 100;
  c.minY = 0
  d.overrideMax = 100;
  d.minY = 0
  e.overrideMax = 100;
  e.minY = 0
  f.overrideMax = 100;
  f.minY = 0
  g.overrideMax = 100;
  g.minY = 0

  chart_.addLegend(750,0,380,30,"right");
  chart_.draw();




}











function draw_FlightDelayYears(data){

  var svg = dimple.newSvg('#chart_delayedFlights',"100%",400);



  var chart_ = new dimple.chart(svg,data);

  var x = chart_.addCategoryAxis("x","year");
  x.dateParseFormat = "%Y"; 
  x.overrideMax = 2010;
  x.minX = 2006;

  var a = chart_.addMeasureAxis("y","weather_ct_prop_by_year");
  var b = chart_.addMeasureAxis("y","carrier_ct_prop_by_year");
  var c = chart_.addMeasureAxis("y","nas_ct_prop_by_year");
  var d = chart_.addMeasureAxis("y","security_ct_prop_by_year");
  var e = chart_.addMeasureAxis("y","late_aircraft_ct_prop_by_year");
  var f = chart_.addMeasureAxis("y","arr_cancelled_prop_by_year");
  var g = chart_.addMeasureAxis("y","arr_diverted_prop_by_year");


  a.showGridlines = false;
  b.showGridlines = false;
  c.showGridlines = false;
  d.showGridlines = false;
  e.showGridlines = false;
  f.showGridlines = false;
  g.showGridlines = false;


  b.hidden = true;
  c.hidden = true;
  d.hidden = true;
  e.hidden = true;
  f.hidden = true;
  g.hidden = true;


  chart_.defaultColors = [
            new dimple.color("green"),
            new dimple.color("yellow"),
            new dimple.color("red"),
            new dimple.color("blue"),
            new dimple.color("black"),
            new dimple.color("orange"),
            new dimple.color("grey")
      ]; 

  chart_.addSeries("Weather",dimple.plot.line,[x,a]);
  chart_.addSeries("Carrier",dimple.plot.line,[x,b]);
  chart_.addSeries("NAS",dimple.plot.line,[x,c]);
  chart_.addSeries("Security",dimple.plot.line,[x,d]);
  chart_.addSeries("Late Aircraft",dimple.plot.line,[x,e]);
  chart_.addSeries("Cancelled",dimple.plot.line,[x,f]);
  chart_.addSeries("Diverted Cancellation",dimple.plot.line,[x,g]);
  

  a.tickFormat = "00.00";
  x.title = "";
  a.title = "";
  b.title = "";
  c.title = "";
  d.title = "";
  e.title = "";
  f.title = "";
  g.title = "";

  a.overrideMax = 5;
  a.minY = 0
  b.overrideMax = 5;
  b.minY = 0
  c.overrideMax = 5;
  c.minY = 0
  d.overrideMax = 5;
  d.minY = 0
  e.overrideMax = 5;
  e.minY = 0
  f.overrideMax = 5;
  f.minY = 0
  g.overrideMax = 5;
  g.minY = 0

  chart_.addLegend(750,0,380,30,"right");
  chart_.draw();
    }





function draw_FlightDelayMonths(data){

  var svg = dimple.newSvg('#chart_delayedFlights',"100%",400);



  var chart_ = new dimple.chart(svg,data);

  var x = chart_.addCategoryAxis("x","month");
  x.dateParseFormat = "%m";
  x.overrideMax = 12;
  x.minX = 1;

  var a = chart_.addMeasureAxis("y","weather_ct_prop_by_month");
  var b = chart_.addMeasureAxis("y","carrier_ct_prop_by_month");
  var c = chart_.addMeasureAxis("y","nas_ct_prop_by_month");
  var d = chart_.addMeasureAxis("y","security_ct_prop_by_month");
  var e = chart_.addMeasureAxis("y","late_aircraft_ct_prop_by_month");
  var f = chart_.addMeasureAxis("y","arr_cancelled_prop_by_month");
  var g = chart_.addMeasureAxis("y","arr_diverted_prop_by_month");


  a.showGridlines = false;
  b.showGridlines = false;
  c.showGridlines = false;
  d.showGridlines = false;
  e.showGridlines = false;
  f.showGridlines = false;
  g.showGridlines = false;


  b.hidden = true;
  c.hidden = true;
  d.hidden = true;
  e.hidden = true;
  f.hidden = true;
  g.hidden = true;


  chart_.defaultColors = [
            new dimple.color("green"),
            new dimple.color("yellow"),
            new dimple.color("red"),
            new dimple.color("blue"),
            new dimple.color("black"),
            new dimple.color("orange"),
            new dimple.color("grey")
      ]; 

  chart_.addSeries("Weather",dimple.plot.line,[x,a]);
  chart_.addSeries("Carrier",dimple.plot.line,[x,b]);
  chart_.addSeries("NAS",dimple.plot.line,[x,c]);
  chart_.addSeries("Security",dimple.plot.line,[x,d]);
  chart_.addSeries("Late Aircraft",dimple.plot.line,[x,e]);
  chart_.addSeries("Cancelled",dimple.plot.line,[x,f]);
  chart_.addSeries("Diverted Cancellation",dimple.plot.line,[x,g]);
  

  a.tickFormat = "00.00";
  x.title = "";
  a.title = "";
  b.title = "";
  c.title = "";
  d.title = "";
  e.title = "";
  f.title = "";
  g.title = "";

  a.overrideMax = 5;
  a.minY = 0
  b.overrideMax = 5;
  b.minY = 0
  c.overrideMax = 5;
  c.minY = 0
  d.overrideMax = 5;
  d.minY = 0
  e.overrideMax = 5;
  e.minY = 0
  f.overrideMax = 5;
  f.minY = 0
  g.overrideMax = 5;
  g.minY = 0

  chart_.addLegend(750,0,380,30,"right");
  chart_.draw();
    }


