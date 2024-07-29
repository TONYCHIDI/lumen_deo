// Navigation appearance function
$(window).scroll(function () {
  if ($(document).scrollTop() > 70) {
    $("nav").addClass("trans");
  } else {
    $("nav").removeClass("trans");
  }
});

// Navigation active page indication function
$(".menu-data").click(function () {
  $(".menu-data").removeClass("active");
  $(this).addClass("active");
});

$(document).ready(function () {
  // Event handler for category links
  $('.category-link').click(function (e) {
    e.preventDefault();
    var category = $(this).data('category');
    
    // Hide all category sections
    $('.category-section').hide();
    // $('.category-section').style.visibility = "hidden";
    
    // Show the selected category section
    $('#' + category).show();
    // category.style.visibility = "visible";
  });
});
