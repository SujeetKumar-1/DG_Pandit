document.addEventListener("DOMContentLoaded", function () {
    const swipeBtn = document.getElementById("swipe-btn");
    const sidebar = document.getElementById("sidebar");
    swipeBtn.addEventListener("click", function () {
        sidebar.classList.toggle("hidden");
    });
});

// document.addEventListener("DOMContentLoaded", function() {
//     const sidebar = document.getElementById("sidebar");
//     const swipeBtn = document.getElementById("swipe-btn");

//     swipeBtn.addEventListener("click", function() {
//         const sidebarWidth = sidebar.offsetWidth;
//         const newWidth = sidebarWidth - 50; // Decrease width by 50px, adjust as needed
//         sidebar.style.width = newWidth + "px";
//     });
// });