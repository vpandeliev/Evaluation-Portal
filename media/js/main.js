/* Messaging */
/*
button_handler toggles the message open close buttons. It is called
from within attach_handlers.
*/

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

function messageNav(active_tab){
  var divs = [
    "received_messages",
    "sent_messages",
    "compose_messages"
  ]

  for(i=0;i<divs.length;i++){
    $("#" + divs[i]).hide();
    $("#show_" + divs[i]).addClass("not_current_tab")
    if(divs[i] != active_tab){
      $("#show_" + divs[i]).removeClass("current_tab")
      
    }
  }
  
  $("#" + active_tab).show();
  $("#show_" + active_tab).addClass("current_tab")
  return false;
}


/*
sendMessage is responsible for sending a message within the compose
tab of the messages dialog.
*/
function sendMessage(){
  var message = $("#message_form").serialize();

  //check to see if one or participants have been selected.
  if($("input:checked:checked").length == 0){
    return alert("Must select participants.")
  }
  $.ajax({
    url: '/study/alert_send',
    type: "POST",
    data: message,
    success: function(){alert("Message has been sent");clearMessage();}
  })
  return false;
}

/*
clearMessage clears the compose form by emptying the values in the subject
and body fields and unchecking participants.
*/
function clearMessage(){
  $(':input','#message_form')
 .not(':button, :submit, :reset, :hidden')
 .removeAttr('checked')
 .removeAttr('selected');
 $('#message_subject').val('');
 $('#message_body').val('');
}

/*
attach_handlers is a massif function that does way too much... poor design!
However, it's main tasks are attaching click handlers to the different links
and buttons within the messages dialog and it handles some of the modal dialog
actions.
*/
function attach_handlers(){
  /*Message nav first*/
  $("#show_received_messages").click(function(){messageNav("received_messages")});
  $("#show_sent_messages").click(function(){messageNav("sent_messages")});
  $("#show_compose_messages").click(function(){messageNav("compose_messages")});
  $("#send_message").click(function(){sendMessage();return false;});

  $("#close_message").click(function(){
      $('#modal_background').toggle();
      $('#inbox').toggle()
  });

  $(".unread li").each(function(){
    var ids = $(this).attr('id');
    var button1 = "#" + ids + " button";
    var self = this;
    $("#" + ids + " button").click(function(){

      $.ajax({
        url: '/study/mark-read',
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
      })
    })
  });

  $(".read li").each(function(){
    var ids = $(this).attr('id');
    var button = "#" + ids + " button";
    $(button).click(function(){button_handler(button,ids);})
  });

  $(".sent li").each(function(){
    var ids = $(this).attr('id');
    var button = "#" + ids + " button";
    $(button).click(function(){button_handler(button,ids)})
  })

}
/*End message */



function bindBoxes(){
  $("#stages_nav li a").click(function(){
    $("#stages_nav li.active").removeClass("active")
    $(this).closest("li").addClass("active")
    $(".stage_panel").hide();
    $("#" + $(this).attr("id").replace("_box","")).show();
    return false;
  })
  
  $("#inv_stages_nav li a").click(function(){
    curr = $("#inv_stages_nav li.active");
    if (curr.attr("cond")!=$(this).attr("cond")) {
     curr.removeClass("active");   
    }
    
    $(this).closest("li").addClass("active");
    $(".stage_panel").hide();
    $("#" + $(this).attr("id").replace("box_","")).show();
    return false;
  })
}

/*
toggle_detail toggles details for an individual study within it's main page.
*/
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

/* show_modal opens modal dialog and inserts text into it. */
function show_modal(text){
  $('#modal_background').toggle();
  $('#modal_body').empty().append(text);
  $('#modal_dialog').show()
  return false;
}

/* close_modal closes modal dialog */
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
