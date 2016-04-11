var map;
var geocoder;
var meLat;
var meLong;

if (navigator.geolocation)
{
    navigator.geolocation.getCurrentPosition(showProfileLocation);
}
else
{
   alert("Geolocation API not supported.");
}

function showProfileLocation(position)
{
    var latitude = position.coords.latitude
    var longitude = position.coords.longitude;
    var coords = new google.maps.LatLng(latitude, longitude);

    var mapOptions = {
    zoom: 15,
    center: coords,
    mapTypeControl: false,
    mapTypeId: google.maps.MapTypeId.ROADMAP
};

//create the map, and place it in the HTML map div
map = new google.maps.Map(
document.getElementById("mapPlaceholder"), mapOptions
);

//place the initial marker
var marker = new google.maps.Marker({
position: coords,
map: map,
});
}

