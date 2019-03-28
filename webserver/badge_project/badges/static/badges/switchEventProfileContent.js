

function switchEventProfileContent() {
    const moderatorContent = document.getElementById("eventProfileModContent");
    const userContent = document.getElementById("eventProfileUserContent");

    if (moderatorContent.style.display === "none") {
        moderatorContent.style.display = "block";
        userContent.style.display = "none"

    } else {
        moderatorContent.style.display = "none";
        userContent.style.display = "block";
    }
}