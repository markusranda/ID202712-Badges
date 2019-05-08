let globalBadgeCount;
let globalBadgeNewCount;
let userlist = [];

const attendeeContainer = document.getElementById("attendeeContainer");

function createNewUserRow(username, color, userbadgeCount) {
    // Create all the html elements, and add them to the row container
    let rowContainer = document.createElement("DIV");
    rowContainer.classList.add("container");
    rowContainer.classList.add("full-width");
    rowContainer.classList.add("fadeIn");
    rowContainer.classList.add("row");
    rowContainer.style.cssText = "margin-right: 0 !important";
    rowContainer.style.cssText = "margin-left: 0 !important";

    let nameContainer = document.createElement("a");
    nameContainer.classList.add("col");
    nameContainer.style.cssText = 'color:' + color + " !important";
    nameContainer.classList.add("activityFeedNameStyle");
    nameContainer.href = baseUrl + "/users/" + username + "/profile_page/";
    nameContainer.innerHTML += username;

    let userbadgeCountContainer = document.createElement("p");
    userbadgeCountContainer.classList.add("col");
    userbadgeCountContainer.classList.add("text-white");
    userbadgeCountContainer.innerHTML += userbadgeCount;

    rowContainer.appendChild(nameContainer);
    rowContainer.appendChild(userbadgeCountContainer);
    attendeeContainer.appendChild(rowContainer);
}

function sortKillBuild() {

    // Sort
    userlist.sort((a, b) => parseFloat(b.userbadgeCount) - parseFloat(a.userbadgeCount));


    // Kill
    while (attendeeContainer.hasChildNodes()) {
        attendeeContainer.removeChild(attendeeContainer.lastChild);
    }

    // Build
    Object(userlist).forEach(function (object) {
        let username = object.username;
        let color = object.color;
        let userbadgeCount = object.userbadgeCount;

        createNewUserRow(username, color, userbadgeCount);
    });
}

function setupUserList() {

    // Get all attending users
    let jqxhr = $.getJSON(baseUrl + "/api/resources/attendee_list/?event_id=" + event_id, function (result) {


        // Create each of them in the user list
        $.each(result.objects, function () {

            // Get the URI to the user
            let url = baseUrl + this.user;

            // Get the username and personal color
            $.getJSON(url + "?event_id=" + event_id + "&get_badgecount=1", function (user) {
                let user_id = user.id;
                let username = user.username;
                let color = user.color_value;
                let userbadgeCount = user.user_badgecount;

                // Place each user in the list
                let object = {id: user_id, username: username, userbadgeCount: userbadgeCount, color: color};
                userlist.push(object);
                sortKillBuild();
            });
        });
    });
}


function updateUserList() {

    sortKillBuild();

    // Get the initial count of the badges achieved in this event
    $.getJSON(baseUrl + "/api/resources/attendee_list/?event_id=" + event_id +
        "&attach_dynamic_fields=get_total_badgecount", function (result) {
        // Get the first number of badges
        globalBadgeCount = result.objects[0].attach_dynamic_fields_get_count;

        // Check for new badges every fifth second
        setInterval(function () {

            $.getJSON(baseUrl + "/api/resources/attendee_list/?event_id=" + event_id +
                "&attach_dynamic_fields=get_total_badgecount", function (result) {
                globalBadgeNewCount = result.objects[0].attach_dynamic_fields_get_count;
                // Check for changes
                if (globalBadgeNewCount > globalBadgeCount) {

                    // A change has occurred
                    // Update every users userbadgeCounter
                    $.when(
                        $.each(userlist, function () {
                            user_id = this.id;
                            $.getJSON(baseUrl + "/api/resources/user/" + user_id + "?user_id=" + user_id +
                                "&event_id=" + event_id + "&get_badgecount=True", function (user) {
                                list = list.update(
                                    list.findIndex(function (item) {
                                        return item.get("id") === user.user_id;
                                    }), function (item) {
                                        return item.set("userbadgeCount", user.userbadgeCount);
                                    }
                                );
                            });
                        })
                    ).then(function () {

                        sortKillBuild();

                        // Set the count to the new value
                        globalBadgeCount = globalBadgeNewCount;
                    });
                }
            });
        }, UPDATE_INTERVAL);
    });
}

!function main() {

    setupUserList();
    //setupUserList().then(updateUserList());

}();