/*function Timer (delay, down, elmt, endfunc) {
    this.delay = delay;
    this.countdown = down;
    this.domelement = elmt;
    this.stop = false;
    this.whenfinished = endfunc;
    if (this.countdown) {this.i = this.delay} else {this.i = 0}
    
    this.startTimer = function() {
        if (this.countdown) {
            //count down
            
        }
        else {
            //count up
        }
    };
}

$(document).ready(function() {
changethis = $('#timer');
t = new Timer(300,true,changethis);
t.startTimer();

});
*/
var counter = {
    i: 60,
    whendone: null,
    period: 60000, // in milliseconds
    timer: null,
    start: function() {
        if (counter.i > 0){
        counter.i -= 1;
//        $('#timer').html("<h2>"+(Math.floor(counter.i/60)) +":"+(String("0" + counter.i%60).slice(-2))+" minutes</h2>");
        $('#timer').html("<h2>Time left to play: "+(counter.i+1)+ ((counter.i == 0) ? " minute" : " minutes") + "</h2>");

        counter.timer = setTimeout(counter.start, counter.period);}
        else {
            counter.stop();
            counter.whendone();
        }
    },
    stop: function() {
        if (counter.timer) {
            clearTimeout(counter.timer);
            counter.timer = null;
        }
    }
};
/*$(document).ready(function(){
    $('#timerdone').hide();
    $('.timer').hide().delay(3000).fadeIn(1000);
    counter.i = parseInt($('#timer').attr('count'));
    //counter.i = 300;
    counter.whendone = function(){
        $('#timer').html("<h2>Time's up!</h2>");
        //$('#warn').fadeOut(1000);
        $('#timerdone').delay(1000).fadeIn(1000);
        $
    }
    counter.start();
});*/
