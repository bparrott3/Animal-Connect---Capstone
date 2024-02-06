// let login = document.querySelector(".login-form");

document.querySelector("#login-btn").onclick = function() {
    if (this.textContent === "Login") {
        window.location.href = "https://animal-168888.wl.r.appspot.com/login";
    } else {
        window.location.href = "https://animal-168888.wl.r.appspot.com/logout";
    }
};

let navbar = document.querySelector(".header .navbar");

document.querySelector('#menu-btn').onclick = () =>{
    // login.classList.remove('active');
    navbar.classList.toggle('active');
}

window.onscroll = () =>{
    // login.classList.remove('active');
    navbar.classList.remove('active');
}

var swiper = new Swiper(".gallery-slider", {
    grabCursor:true,
    loop:true,
    centeredSlides:true,
    spaceBetween:20,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        0:{
            slidesPerView:1,
        },
        700:{
            slidesPerView:2,
        },
    }
})


function showDetails(detailsId) {
    var detailsModal = document.getElementById(detailsId);
    detailsModal.style.display = "block";
}

function closeDetails(detailsId) {
    var detailsModal = document.getElementById(detailsId);
    detailsModal.style.display = "none";
}
