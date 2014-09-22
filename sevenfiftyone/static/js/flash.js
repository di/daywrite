$(document).ready(function(){

  $('.admin_flashes').delay(500).fadeOut(1000, 'swing');
  $('.admin_flashes').on('click', function(){
    $(this).stop().slideUp(100);
  })
})