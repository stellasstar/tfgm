var data;
var map;
var map_location;
var waypoints;

$(document).ready(function() {
      data = $.parseJSON(var_json);
      var key = '&key=' + String(data.GOOGLE_KEY);
      var call = '&callback=makeMap';
      var script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp'
          + key + call;
      document.body.appendChild(script);
    }
);

function searchAddress() {
    //alert("This is the searchAddress.");
    var defaultText = data.address;
    var searchBox = document.getElementById("search_address");
 
    //default text after load
    searchBox.value = defaultText;
 
    //on focus behaviour
    searchBox.onfocus = function() {
        if (this.value == defaultText) {//clear text field
            this.value = '';
        }
    }
 
    //on blur behaviour
    searchBox.onblur = function() {
        if (this.value == "") {//restore default text
            this.value = defaultText;
        }
    }
}

function makeMap() {
    //alert("This is the makeMap.");

    var latitude = data.latitude;
    var longitude = data.longitude;
    map_location = data.map;

    var coords = new google.maps.LatLng(latitude, longitude);
    //alert(coords);
    var bounds = new google.maps.LatLngBounds();
    //alert(data.map);

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
       data.name  + '\n' +
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
        title: data.name,
        animation: google.maps.Animation.DROP,
        label: data.name[0].toUpperCase()
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
        alert("This is the makeMarkers.");
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
            
            // create the marker
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

function printTransport() {
    //alert("this is printWaypoints")
    var str = String(map_location);
    if (str.includes('canvas')) {
    
        waypoints = $.parseJSON(var_waypoints);
        var end = waypoints.features.length;
        var links;
        
        if (parseInt(end) > 0) {
            $("#wpitems").html("...Transport Links...\n");
        } else {
            $("#wpitems").html("Finding Transport Links... \n");
        }
        for (var i = 0; i < end; i++) {
            var lat = waypoints.features[i].geometry.coordinates[0][1];
            var lng = waypoints.features[i].geometry.coordinates[0][0];
            var name = waypoints.features[i].properties.name;
            var pos = new google.maps.LatLng(lat, lng);
            $('#wpitems').append("<br>");
            $('#wpitems').append(i + 1 + " ");
            $('#wpitems').append(name + " ");
            $('#wpitems').append(parseFloat(Math.round(lat * 100) / 100).toFixed(4));
            $('#wpitems').append(" ");
            $('#wpitems').append(parseFloat(Math.round(lng * 100) / 100).toFixed(4));
        }
    }
}

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

addLoadEvent(searchAddress);
addLoadEvent(printTransport);
addLoadEvent(makeMap);
addLoadEvent(makeMarkers);

// user_id = data.user_id
// name = data.name 
    // the name of the initial user coordinates is set to the username
// address = data.address
// id = data.id
// latitude = data.latitude
// longitude = data.longitude
// srid = data.srid
// map = data.map
// GOOGLE_KEY = data.GOOGLE_KEY
// address = data.address