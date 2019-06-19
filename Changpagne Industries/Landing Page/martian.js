$(document).ready(function() {
    $("#jump").click(function() {
        $('html, body').animate({
            scrollTop: $("#portfolio").offset().top
        }, 1000);
    });
    
      $("button").click(function() {
        var target = $(this).attr("href");
        $(".content")
          .not(target)
          .hide();
        $(target).show("slow");
      });
    
      var cw = $(".project").width();
      $(".project").css({ height: cw + "px" });
    
      $("#first").click();
    });
    