$(function () {
   let form = $("#filterForm");
   let loader = $(".filter-loader");
   let grid = $("#productGrid");
   let count = $("#resultCount");

   function loadHomes() {
      loader.addClass("active");

      $.ajax({
         url: form.data("url"),
         data: {
            category: $("#category").val() || $("#category").data("category"),
            bedrooms: $("#bedrooms").val(),
            bathrooms: $("#bathrooms").val(),
            stories: $("#stories").val(),
            sort: $("#sort").val()
         },
         success: function (response) {
            setTimeout(function () {
               grid.html(response.html);
               count.text(response.count + " Home" + (response.count != 1 ? "s" : ""));
               loader.removeClass("active");
            }, 400);
         },
         error: function () {
            loader.removeClass("active");
         }
      });
   }

   $("#category,#bedrooms,#bathrooms,#stories,#sort").on("change", function () {
      loadHomes();
   });
});



const filter = $("#shopFilter");
const overlay = $(".filter-overlay");

$("#mobileFilterBtn").on("click", function () {
   filter.addClass("active");
   overlay.addClass("active");
});

$("#filterClose,.filter-overlay").on("click", function () {
   filter.removeClass("active");
   overlay.removeClass("active");
});
