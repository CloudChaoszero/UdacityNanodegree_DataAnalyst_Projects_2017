function draw_weatherDelay(data){
      var svg = dimple.newSvg('#chart_weather_delay',400,400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);

      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","weather_delay");
      chart_.addColorAxis("weather_delay","black");
      chart_.addSeries(null,dimple.plot.line);
      
      chart_.addSeries(null,dimple.plot.scatter);


      chart_.draw();
    }

    function draw_onTimeArrival(data){
      var id_chart = '#chart_arr_flights';
      var svg = dimple.newSvg(id_chart,400,400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);

      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","arr_flights");
      chart_.addColorAxis("arr_flights","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      var s2 = chart_.addSeries(null,dimple.plot.scatter);
      chart_.draw();
      
    }




  function draw_securityDelay(data){
      var id_chart = '#chart_security_delay';
      var svg = dimple.newSvg(id_chart,400,400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);

      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","security_delay");
      chart_.addColorAxis("security_delay","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      var s2 = chart_.addSeries(null,dimple.plot.scatter);
      chart_.draw();
    
    }  

    function draw_aircraftDelay(data){
      var id_chart = '#chart_late_aircraft_delay';
      var svg = dimple.newSvg(id_chart,400,400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);

      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","late_aircraft_delay");
      chart_.addColorAxis("late_aircraft_delay","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      var s2 = chart_.addSeries(null,dimple.plot.scatter);
      chart_.draw();
      
    }  

    
    function draw_carrierDelay(data){
      var id_chart = '#chart_carrier_delay';
      var svg = dimple.newSvg(id_chart,400,400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);

      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","carrier_delay");
      chart_.addColorAxis("carrier_delay","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      var s2 = chart_.addSeries(null,dimple.plot.scatter);
      chart_.draw();
      
    } 

     function draw_cancelledFlight (data){
      var id_chart = '#chart_arr_cancelled';
      var svg = dimple.newSvg(id_chart,400,400);

      // format new 'date' variable
      var format = d3.time.format("%m-%Y");

      // loop through "data" creating Date variable
      data.forEach(function(d){
        d['date'] = d.month + '-' + d.year;
        d['date'] = format.parse(d['date']);

      });

      var chart_ = new dimple.chart(svg,data);
      var x = chart_.addTimeAxis("x","Date")
      x.tickFormat="%Y/%m";
      x.timeField = "date";
      x.addOrderRule("date");

      var y = chart_.addMeasureAxis("y","arr_cancelled");
      chart_.addColorAxis("arr_cancelled","black")
      var s1 =chart_.addSeries(null,dimple.plot.line);
      var s2 = chart_.addSeries(null,dimple.plot.scatter);
      chart_.draw();
      
    } 