let loginBtn = document.getElementById('login-btn');
fetch("https://pet-testing-414141.wl.r.appspot.com/jwt", {
        method: 'GET'
    })
    .then(function(res) {
        return res.text();
    })
    .then(function(output) {
        var jwt = output;
        
        if (jwt !== "") {
            loginBtn.textContent = ' Logout';
        }
    })
    .catch(function(error) {
        console.log(error);
    });

    
let login = document.querySelector(".header .login-form");
let navbar = document.querySelector(".header .navbar");

document.querySelector("#login-btn").onclick = function() {

    if (this.textContent.trim() === "Login") {
        login.classList.toggle('active');
        navbar.classList.remove('active');
    } else {
        window.location.href = "https://pet-testing-414141.wl.r.appspot.com/logout";
        loginBtn.textContent = ' Login';
    }
};

document.querySelector("#admin-btn").onclick = function() {
    window.location.href = "https://pet-testing-414141.wl.r.appspot.com/admin-login";
};

document.querySelector("#member-btn").onclick = function() {
    window.location.href = "https://pet-testing-414141.wl.r.appspot.com/member-login";
};





document.querySelector('#menu-btn').onclick = () =>{
    login.classList.remove('active');
    navbar.classList.toggle('active');
};

window.onscroll = () =>{
    login.classList.remove('active');
    navbar.classList.remove('active');
};

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
});


function showDetails(detailsId) {
    var detailsModal = document.getElementById(detailsId);
    detailsModal.style.display = "block";
};

function closeDetails(detailsId) {
    var detailsModal = document.getElementById(detailsId);
    detailsModal.style.display = "none";
};