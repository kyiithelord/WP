

odoo.define('final_assign.get_location', function (require) {
    'use strict';

    var rpc = require('web.rpc');
    var core = require('web.core');
    var _t = core._t;

    function getLocationByGeolocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
        
                console.log('Latitude:', lat);
                console.log('Longitude:', lon);
        
                // Make RPC call to Odoo
                rpc.query({
                    model: 'sale.order',
                    method: 'action_check_in',
                    args: [],  // Pass method args if needed
                    kwargs: { 
                        context: { 
                            current_latitude: lat, 
                            current_longitude: lon 
                        } 
                    },
                }).then(function(response) {
                    console.log("Check-in successful:", response.message);
                }).catch(function(error) {
                    console.error("Error during check-in:", error);
                });
            });
        } else {
            console.log("Geolocation not supported.");
        }
        
    }

    return {
        getLocationByGeolocation: getLocationByGeolocation,
    };
});








// odoo.define('final_assign.get_location', function (require) {
//     'use strict';

//     var rpc = require('web.rpc');
//     var core = require('web.core');
//     var _t = core._t;

//     async function getLocationAndPerformAction(saleOrderId) {
//     if (navigator.geolocation) {
//         try {
//             const position = await new Promise((resolve, reject) => {
//                 navigator.geolocation.getCurrentPosition(resolve, reject);
//             });

//             const lat = position.coords.latitude;
//             const lon = position.coords.longitude;

//             console.log('Latitude:', lat);
//             console.log('Longitude:', lon);

//             // Now you want to call the backend with the lat, lon, and Sale Order ID
//             const response = await rpc.query({
//                 model: 'sale.order',          // The model where you want to perform the action
//                 method: 'action_check_in',    // The method you're calling on that model
//                 args: [lat, lon],             // Arguments (latitude and longitude) you're passing to the method
//                 kwargs: { context: { active_id: saleOrderId } },  // Passing the Sale Order ID
//             });

//             console.log('Check-in completed:', response.message);
//             alert(response.message);  // Display success message to the user

//         } catch (error) {
//             console.error('Geolocation error:', error);
//             alert('Unable to retrieve your location.');
//         }
//     } else {
//         alert("Geolocation is not supported by this browser.");
//     }
// }
