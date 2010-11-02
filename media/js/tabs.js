$(document).ready(function() {
    
    num = $('#stages_nav').attr('num');
    console.log(100/num+"%");
    $('.stage').css('width', 100/num + '%')    
    $('.tablink', this).bind('click', function(){
    
        currtab = $(this);
        $('.tablink').removeClass('on');
        currtab.addClass('on');
        $('.tab').hide();
        $('#' + currtab.attr('id') + 'box').show();
    
    });
    
    
});