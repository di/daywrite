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
            jQuery("#current").animate({"border-color": "#8CC665"}, 1000)
            jQuery("#current").animate({"border-color": "#EEEEEE"}, 3000)
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
        $('html, body').animate({scrollTop: $(document).height()}, 'slow');
    }
};

$(document).ready(function(){
  $('textarea').autosize({
    "callback": scrollToBottom
    });
  $('textarea').caret(-1);
});