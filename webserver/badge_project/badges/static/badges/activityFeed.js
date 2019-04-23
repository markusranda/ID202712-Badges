let count;
const container = document.getElementById("activityFeedContainer");
const baseUrl = "http://192.168.50.50:8080";

function printLatestActivity() {
    let newCount = getCount();

    // Check for changes
    if (newCount > count) {

        // Get how many new activities that exist in the database
        let numActivities = newCount - count;

        // Save the position of the activity in the database
        let pos = count + 1;

        for (let i = 0; i < numActivities; i++) {
            // Retrieves a specific activity
            printActivity(pos);

            pos++;
        }

        console.log("TEST");

        // Set the count to the new value
        count = newCount;
    }

    function printActivity(pos) {
        $.getJSON("http://192.168.50.50:8080/api/resources/joined_event_activities/?id=" + event_id, function (result) {
            let curUser = result.objects.user;
            let curTime = result.objects.timestamp;
            createNewJoinedEventRow(curUser, curTime);
        });
    }

    return undefined;
}


function getCount() {

    $.getJSON("//192.168.50.50:8080/api/resources/joined_event_activities/?id=" + event_id, function (result) {
        return result.meta.total_count;
    });
}


function print10LastActivities() {
    $.getJSON("http://192.168.50.50:8080/api/resources/joined_event_activities/?id=" + event_id, function (result) {

        $.each(result.objects, function () {
            createNewJoinedEventRow(this.user, this.datetime_earned)
        });
    });
}

function createNewJoinedEventRow(user, timestamp) {

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
    let user_uri = baseUrl + user;

    // Get the username
    $.getJSON(user_uri, function (result) {
        // Get the involved user and add it to the html element
        username = result.username;
        const url = baseUrl + "/users/" + username + "/profile_page/";
        nameContainer.href = url;
        nameContainer.innerHTML += username;
    });
    // Set the timestamp
    datetimeContainer.innerHTML += timestamp;
}


!function checkForUpdate() {

    // Get the 10 latest activities for the event
    print10LastActivities();

    // Get the current number of activities for the event
    count = getCount();

    // Creates a new thread that will be fetching new activities

    // Check every second for a new activity
    setInterval(printLatestActivity(), 1000);

}();
