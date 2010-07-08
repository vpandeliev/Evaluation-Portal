var current_box = null;
var curent_stage = null;


function bindBoxes(){
  current_box = $('.active');
  current_stage = $("#stage_1");
  //$(current_box).toggleClass('active','not_active');
  $('#stages_nav li a').each(function(index){
    $(this).click(function(){
      $(current_box).removeClass('active').addClass('not_active');//toggleClass('active','not_active');
      current_box = $(this).parent();
      $(current_stage).toggle();
      current_stage = $('#stage_' + $(this).attr('id').split('_').pop());
      $(current_stage).toggle();
      $(current_box).toggleClass('active','not_active');
      return false;
    })
  });
}

function init(){
  bindBoxes();
}



$(document).ready(init);
