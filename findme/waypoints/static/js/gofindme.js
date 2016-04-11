
var lat = null;
var lng = null;
var labels = "";
var labelIndex = labels.length;

function geoFindMe() {
  var output = document.getElementById("map");  

  if (!navigator.geolocation){
    output.innerHTML = "<p>Geolocation is not supported by your browser</p>";
    return;
  }

  function success(position) {
  
    var lat  = position.coords.latitude;
    var lng = position.coords.longitude;
    var myLatLng = {lat, lng};
    
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: myLatLng
    });
    
    var marker = new google.maps.Marker({
        position: myLatLng,
        label: labels[labelIndex++ % labels.length],
        map: map
    });
    
    return myLatLng;
   };

  function error() {
    output.innerHTML = "Unable to retrieve your location";
    
  };

  output.innerHTML = "<p>Locating…</p>";

  navigator.geolocation.getCurrentPosition(success, error);
}

function errorCallback(error) {
  alert('ERROR(' + error.code + '): ' + error.message);
};

function prompt(window, pref, message, callback) {
    let branch = Components.classes["@mozilla.org/preferences-service;1"]
                           .getService(Components.interfaces.nsIPrefBranch);

    if (branch.getPrefType(pref) === branch.PREF_STRING) {
        switch (branch.getCharPref(pref)) {
        case "always":
            return callback(true);
        case "never":
            return callback(false);
        }
    }

    let done = false;

    function remember(value, result) {
        return function() {
            done = true;
            branch.setCharPref(pref, value);
            callback(result);
        }
    }

    let self = window.PopupNotifications.show(
        window.gBrowser.selectedBrowser,
        "geolocation",
        message,
        "geo-notification-icon",
        {
            label: "Share Location",
            accessKey: "S",
            callback: function(notification) {
                done = true;
                callback(true);
            }
        }, [
            {
                label: "Always Share",
                accessKey: "A",
                callback: remember("always", true)
            },
            {
                label: "Never Share",
                accessKey: "N",
                callback: remember("never", false)
            }
        ], {
            eventCallback: function(event) {
                if (event === "dismissed") {
                    if (!done) callback(false);
                    done = true;
                    window.PopupNotifications.remove(self);
                }
            },
            persistWhileVisible: true
        });
}

prompt(window,
       "extensions.foo-addon.allowGeolocation",
       "Foo Add-on wants to know your location.",
       function callback(allowed) { alert(allowed); });