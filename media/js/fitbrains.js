
$(document).ready(function(){
    $('#timerdone').hide();
    $('.timer').hide().delay(3000).fadeIn(1000);
    counter.i = parseInt($('#timer').attr('count'));
    //counter.i = 300;
    counter.whendone = function(){
        $('#timer').html("<h2>Time's up!</h2>");
        //$('#warn').fadeOut(1000);
        $('#timerdone').delay(1000).fadeIn(1000);
        
    }
    counter.start();
});
