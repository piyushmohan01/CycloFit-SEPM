const menuBtn = document.querySelector('.menu-btn');
const navtext = document.querySelector('.text');
let menuOpen = false;
menuBtn.addEventListener('click', () => {
    if(!menuOpen) {
        navtext.classList.add('is-active');
        menuBtn.classList.add('open');
        menuOpen = true;
    }
    else {
        navtext.classList.remove('is-active');
        menuBtn.classList.remove('open');
        menuOpen=false;
    }
});

$(document).ready(function(){
    $(".menu-btn").click(function(){
        $('.text').toggleClass("is-active");
    //   $('.bg').toggleClass("is-active");
    //   $('#shape-main').toggleClass("is-active");
    //   $('.nav-1').toggleClass("is-active");
    //   $('.menu-icon').toggleClass("is-active");
    //   $('.menu-close').toggleClass("is-active");
      // $('.register-page').toggleClass("is-active");
    });
});