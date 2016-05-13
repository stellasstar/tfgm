var data;
var map;
var map_location;
var waypoints;

function initGoogle() {
      data = $.parseJSON(var_json);
      var key = '&key=' + String(data.GOOGLE_KEY);
      var call = '&callback=makeMap';
      var geom = '&libraries=geometry';
      var script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp'
          + key + call + geom;
      document.body.appendChild(script);
      
      if (data.map.includes('canvas')) {
        waypoints = $.parseJSON(var_waypoints);
      }
}

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
        shadow:'https://chart.googleapis.com/chart?chst=d_map_pin_shadow',
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
    var newMap = map;
    var bounds = new google.maps.LatLngBounds();
    if (map_location.includes('canvas')) {
        //alert("This is the makeMarkers.");
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
            var pin_options ='d_map_pin_letter&chld='+(i + 1)+'|FFFFFF|000000'
            var pin = 'https://chart.googleapis.com/chart?chst=' + pin_options;
            var waypoint = new google.maps.Marker({
                position: pos,
                title: contentString,
                map: newMap,
                icon: pin,
                shadow:'https://chart.googleapis.com/chart?chst=d_map_pin_shadow'
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

    if (map_location.includes('canvas')) {
        //alert("This is the printTransport.");
        var end = waypoints.features.length;
        if (end > 0) {
            $(".wp_header").html("...Transport Links...(in metres)\n");
        } else {
            $(".wp_header").html("Finding Transport Links... \n");
        }
        var ways= $('.wpitems');
        for (var i = 0; i < end; i++) {
            var usr_lat = data.latitude;
            var usr_lng = data.longitude;
            var lat = waypoints.features[i].geometry.coordinates[0][1];
            var lng = waypoints.features[i].geometry.coordinates[0][0];
            var name = waypoints.features[i].properties.name;
            var id = waypoints.features[i].id;
            var comments = waypoints.features[i].properties.comments;
            var usr_pos = new google.maps.LatLng(usr_lat, usr_lng);
            var pos = new google.maps.LatLng(lat, lng);
            var distance = google.maps.geometry.spherical.computeDistanceBetween(pos, usr_pos); 
            //alert(id);
            var content = $("<div>");
            content.addClass("expandContent");
            var a = $('<a href="#">');
            a.addClass("glyphicon glyphicon-triangle-right");
            content.append(a);
            content.append((i+1) + "&nbsp;&nbsp;");
            content.append(name + "&nbsp;&nbsp;");
            content.append(distance.toFixed(1) +"&nbsp;m&nbsp;&nbsp;");
            //alert($(content).html());
            
            var show = $("<div>");
            show.addClass('showMe');
            show.append("latitude: &nbsp;&nbsp;" + lat.toFixed(6) + "\n");
            show.append("longitude: &nbsp;&nbsp;" +lng.toFixed(6) + "\n");
            var b = $('<a>');
            b.attr("href", "?pk=" + id + "&location=" + (i+1))
            b.append("Comments: &nbsp;&nbsp;" + comments.length);
            show.append(b);

            ways.append(content);
            ways.append(show);
        }
        // jquery to create peek a boo code, where showMe hides when not needed
        $('.expandContent').click(function() {
            $(this).next('.showMe').slideToggle('slow');
        });
    }
}



function googleMapsLoaded() {
  printTransport();
  makeMap();
  makeMarkers();
}

$(document).ready(initGoogle);
$(document).ready(searchAddress);

window.onload = googleMapsLoaded;

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