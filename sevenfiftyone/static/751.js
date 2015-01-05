$(function(){
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
            if (data.logged_out) {
            }
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
  }).triggerHandler("save");
});

$(function(){

    // Turn on tooltips
    $("[rel='tooltip']").tooltip();

    // Initialize headroom
    $("header").headroom({
        tolerance: {
          down : 10,
          up : 20
        },
        offset : 205
    });

    // Set the idleTimer to log out after 5 minutes
    $.idleTimer(300000);
    $( document ).on( "idle.idleTimer", function(event, elem, obj){
        window.location.href = "/logout/";
    });
});

// Set trigger for autosave on page unload
window.onbeforeunload = function(e) {
    $("form").trigger("save");
    return null;
};
