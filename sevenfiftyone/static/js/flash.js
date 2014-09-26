$(document).ready(function(){
  $('.admin_flashes').delay(1000).fadeOut(1000, 'swing');
  $('.admin_flashes').on('click', function(){
    $(this).stop().fadeOut(100, 'swing');
  })
})
