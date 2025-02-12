let touchStartX = 0;
let touchEndX = 0;

document.getElementById("imageContainer").addEventListener("touchstart", (e) => {
    touchStartX = e.touches[0].clientX;
});

document.getElementById("imageContainer").addEventListener("touchend", (e) => {
    touchEndX = e.changedTouches[0].clientX;
    handleSwipe();
});

function handleSwipe() {
    if (touchStartX - touchEndX > 50) { // Swipe left
        swipeLeft();
    }
}

function swipeLeft() {
    const imageStack = document.getElementById("imageStack");
    imageStack.classList.add("swipe-left");

    // Simulate new images loading
    setTimeout(() => {
        imageStack.innerHTML = `
            <img class="image-layer top" src="https://placehold.co/800x600?text=New+Image+1" alt="Main Image">
            <img class="image-layer middle" src="https://placehold.co/800x600?text=New+Image+2" alt="Stacked Image">
            <img class="image-layer bottom" src="https://placehold.co/800x600?text=New+Image+3" alt="Stacked Image">
        `;

        document.getElementById("imageFilename").innerText = "new-image.jpg";
        imageStack.classList.remove("swipe-left");
    }, 400); // Wait for animation to complete
}
