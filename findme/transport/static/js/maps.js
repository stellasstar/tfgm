// data structure of json
// city = data[0].city
// user_id = data[1].user_id
// name = data[2].name // the name of the coordinates is set to the username
// address = data[3].address
// id = data.[4].id
// latitude = data.[5].latitude
// longitude = data[6].longitude
// srid = data[7].srid
// map = data[8].map
// GOOGLE_KEY = data[9].GOOGLE_KEY

$(window).load(function() {
    var data = $.parseJSON(var_json);
    
    var latitude = data[5].latitude;
    var longitude = data[6].longitude;
    var map_location = data[8].map
    
    var contentString = '<div>'+
      data[2].name  + '\n' +
      '</div><div>' +
      'latitude : ' + latitude + '\n' +
       '</div><div>' +
      'longitude : ' + longitude + '\n' +
      '</div>';
    
    var coords = new google.maps.LatLng(latitude, longitude);
    
    
    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });

    var mapOptions = {
        zoom: 15,
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
    var marker = new google.maps.Marker({
        position: coords,
        map: map,
        title : data[2].name,
        animation: google.maps.Animation.DROP,
    }); // end marker
    
    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
    
        
} // end function

);

$(document).ready(function() {
      var data = $.parseJSON(var_json); 
      var key = 'key=' + data[9].GOOGLE_KEY;
      var script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&' + key;
      document.body.appendChild(script);
    }
);








