window.fbAsyncInit = function() {
    FB.init({
        appId: '1132469394552936',
        autoLogAppEvents: true,
        xfbml: true,
        version: 'v13.0'
    });
    FB.AppEvents.logPageView();
};

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
                // Update HTML elements with user data
                document.getElementById('userID').textContent = userID;
                document.getElementById('userName').textContent = userName;
                document.getElementById('userEmail').textContent = userEmail;

                // Pass the access token to fetchInstagramUserData
                fetchInstagramUserData(accessToken);
            } else {
                console.log("Error fetching user data:", response.error);
            }
        }
    );
}

function fetchInstagramUserData(accessToken) {
    // Define the URL for the API endpoint with the necessary parameters
    const apiUrl = `https://graph.facebook.com/17841405822304914/insights?metric=impressions,reach,profile_views&period=day&access_token=${accessToken}`;

    // Make the GET request using fetch
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Insights Data:", data);
            // Process the data as needed
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
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

// Initialize the Facebook SDK and check login state once loaded
window.onload = function() {
    checkLoginState();
};
