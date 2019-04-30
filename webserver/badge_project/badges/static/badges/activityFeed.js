let badgeCount;
let badgeNewCount;
let joinedCount;
let joinedNewCount;

const debugging = true;
const UPDATE_INTERVAL = 5000;
const container = document.getElementById("activityFeedContainer");
const baseUrl = "http://192.168.50.50:8080";


function createNewEarnedBadgeRow(username, color, timestamp, badgeTitle, badgeDescription, badgeImgUrl) {

    // Create all the html elements, and add them to the row container
    let rowContainer = document.createElement("DIV");
    rowContainer.classList.add("container");
    rowContainer.classList.add("full-width");
    rowContainer.classList.add("fadeIn");
    rowContainer.style.cssText = "margin-right: 0 !important";
    rowContainer.style.cssText = "margin-left: 0 !important";

    let firstRow = document.createElement("DIV");
    firstRow.classList.add("row");
    firstRow.classList.add("full-width");

    let secondRow = document.createElement("DIV");
    secondRow.classList.add("row");
    secondRow.classList.add("full-width");

    let imgBox = document.createElement("DIV");
    imgBox.classList.add("col-md-1");

    let badgeImg = document.createElement("IMG");
    // Due to a bug, i've added slicing to remove the redundant /images
    badgeImg.src = badgeImgUrl.slice(7);
    badgeImg.style.width = "50px";

    let txtBox = document.createElement("DIV");
    txtBox.classList.add("col-md-8");

    let badgeTitleBox = document.createElement("p");
    badgeTitleBox.classList.add("text-white");
    badgeTitleBox.innerHTML += badgeTitle;

    let badgeDescBox = document.createElement("p");
    badgeDescBox.classList.add("text-white");
    badgeDescBox.innerHTML += badgeDescription;

    let nameContainer = document.createElement("a");
    nameContainer.classList.add("col-md-1");
    nameContainer.style.cssText = 'color:' + color + " !important";
    nameContainer.classList.add("activityFeedNameStyle");
    nameContainer.href = baseUrl + "/users/" + username + "/profile_page/";
    nameContainer.innerHTML += username;

    let activityTextContainer = document.createElement("p");
    activityTextContainer.classList.add("col-md-8");
    activityTextContainer.classList.add("text-white");
    activityTextContainer.innerHTML += 'Just won the badge!';

    let datetimeContainer = document.createElement("p");
    datetimeContainer.classList.add("col-md-1");
    datetimeContainer.classList.add("text-warning");
    datetimeContainer.innerHTML += timestamp;

    firstRow.appendChild(nameContainer);
    firstRow.appendChild(activityTextContainer);
    firstRow.appendChild(datetimeContainer);
    rowContainer.appendChild(firstRow);
    imgBox.appendChild(badgeImg);
    txtBox.appendChild(badgeTitleBox);
    txtBox.appendChild(badgeDescBox);
    secondRow.appendChild(imgBox);
    secondRow.appendChild(txtBox);
    rowContainer.appendChild(secondRow);
    container.appendChild(rowContainer);
    container.insertBefore(rowContainer, container.firstChild);
}


function createNewJoinedEventRow(username, color, timestamp) {

    // Create all the html elements, and add them to the row container
    let rowOuterContainer = document.createElement("DIV");
    rowOuterContainer.classList.add("container");
    rowOuterContainer.classList.add("full-width");
    rowOuterContainer.classList.add("fadeIn");
    rowOuterContainer.style.cssText = "margin-right: 0 !important";
    rowOuterContainer.style.cssText = "margin-left: 0 !important";

    let rowInnerContainer = document.createElement("DIV");
    rowInnerContainer.classList.add("row");
    rowInnerContainer.classList.add("full-width");

    let nameContainer = document.createElement("a");
    nameContainer.classList.add("col-md-1");
    nameContainer.style.cssText = 'color:' + color + " !important";
    nameContainer.classList.add("activityFeedNameStyle");
    nameContainer.href = baseUrl + "/users/" + username + "/profile_page/";
    nameContainer.innerHTML += username;

    let activityTextContainer = document.createElement("p");
    activityTextContainer.classList.add("col-md-8");
    activityTextContainer.classList.add("text-white");
    activityTextContainer.innerHTML += 'Just joined the event!';

    let datetimeContainer = document.createElement("p");
    datetimeContainer.classList.add("col");
    datetimeContainer.classList.add("text-warning");
    datetimeContainer.innerHTML += timestamp;

    rowInnerContainer.appendChild(nameContainer);
    rowInnerContainer.appendChild(activityTextContainer);
    rowInnerContainer.appendChild(datetimeContainer);
    rowOuterContainer.appendChild(rowInnerContainer);
    container.appendChild(rowOuterContainer);
    container.insertBefore(rowOuterContainer, container.firstChild);
}


!function buildAndLoop() {

    // Get the 5 latest joined activities
    $.getJSON(baseUrl + "/api/resources/joined_event_activities/?event_id=" + event_id, function (result) {

        // Create each of them in the activity feed
        $.each(result.objects, function () {

            // Get the URI to the user
            let user_uri = baseUrl + this.user;
            let timestamp = this.datetime_earned;

            // Get the username
            $.getJSON(user_uri, function (result) {
                // Get the involved user and add it to the html element
                let username = result.username;
                let color = result.color_value;
                createNewJoinedEventRow(username, color, timestamp);
            });
        });

        // Get the count of the activities
        $.getJSON(baseUrl + "/api/resources/joined_event_activities/?event_id=" + event_id + "&attach_dynamic_fields=get_count", function (result) {
            // Get the first number of activities
            joinedCount = result.objects[0].attach_dynamic_fields_get_count;

            if (debugging) {
                console.log(joinedCount + " - JOINED - Initial count");
            }

            // Check for new activities every fifth second
            setInterval(function () {

                $.getJSON(baseUrl + "/api/resources/joined_event_activities/?event_id=" + event_id + "&attach_dynamic_fields=get_count", function (result) {
                    joinedNewCount = result.objects[0].attach_dynamic_fields_get_count;
                    if (debugging) {
                        console.log(joinedNewCount + " - JOINED - Current count");
                    }
                    // Check for changes
                    if (joinedNewCount > joinedCount) {

                        for (let i = joinedCount; i < joinedNewCount; i++) {
                            // Retrieves a specific activity
                            let object = result.objects[i];
                            createNewJoinedEventRow(object.user, object.datetime_earned);
                        }

                        // Set the count to the new value
                        joinedCount = joinedNewCount;

                        if (debugging) {
                            console.log(count + " - JOINED - New count");
                        }
                    }
                });

            }, UPDATE_INTERVAL);
        });
    });

    // Get the 5 latest earned badges activities
    $.getJSON(baseUrl + "/api/resources/earned_badge_activities/?event_id=" + event_id, function (result) {

        // Create each of them in the activity feed
        $.each(result.objects, function () {

            // Get the URI to the user
            let badge_uri = baseUrl + this.badge;
            let timestamp = this.datetime_earned;
            let user_uri = baseUrl + this.user;

            // Get the username and personal color
            $.getJSON(user_uri, function (result) {
                let username = result.username;
                let color = result.color_value;

                // Get the badge title, description and img
                $.getJSON(badge_uri, function (result) {
                    let badgeTitle = result.name;
                    let badgeDescription = result.description;
                    let image_uri = baseUrl + result.image;

                    // Get the badge image
                    $.getJSON(image_uri, function (result) {
                        let badgeImgUrl = result.url;
                        createNewEarnedBadgeRow(username, color, timestamp, badgeTitle, badgeDescription, badgeImgUrl);
                    });

                });
            });
        });

        // Get the count of the activities
        $.getJSON(baseUrl + "/api/resources/earned_badge_activities/?event_id=" + event_id + "&attach_dynamic_fields=get_count", function (result) {
            // Get the first number of activities
            badgeCount = result.objects[0].attach_dynamic_fields_get_count;

            if (debugging) {
                console.log(badgeCount + " - BADGE - Initial count");
            }

            // Check for new activities every fifth second
            setInterval(function () {

                $.getJSON(baseUrl + "/api/resources/earned_badge_activities/?event_id=" + event_id + "&attach_dynamic_fields=get_count", function (result) {
                    badgeNewCount = result.objects[0].attach_dynamic_fields_get_count;
                    if (debugging) {
                        console.log(badgeNewCount + " - BADGE - Current count");
                    }
                    // Check for changes
                    if (badgeNewCount > badgeCount) {

                        for (let i = badgeCount; i < badgeNewCount; i++) {
                            // Retrieves a specific activity
                            let object = result.objects[i];

                            // Get the URI to the user
                            let badge_uri = baseUrl + object.badge;
                            let timestamp = object.datetime_earned;
                            let user_uri = baseUrl + object.user;

                            // Get the username and personal color
                            $.getJSON(user_uri, function (result) {
                                let username = result.username;
                                let color = result.color_value;

                                // Get the badge title, description and img
                                $.getJSON(badge_uri, function (result) {
                                    let badgeTitle = result.name;
                                    let badgeDescription = result.description;
                                    let image_uri = baseUrl + result.image;

                                    // Get the badge image
                                    $.getJSON(image_uri, function (result) {
                                        let badgeImgUrl = result.url;
                                        createNewEarnedBadgeRow(username, color, timestamp, badgeTitle, badgeDescription, badgeImgUrl);
                                    });
                                });
                            });
                        }


                        // Set the count to the new value
                        badgeCount = badgeNewCount;

                        if (debugging) {
                            console.log(badgeCount + " - BADGE - New count");
                        }
                    }
                });
            }, UPDATE_INTERVAL);
        });
    });
}();