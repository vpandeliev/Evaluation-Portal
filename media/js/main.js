/* Messaging */
function button_handler(button, ids){
  $("#" + ids + " p").toggle();
  if($(button).html() == "Open"){
    $(button).empty().append("Close");
  }else{
    $(button).empty().append("Open");
  }
}
function toggleCloseButton(){
  var button = $("#close_message");
  if($(button).attr("class") == "close_fade"){
    $(button).attr({"class":"close_nofade"});
  }else{
    $(button).attr({"class":"close_fade"});
  }
}

function highlight(i,color){
  $(i).css({"background":"yellow"});
  $(i).animate({"backgroundColor":color}, 1400);
}

function messageRead(message_id){
}

function attach_handlers(){
  $("#close_message").click(function(){
      $('#modal_background').toggle();
      $('#inbox').toggle()
  })
  $(".unread li").each(function(){
    var ids = $(this).attr('id');
    var button1 = "#" + ids + " button";
    var self = this;
    $("#" + ids + " button").click(function(){
      $.ajax({
        url: 'studies/mark-read',
        type: 'POST',
        data: {'id':ids},
        success: function(){
          var unread_num = Number($("#unread_count").html());
          unread_num -= 1;
          if(!unread_num){toggleCloseButton()}
          var header = $("#unread_count").html().replace(/\d+/,String(unread_num));
          $("#unread_count").empty().append(header);
          highlight("#inbox h3:first","#eee");
          $("#" + ids + " button").replaceWith($("<button>").append("Close"));
          $(".read").prepend($("<li>").attr('id',ids).append($(self).html()));
          $(self).remove();
          $("#" + ids + " button").click(function(){button_handler(button1, ids)});
          highlight("#" + ids + " h4", "#E4F7FF")
        }
      });
      /*var unread_num = Number($("#unread_count").html());
      unread_num -= 1;
      if(!unread_num){toggleCloseButton()}
      var header = $("#unread_count").html().replace(/\d+/,String(unread_num));
      $("#unread_count").empty().append(header);
      highlight("#inbox h3:first","#eee");
      $("#" + ids + " button").replaceWith($("<button>").append("Close"));
      $(".read").prepend($("<li>").attr('id',ids).append($(self).html()));
      $(self).remove();
      $("#" + ids + " button").click(function(){button_handler(button1, ids)});
      highlight("#" + ids + " h4", "#E4F7FF")*/
    })
  })

  $(".read li").each(function(){
    var ids = $(this).attr('id');
    var button = "#" + ids + " button";
    $(button).click(function(){button_handler(button,ids)
    })
    
  })
}
/*End message */

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

function toggle_detail(id,obj){
  $("#" + id).toggle();
  if ($(obj).attr('class') == 'right'){
    $(obj).toggleClass('right');
    $(obj).toggleClass('down');
  } else {
    $(obj).toggleClass('down');
    $(obj).toggleClass('right');
  }
  return false;
}

function show_modal(text){
  $('#modal_background').toggle();
  $('#modal_body').empty().append(text);
  $('#modal_dialog').show()
  return false;
}

function close_modal(){
  $('#modal_background').toggle();
$('#modal_dialog').toggle()
}

function init(){
  bindBoxes();
  if($('#inbox').length){
    /* make sure this is only executed if inbox has contents. */
    attach_handlers();
  }
}



$(document).ready(init);
