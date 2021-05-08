// $(document).ready(function(){
//     $(".menu-icon").click(function(){
//       $('.bg').toggleClass("is-active");
//       $('#shape-main').toggleClass("is-active"); 
//       $('.nav-1').toggleClass("is-active");
//       $('.menu-icon').toggleClass("is-active");
//       $('.menu-close').toggleClass("is-active");
//       // $('.register-page').toggleClass("is-active");
//     });
// });

const menuBtn = document.querySelector('.menu-btn');
const bg = document.querySelector('.bg');
const shape = document.querySelector('#shape-main')
const nav1 = document.querySelector('.nav-1')
let menuOpen = false;
menuBtn.addEventListener('click', () => {
    if(!menuOpen) {
        bg.classList.add('is-active');
        shape.classList.add('is-active');
        nav1.classList.add('is-active');
        menuBtn.classList.add('open');
        menuOpen = true;
    }
    else {
        bg.classList.remove('is-active');
        shape.classList.remove('is-active');
        nav1.classList.remove('is-active');
        menuBtn.classList.remove('open');
        menuOpen=false;
    }
});