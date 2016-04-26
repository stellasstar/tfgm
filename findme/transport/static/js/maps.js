var data;
var map;
var map_location;

$(document).ready(function() {
      data = $.parseJSON(var_json);
      var key = '&key=' + data[9].GOOGLE_KEY;
      var call = '&callback=makeMap';
      var script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp'
          + key + call;
      document.body.appendChild(script);
    }
);

function makeMap() {
    //alert("This is the second.");

    var latitude = data[5].latitude;
    var longitude = data[6].longitude;
    map_location = data[8].map;

    var coords = new google.maps.LatLng(latitude, longitude);
    //alert(coords);
    var bounds = new google.maps.LatLngBounds();
    //alert(data[8].map);

    var mapOptions = {
        zoom: 14,
        center: coords,
        mapTypeControl: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    //create the map, and place it in the HTML map div
    map = new google.maps.Map(
        document.getElementById(map_location),
        mapOptions
    );

    var contentString = '<div>'+
       data[2].name  + '\n' +
       '</div><div>' +
     'latitude : ' + latitude + '\n' +
       '</div><div>' +
      'longitude : ' + longitude + '\n' +
      '</div>';

    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });

    //place the initial marker
    var marker = new google.maps.Marker({
        position: coords,
        map: map,
        title: data[2].name,
        animation: google.maps.Animation.DROP,
        label: data[2].name[0]
    }); // end marker

    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });

}

function makeMarkers() {
    var str = String(map_location);
    var newMap = map;
    var bounds = new google.maps.LatLngBounds();
    if (str.includes('canvas')) {
        //alert("This is the third.");
        var waypoints = $.parseJSON(var_waypoints);
        var end = waypoints.features.length;
        // Display multiple markers on a map
        var infoWindow = new google.maps.InfoWindow();
        for (var i = 0; i < end; i++) {
            var lat = waypoints.features[i].geometry.coordinates[0][1];
            var lng = waypoints.features[i].geometry.coordinates[0][0];
            var name = waypoints.features[i].properties.name;
            var pos = new google.maps.LatLng(lat, lng);
            //alert(pos);
            bounds.extend(pos);
            var contentString = name  + '\n' +
                                String(pos) + '\n';
            var waypoint = new google.maps.Marker({
                position: pos,
                title: contentString,
                label: String(i + 1),
                map: newMap
            });
            google.maps.event.addListener(waypoint, 'mouseover',
            (function(waypoint, i) {
                return function() {
                  infowindow.open(map, waypoint);
                }
            })(waypoint, i));
            // Automatically center the map fitting all markers on the screen
            map.fitBounds(bounds);
        } // end for
    } // end if
} // end makeMarkers

function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      if (oldonload) {
        oldonload();
      }
      func();
    }
  }
}
addLoadEvent(makeMap);
addLoadEvent(makeMarkers);