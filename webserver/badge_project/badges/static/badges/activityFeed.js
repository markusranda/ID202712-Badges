function checkForUpdate() {

    function getCount() {
        $.getJSON("http://192.168.50.50:8080/api/resources/joined_event_activities_count/", function (result) {
            return result;
        }

        let oldCount = getCount();

        while (true) {


        }

    }
}


!function () {
    const container = document.getElementById("activityFeedContainer");
    const baseUrl = "http://192.168.50.50:8080";

    $.getJSON("http://192.168.50.50:8080/api/resources/joined_event_activities/", function (result) {

        let username = "";
        let timestamp = "";

        $.each(result.objects, function () {
            // Create all the html elements, and add them to the row container
            let rowContainer = document.createElement("DIV");
            rowContainer.classList.add("row");
            rowContainer.classList.add("full-width");

            let nameContainer = document.createElement("a");
            nameContainer.classList.add("col-md-1");
            nameContainer.classList.add("text-white");

            let activityTextContainer = document.createElement("p");
            activityTextContainer.classList.add("col-md-8");
            activityTextContainer.classList.add("text-white");
            activityTextContainer.innerHTML += 'Just joined the event!';

            let datetimeContainer = document.createElement("p");
            datetimeContainer.classList.add("col-md-1");
            datetimeContainer.classList.add("text-warning");

            rowContainer.appendChild(nameContainer);
            rowContainer.appendChild(activityTextContainer);
            rowContainer.appendChild(datetimeContainer);
            container.appendChild(rowContainer);

            // Get the URI to the user
            let user_uri = baseUrl + this.user;

            // Get the username
            $.getJSON(user_uri, function (result) {
                // Get the involved user and add it to the html element
                username = result.username;
                const url = baseUrl + "/users/" + username + "/profile_page/";
                nameContainer.href = url;
                nameContainer.innerHTML += username;
            });
            // Get the timestamp
            timestamp = this.datetime_earned;
            datetimeContainer.innerHTML += timestamp;
        });
    });

    checkForUpdate();
}();
