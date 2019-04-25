let count;
let newCount;
const debugging = true;
const UPDATE_INTERVAL = 5000;
const container = document.getElementById("activityFeedContainer");
const baseUrl = "http://192.168.50.50:8080";


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
    container.insertBefore(rowContainer, container.firstChild);

    // Get the URI to the user
    let user_uri = baseUrl + user;

    // Get the username
    $.getJSON(user_uri, function (result) {
        // Get the involved user and add it to the html element
        let username = result.username;
        let color = result.personal_color;
        nameContainer.href = baseUrl + "/users/" + username + "/profile_page/";
        nameContainer.innerHTML += username;
        nameContainer.style.cssText = 'color:' + color + " !important";
        nameContainer.classList.add("activityFeedNameStyle");
        if (debugging) {
            console.log(username + "'s personal color is: " + color );
        }

    });
    // Set the timestamp
    datetimeContainer.innerHTML += timestamp;
}


!function buildAndLoop() {

    // Get the 10 latest activities
    $.getJSON(baseUrl + "/api/resources/joined_event_activities/?event_id=" + event_id, function (result) {

        // Create each of them in the activity feed
        $.each(result.objects, function () {
            createNewJoinedEventRow(this.user, this.datetime_earned);
        });

        // Get the count of the activities
        $.getJSON(baseUrl + "/api/resources/joined_event_activities/?event_id=" + event_id + "&attach_dynamic_fields=get_count", function (result) {
            // Get the first number of activities
            count = result.objects[0].attach_dynamic_fields_get_count;

            if (debugging) {
                console.log(count + " - Initial count");
            }

            // Check for new activities every fifth second
            setInterval(function () {

                $.getJSON(baseUrl + "/api/resources/joined_event_activities/?event_id=" + event_id + "&attach_dynamic_fields=get_count", function (result) {
                    newCount = result.objects[0].attach_dynamic_fields_get_count;
                    if (debugging) {
                        console.log(newCount + " - Current count");
                    }
                    // Check for changes
                    if (newCount > count) {

                        for (let i = count; i < newCount; i++) {
                            // Retrieves a specific activity
                            let object = result.objects[i];
                            createNewJoinedEventRow(object.user, object.datetime_earned);
                        }

                        // Set the count to the new value
                        count = newCount;

                        if (debugging) {
                            console.log(count + " - New count");
                        }
                    }
                });

            }, UPDATE_INTERVAL);
        });
    });
}();