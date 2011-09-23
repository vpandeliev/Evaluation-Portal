$(document).ready(function() {
    num = $('#stages_nav').attr('num');
	width = $('#login_menu').width() + 96;
	//console.log(width);
	//console.log(Math.round(width/num));
    
    $('.stage').css('width', ((1/num * width - num*2 - 8) - 200) + 'px');
    
    $('.tablink', this).bind('click', function(){
        currtab = $(this);
        $('.tablink').removeClass('on');
        currtab.addClass('on');
        $('.tab').hide();
        $('#' + currtab.attr('id') + 'box').show();
    
    });
    
    
});
