// Collapsible functionality
function handleCollapsible(collapsible) {
    collapsible.classList.toggle("active");
    var content = collapsible.nextElementSibling;
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Check if there's a hash fragment in the URL
    var hash = window.location.hash;
    if (hash) {
        var targetCollapsible = document.querySelector(hash + ' .collapsible');
        if (targetCollapsible) {
            handleCollapsible(targetCollapsible);
        }
    }
});

// Collapsible event listeners
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}