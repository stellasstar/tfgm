// data structure of json
// city = data[0].city
// user_id = data[1].user_id
// name = data[2].name // the name of the coordinates is set to the username
// address = data[3].address
// id = data[4].id
// latitude = data.[5].latitude
// longitude = data[6].longitude
// srid = data[7].srid
// map = data[8].map
// GOOGLE_KEY = data[9].GOOGLE_KEY

$(window).load(

function initialize(){
    var data = $.parseJSON(var_json);
    var waypoints = $.parseJSON(var_waypoints);
    var marker;
    
    //alert(waypoints.features[0].geometry.coordinates[0][1]);
    //alert(waypoints.features[0].properties.name);
    //alert(waypoints.features.length);
    
    var latitude = data[5].latitude;
    var longitude = data[6].longitude;
    var map_location = data[8].map
    var coords = new google.maps.LatLng(latitude, longitude);
    var bounds = new google.maps.LatLngBounds();
    
    var mapOptions = {
        zoom: 14,
        center: coords,
        mapTypeControl: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    
    //create the map, and place it in the HTML map div
    var map = new google.maps.Map(
        document.getElementById(map_location), 
        mapOptions
    ); 
    
    //place the initial marker
    marker = new google.maps.Marker({
        position: coords,
        map: map,
        title : data[2].name,
        animation: google.maps.Animation.DROP,
    }); // end marker
    
    // Display multiple markers on a map
    var infoWindow = new google.maps.InfoWindow();
    
        
    for (var i = 0; i < waypoints.features.length; i++) { 
        var lat = waypoints.features[i].geometry.coordinates[i][1];
        var lng = waypoints.features[i].geometry.coordinates[i][0];
        var name = waypoints.features[i].properties.name;
        var pos = new google.maps.LatLng(lat, lng);
        bounds.extend(pos);
        marker = new google.maps.Marker({
            position: pos,
            title: name,
            label: i,
            map: map
        }); 
        
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(name);
          infowindow.open(map, marker);
        }
      })(marker, i));
    }
} // end function

);

$(document).ready(function() {
      var data = $.parseJSON(var_json); 
      var key = '&key=' + data[9].GOOGLE_KEY;
      var call = '&callback=initialize';
      var script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp' + key + call;
      document.body.appendChild(script);
    }
);








