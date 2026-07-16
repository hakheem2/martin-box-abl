$(document).ready(function () {
   const $mobileToggle = $("#mobileToggle");
   const $mobileMenu = $("#mobileMenu");
   const $header = $(".header");

   // MOBILE MENU TOGGLE
   $mobileToggle.on("click", function () {
      const isExpanded = $(this).attr("aria-expanded") === "true";

      $(this).toggleClass("active").attr("aria-expanded", !isExpanded);
      $mobileMenu.toggleClass("show").attr("aria-hidden", isExpanded);
      $("body").toggleClass("menu-open");
   });

   // CLOSE MOBILE MENU WHEN LINK IS CLICKED
   $(".mobile-menu a").on("click", function () {
      $mobileMenu.removeClass("show").attr("aria-hidden", true);
      $mobileToggle.removeClass("active").attr("aria-expanded", false);
      $("body").removeClass("menu-open");
   });

   // STICKY HEADER
   $(window).on("scroll", function () {
      $header.toggleClass("scrolled", $(window).scrollTop() > 50);
   });


   // NAV LINK ACTIVE STATE
   $(document).ready(function () {
      let currentPath = window.location.pathname;

      $('.nav-link').each(function () {
         let linkPath = new URL($(this).attr('href'), window.location.origin).pathname;

         if (linkPath === currentPath) {
            $('.nav-link').removeClass('active');
            $(this).addClass('active');
         }
      });
   });



   // FAQ TOGGLE
   $(".faq-question").on("click", function () {

      $(this).next(".faq-answer").slideToggle();

      $(this).find("span").text(
         $(this).find("span").text() === "+" ? "-" : "+"
      );

   });


   // COUNTER ANIMATION
   $(".counter").each(function () {

      let $this = $(this);

      $({ count: 0 }).animate(
         { count: $this.data("count") },
         {
            duration: 2000,
            easing: "swing",
            step: function () {
               $this.text(Math.floor(this.count));
            },
            complete: function () {
               let value = $this.data("count");

               if (value === 100) {
                  $this.text(value + "%");
               } else {
                  $this.text(value + "+");
               }
            }
         }
      );

   });


   /* ==========================================
   PRODUCT GALLERY
========================================== */

   const $heroImage = $("#mainHeroImage");
   const $counter = $(".viewer-counter");

   $(".thumb-btn").on("click", function () {

      $(".thumb-btn").removeClass("active");

      $(this).addClass("active");

      const image = $(this).data("image");
      const index = $(this).data("index");
      const total = $(".thumb-btn").length;

      $heroImage
         .fadeOut(150, function () {

            $(this)
               .attr("src", image)
               .fadeIn(150);

         });

      $counter.text(index + " / " + total);

   });
});

// STICKY HEADER TRANSPARENCY ON SCROLL
$(window).on("scroll", function () {

   if ($(this).scrollTop() > 40) {
      $(".header").addClass("scrolled");
   } else {
      $(".header").removeClass("scrolled");
   }

});
