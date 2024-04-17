// facebookApi.js

window.fbAsyncInit = function() {
    FB.init({
        appId: '1132469394552936',
        autoLogAppEvents: true,
        xfbml: true,
        version: 'v13.0'
    });
};

// Function to initialize the Facebook SDK
function initializeFacebookSDK() {
    // Replace 'YOUR_APP_ID_HERE' with your actual Facebook App ID
    FB.init({
        appId: 'YOUR_APP_ID_HERE',
        cookie: true,
        xfbml: true,
        version: 'v13.0'
    });
}

(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) { return; }
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function fetchUserData(accessToken) {
    // Use the access token in the API request
    FB.api(
        '/me',
        'GET',
        {"fields": "id,name,email", "access_token": accessToken},
        function(response) {
            if (response && !response.error) {
                var userID = response.id;
                var userName = response.name;
                var userEmail = response.email;
                console.log("User ID: " + userID);
                console.log("User Name: " + userName);
                console.log("User Email: " + userEmail);
            } else {
                console.log("Error fetching user data:", response.error);
            }
        }
    );
}


function checkLoginState() {
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            var accessToken = response.authResponse.accessToken;
            // Call fetchUserData with the accessToken
            fetchUserData(accessToken);
        } else {
            // User is not logged in or did not grant permissions
            console.log('User is not logged in.');
        }
    });
}


// Load the Facebook SDK asynchronously
(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// Initialize the Facebook SDK and fetch user data once loaded
window.onload = function() {
    initializeFacebookSDK();
    fetchUserData();
};
