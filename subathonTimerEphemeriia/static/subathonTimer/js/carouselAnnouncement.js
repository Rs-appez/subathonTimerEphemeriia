const announcements = document.getElementById("announcements");
const announcementData = JSON.parse(announcements.innerHTML);

const switchTime =
    parseInt(document.getElementById("switchTime").innerHTML) || 300;

let i = 0;

function rotateAnnouncements() {
    if (i >= announcementData.length) {
        i = 0;
    }
    const element = announcementData[i];
    let announcement = document.getElementById("ann_" + element.id);
    if (announcement) {
        showAnnouncement(announcement);
        setTimeout(() => {
            hideAnnouncement(announcement);
            console.log(switchTime);
            setTimeout(() => {
                rotateAnnouncements();
            }, switchTime * 1000);
        }, element.duration * 1000);
    }
    i++;
}

function showAnnouncement(announcement) {
    announcement.classList.remove("hide");
    announcement.classList.add("show");
}
function hideAnnouncement(announcement) {
    announcement.classList.remove("show");
    announcement.classList.add("hide");
}

rotateAnnouncements();
