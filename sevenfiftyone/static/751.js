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
            alert("saved!");
          }
        }
      }
    }
  });
});

jQuery(function($) {
  $('textarea').autosize();
});
