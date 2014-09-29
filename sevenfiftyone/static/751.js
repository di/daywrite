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
            } else {
                // Show the header if it's unpinned
                var unpinned = $("#header").hasClass("headroom--unpinned");
                if (unpinned) {
                    $("#header").toggleClass("headroom--unpinned headroom--pinned")
                }
                if (data.completed) {
                    if(cur.hasClass("fui-new")) {
                        cur.removeAttr('style');
                        cur.toggleClass("fui-new fui-checkbox-checked", 3000);
                    }
                } else {
                    if (cur.hasClass("fui-checkbox-checked")) {
                        cur.removeAttr('style');
                        cur.toggleClass("fui-new fui-checkbox-checked", 3000).promise().done(function(){
                    // TODO: Move this into a better place
                    /*
                    if (unpinned) {
                        $("#header").toggleClass("headroom--unpinned headroom--pinned")
                    }
                    */
});
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

// Enable tooltips, headroom
$(function(){
    $("[rel='tooltip']").tooltip();
    $("header").headroom({
        tolerance: {
          down : 10,
          up : 20
        },
        offset : 205
    });
});

