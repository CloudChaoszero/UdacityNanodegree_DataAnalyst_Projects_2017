function draw_weatherDelay(data){
      var svg = dimple.newSvg('#chart_weather_delay',400,400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);
        
      });
      data.forEach(function(d){
        d['weather_delay'] = +d['weather_delay'];
      });
      
      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");


      var y = chart_.addMeasureAxis("y","weather_delay");
      y.showGridlines = false;
      chart_.addColorAxis("weather_delay","black");
      chart_.addSeries(null,dimple.plot.line);
      
      chart_.addSeries(null,dimple.plot.scatter);

      x.title = "";
      y.title = "";
      y.overrideMax = 4500000;
      chart_.draw();
    }

function draw_onTimeArrival(data){
      var id_chart = '#chart_arr_flights';
      var svg = dimple.newSvg(id_chart,"100%",400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);

      });

      data.forEach(function(d){
        d['arr_flights'] = +d['arr_flights'];
      });


      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","arr_flights");
      y.showGridlines = false;
      chart_.addColorAxis("arr_flights","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      var s2 = chart_.addSeries(null,dimple.plot.scatter);
      

      x.title = "";
      y.title = "";
      //chart_.setMargins("10px", "30px", "110px", "70px");
      y.overrideMax = 4500000;
      chart_.draw();
      
    }




function draw_securityDelay(data){
      var id_chart = '#chart_security_delay';
      var svg = dimple.newSvg(id_chart,"100%",400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);

      });

      data.forEach(function(d){
        d['security_delay'] = +d['security_delay'];
      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","security_delay");
      y.showGridlines = false;

      chart_.addColorAxis("security_delay","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      var s2 = chart_.addSeries(null,dimple.plot.scatter);
      

      x.title = "";
      y.title = "";
      y.overrideMax = 4500000;
      chart_.draw();
    
    }  

function draw_aircraftDelay(data){
      var id_chart = '#chart_late_aircraft_delay';
      var svg = dimple.newSvg(id_chart,"100%",400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);

      });

      data.forEach(function(d){
        d['late_aircraft_delay'] = +d['late_aircraft_delay'];
      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","late_aircraft_delay");
      y.showGridlines = false;

      chart_.addColorAxis("late_aircraft_delay","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      var s2 = chart_.addSeries(null,dimple.plot.scatter);
      
      x.title = "";
      y.title = "";
      y.overrideMax = 4500000;
      chart_.draw();
      
    }  

    
function draw_carrierDelay(data){
      var id_chart = '#chart_carrier_delay';
      var svg = dimple.newSvg(id_chart,"100%",400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);

      });

      data.forEach(function(d){
        d['carrier_delay'] = +d['carrier_delay'];
      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","carrier_delay");
      y.showGridlines = false;

      chart_.addColorAxis("carrier_delay","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      var s2 = chart_.addSeries(null,dimple.plot.scatter);
      
      x.title = "";
      y.title = "";
      y.overrideMax = 4500000;
      chart_.draw();
      
    } 

function draw_cancelledFlight(data){
      var id_chart = '#chart_arr_cancelled';
      var svg = dimple.newSvg(id_chart,"100%",400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);

      });

      data.forEach(function(d){
        d['arr_cancelled'] = +d['arr_cancelled'];
      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","arr_cancelled");
      y.showGridlines = false;


      

      chart_.addColorAxis("arr_cancelled","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      var s2 = chart_.addSeries(null,dimple.plot.scatter);
      

      x.title = "";
      y.title = "";
      y.overrideMax = 4500000;
      chart_.draw();
      
}

function draw_cancelledFlight_prop(data){
      var id_chart = '#chart_arr_cancelled';
      var svg = dimple.newSvg(id_chart,"100%",400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);

      });

      data.forEach(function(d){
        d['arr_cancelled_prop_by_month'] = +d['arr_cancelled_prop_by_month'];
      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","arr_cancelled_prop_by_month");
      y.showGridlines = false;


      

      chart_.addColorAxis("arr_cancelled_prop_by_month","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      var s2 = chart_.addSeries(null,dimple.plot.scatter);
      

      x.title = "";
      y.title = "";
      //y.overrideMax = 4500000;
      chart_.draw();
      
}
