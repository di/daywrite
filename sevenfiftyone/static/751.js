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
          success: function(data, textStatus, jqXHR) {
            var cur = jQuery("#current");
            if (data.refresh) {
                location.reload(true);
            } else if (data.completed) {
                if(cur.hasClass("fui-new")) {
                    cur.removeAttr('style');
                    cur.toggleClass("fui-new fui-checkbox-checked", 3000);
                }
            } else {
                if (cur.hasClass("fui-checkbox-checked")) {
                    cur.removeAttr('style');
                    cur.toggleClass("fui-new fui-checkbox-checked", 3000);
                } else {
                    $("#current").animate({"color": "#16A085"}, 1000).
                    delay(100).
                    animate({"color": "#BDC3C7"}, 4000, "swing",
                        function() {
                            $("#current").removeAttr('style');
                        }
                    );
                }
            }
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

// Enable tooltips
$(function(){
    $("[rel='tooltip']").tooltip();
});
