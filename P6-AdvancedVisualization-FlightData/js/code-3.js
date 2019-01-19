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
        d['weather_delay_prop_by_month'] = +d['weather_delay_prop_by_month'];
      });
      
      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","month")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("month");


      var y = chart_.addMeasureAxis("y","weather_delay_prop_by_month");
      y.showGridlines = false;
      chart_.addColorAxis("weather_delay_prop_by_month","black");
      chart_.addSeries(null,dimple.plot.line);
      chart_.colors = 'black';
      
      x.title = "";
      y.title = "";
      y.overrideMax = 0.5;
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
        d['arr_flights_prop_by_month'] = +d['arr_flights_prop_by_month'];
      });


      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","arr_flights_prop_by_month");
      y.showGridlines = false;
      chart_.addColorAxis("arr_flights_prop_by_month","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      //var s2 = chart_.addSeries(null,dimple.plot.scatter);
      

      x.title = "";
      y.title = "";
      //chart_.setMargins("10px", "30px", "110px", "70px");
      y.overrideMax = 0.5;
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
        d['security_delay_prop_by_month'] = +d['security_delay_prop_by_month'];
      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","security_delay_prop_by_month");
      y.showGridlines = false;

      chart_.addColorAxis("security_delay_prop_by_month","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      //var s2 = chart_.addSeries(null,dimple.plot.scatter);
      

      x.title = "";
      y.title = "";
      y.overrideMax = 0.5;
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
        d['late_aircraft_delay_prop_by_month'] = +d['late_aircraft_delay_prop_by_month'];
      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","late_aircraft_delay_prop_by_month");
      y.showGridlines = false;

      chart_.addColorAxis("late_aircraft_delay_prop_by_month","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      //var s2 = chart_.addSeries(null,dimple.plot.scatter);
      
      x.title = "";
      y.title = "";
      y.overrideMax = 0.5;
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
        d['carrier_delay_prop_by_month'] = +d['carrier_delay_prop_by_month'];
      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","carrier_delay_prop_by_month");
      y.showGridlines = false;

      chart_.addColorAxis("carrier_delay_prop_by_month","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      //var s2 = chart_.addSeries(null,dimple.plot.scatter);
      
      x.title = "";
      y.title = "";
      y.overrideMax = 0.6;
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
      //var s2 = chart_.addSeries(null,dimple.plot.scatter);
      

      x.title = "";
      y.title = "";
      y.overrideMax = 0.6;
      chart_.draw();
      
}

