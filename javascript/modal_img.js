var modalEle = document.querySelector(".modal");
var modalImage = document.querySelector(".modalImage");
var captionText = document.getElementById("caption");

Array.from(document.querySelectorAll(".ImgThumbnail")).forEach(item => {
    item.addEventListener("click", event => {
        modalEle.style.display = "block";
        modalImage.src = event.target.src;
        captionText.innerHTML = event.target.alt;
    });
});

document.querySelector(".close").addEventListener("click", () => {
    modalEle.style.display = "none";
});