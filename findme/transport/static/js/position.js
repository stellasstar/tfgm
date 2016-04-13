var map;
var geocoder;
var position;

var data = JSON.parse(document.getElementById('json_value').value);
alert(data)

var infowindow = new google.maps.InfoWindow();

function showDefaultProfileLocation()
{
    var latitude = {{data.latitude}};
    var longitude = {{data.longitude}};
    var coords = new google.maps.LatLng(latitude, longitude);

    var mapOptions = {
    zoom: 15,
    center: coords,
    mapTypeControl: false,
    mapTypeId: google.maps.MapTypeId.ROADMAP
};  // end mapOptions

//create the map, and place it in the HTML map div
map = new google.maps.Map(
document.getElementById("defaultPositionMap"), mapOptions
); 

//place the initial marker
var marker = new google.maps.Marker({
position: coords,
map: map,
}); // end marker

} // end function



