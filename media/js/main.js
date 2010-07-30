var current_box = null;
var curent_stage = null;
var last_click = 0;


function bindBoxes(){
  current_box = $('.active');
  current_stage = $(".stage_panel:visible");
  //$(current_box).toggleClass('active','not_active');
  $('#stages_nav li a').each(function(index){
    $(this).bind('click',function(){
      if(((new Date).getTime() - last_click) < 200){ return false;}
      last_click = new Date;
      $(current_box).removeClass('active').addClass('not_active');//toggleClass('active','not_active');
      current_box = $(this).parent();
      $(current_stage).toggle();
      current_stage = $('#stage_' + $(this).attr('id').split('_').pop());
      $(current_stage).toggle();
      $(current_box).toggleClass('active','not_active');
      return false;
    });
  });
}

function init(){
  bindBoxes();
}



$(document).ready(init);