$(document).ready(function(){
    $(".menu-icon").click(function(){
      $('.bg').toggleClass("is-active");
      $('#shape-main').toggleClass("is-active");
      $('.nav-1').toggleClass("is-active");
      $('.menu-icon').toggleClass("is-active");
      $('.menu-close').toggleClass("is-active");
      // $('.register-page').toggleClass("is-active");
    });
});