var map;
var geocoder;
var position;

if (navigator.geolocation)
{
    navigator.geolocation.getCurrentPosition();
}
else
{
   alert("Geolocation API not supported.");
}

function showProfileLocation()
{
    var latitude = {{form.instance.latitude}}
    var longitude = {{form.instance.longitude}}
    var coords = new google.maps.LatLng(latitude, longitude);

    var mapOptions = {
    zoom: 15,
    center: coords,
    mapTypeControl: false,
    mapTypeId: google.maps.MapTypeId.ROADMAP
};

//create the map, and place it in the HTML map div
map = new google.maps.Map(
document.getElementById("defaultPositionMap"), mapOptions
);

//place the initial marker
var marker = new google.maps.Marker({
position: coords,
map: map,
});
}