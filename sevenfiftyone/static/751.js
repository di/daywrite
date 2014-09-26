jQuery(function($) {
  $("form").autosave({
    callbacks: {
      scope: "all",
      trigger: {
        method: "interval",
        options: {
            interval: 10000
        }
      },
      condition: "modified",
      save: {
        method: "ajax",
        options: {
          type: "POST",
          success: function() {
            jQuery("#current").animate({"color": "#1abc9c"}, 1000)
            jQuery("#current").animate({"color": "#becac9"}, 3000)
          },
          error: function() {
            alert("error!");
          }
        }
      }
    }
  });
});

var scrollToBottom = function(){
    // Check if the caret is at the end of the textarea
    if ($('textarea').caret() == $('textarea').val().length) {
        // If it is, do the animation
        $('html, body').stop().animate({scrollTop: $(document).height()});
    }
};

$(document).ready(function(){
  $('textarea').autosize({
    "callback": scrollToBottom
    });
  $('textarea').caret(-1);
});
