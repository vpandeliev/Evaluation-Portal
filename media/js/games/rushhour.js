var gridsize = 70;
var div;
var occupied = new Array(36);
var allow;    
var redcar;
var end;
var left_limit;
var top_limit;
var prevx;
var prevy;
var moves;
var level;
var starttime;
var maxmoves;

function submit_score() {
    endtime = (new Date).getTime()/1000.0;
    timetaken = endtime - starttime;
    data = 'data=' + level + "," + moves + "," + timetaken  +'&timestamp=' + endtime +'&code=RSL'
    //console.log(data);
    jQuery.post("/study/send-data", data, false);
     
    
}


function update(id){
  
 //poll for position
     set[id].move(gettopleftsquare(id));
     collision_grid();
     if (set[id].x != prevx || set[id].y != prevy) {
		sc = maxmoves - moves
		str = "<p>Your moves: " + moves + "</p>";
		$('#score').html(str);
         moves++;

         //console.log(moves);
     }
     //print_grid();
/*     if (set[id].target && set[id].x == 7){
         alert("victory");
     }*/
    if (set[redcar].x + set[redcar].freespace().plus == 5){
        getleft = left_limit + 5 + gridsize * 6;
        end = true;
        //$('#button').fadeTo("fast",0.0);
        $('#'+redcar).animate({left: getleft}, 3000);
        
        submit_score();
        $('#button').delay(5000).html('<span class="actbutton green" style="z-index:130;"><a href="/study/rushhour/play"> Next Level </a></span>');
        $('#gridmask').delay(3000).fadeTo("slow",0.8);
        $('#leveldone').delay(3000).fadeTo("slow",1.0);
        //console.log("Victory");
    }

}




function gettopleftsquare(id){
    pos = $('#'+id).offset();
    d = div.offset();
    pos.top = Math.round((pos.top - d.top - 5)/gridsize) + 1;
    pos.left = Math.round((pos.left - d.left - 5)/gridsize) + 1;
    return pos;
}

function collision_grid() {
     var i;
     for (i = 0; i < 36; i++) {
         occupied[i] = false;
    }
    for (var carr in set) {
        his = set[carr];
    
        occupied[6*(his.y - 1) + his.x - 1] = true;
        if (his.orientation) {
            occupied[6*(his.y - 1) + his.x] = true;
            if (his.length == 3){
                occupied[6*(his.y - 1) + his.x + 1] = true;
            }
        }
        else{
            occupied[6*his.y + his.x - 1] = true;
            if (his.length == 3){
                occupied[6*(his.y + 1) + his.x - 1] = true;
            }
        }
    }
}
function Car(id,len, orient, xin, yin, theone){
    this.id = id;
    this.length = len;
    this.target = theone;
    this.orientation = orient;
    this.x = xin;
    this.y = yin;
    
    this.move = function(pos){
        //console.log(pos);
        this.y = pos.top;
        this.x = pos.left;
        
    };
    this.init = function(){
        collision_grid();
        
        if (this.target){
            this.color = '#f00';
            redcar = this.id;
        }
        else {
            this.color = genHex(this.id); 
        }
        div = $('#grid');
        var top = div.offset().top + (this.y - 1)*gridsize + 5;
        var left  = div.offset().left + 5 + (this.x - 1)*gridsize;
        var length = this.length*gridsize - 4;
        var size = gridsize - 4;       
        if (this.orientation) {
            var stylestring = '<div class="car" id="' + this.id + '" style="background-color:' + this.color + '; top:' +  top + 'px; left:' + left + 'px;width:'+ length + 'px;height:'+ size + 'px;"></div>';
            $(stylestring).insertAfter('#grid');}
        else {
            var stylestring = '<div class="car" id="' + this.id + '" style="background-color:' + this.color + '; top:' +  top + 'px; left:' + left + 'px;height:'+ length + 'px;width:'+ size + 'px;"></div>';
            $(stylestring).insertAfter('#grid');}

            
        
        
    };
    
    this.freespace = function(){
        var free = new Object;
        free.plus = 0;
        free.minus = 0;
        if (this.orientation){
            for (var i = this.x - 2; i >= 0; i--) {
                if (occupied[6*(this.y - 1) + i]) {
                    break;
                }
                else {
                free.minus += 1;}
            }
            for (var i = this.x + this.length - 1; i < 6; i++){
                if (occupied[6*(this.y - 1) + i]) {
                    break;
                }
                else{
                free.plus += 1;}
            }
        }
        else {
            for (var i = this.y - 2; i >= 0; i--) {
                if (occupied[6*(i) + this.x - 1]) {
                    break;
                }
                else {
                    free.minus += 1;}
            }
            for (var i = this.y + this.length - 1; i < 6; i++){
                if (occupied[6*i + this.x - 1]) {
                    break;
                }
                else{
                free.plus += 1;}
            }
        }
        return free;
    }
}

function genHex(id){
colors = new Array(16)

colors[0]="blue"
colors[1]="fuchsia"
colors[2]="green"
colors[3]="CornflowerBlue"
colors[4]="maroon"
colors[5]="yellow"
colors[6]="LightPink"
colors[7]="Coral"
colors[8]="PaleGreen"
colors[9]="navy"
colors[10]="olive"
colors[11]="purple"
colors[12]="CornflowerBlue"
colors[13]="Brown"
colors[14]="DarkSalmon"
colors[15]="teal"
return colors[id];
}


    

$(document).ready(function(){
    //$('#button').hide();
    $('#button2').hide();
    //$('$gridmask').hide()
    
    $('#timerdone').hide();
    $('.timer').hide().delay(3000).fadeIn(1000);
    counter.i = parseInt($('#timer').attr('count'));
    //counter.i = 300;
    counter.whendone = function(){
        $('#timer').html("<h2>Time's up!</h2>");
        //$('#warn').fadeOut(1000);
        $('#timerdone').delay(1000).fadeIn(1000);
        //console.log($('#button'));
        $('#button').hide();
    }
    counter.start();
    
    $('#button').click(function(){
        location.reload();
		//window.location.replace("/study/ftask/RSH");
		
    });
    $('#button2').click(function(){
        /*location.reload();*/
		//window.location.replace("/study/ftask/RSH");
		
    });
    starttime = (new Date).getTime()/1000.0;
    set = {};
    setc = {};
    end = false;
    moves = 1;
    div = $('#grid');
    left_limit = div.offset().left + 5;
    top_limit = div.offset().top + 5;
        a = jQuery.parseJSON(div.attr('level'));
        
        level = a['level'];
		maxmoves = div.attr('moves');
        eval('setc = ' + a['content'] + ';');
        //
        //console.log(setc);
        var i = 0;
        for (var a in setc.cars) {
            c = setc.cars[a];
            set[i] = new Car(i, c.len, c.or, c.x, c.y, c.theone);
            i++;   
        }
        
        for (var carr in set) {
               set[carr].init();
           }
            
            div.css({
                width: gridsize * 6,
                height: gridsize * 6
             });
             div2 = $('#target');
             div2.css({
                 width: gridsize * 2 + 5,
                 height: gridsize,
                 top: top_limit - 5 + gridsize * 2,
                 left: left_limit + gridsize * 6
              });
             var i;
             for (i = 0; i < 36; i++) {
                 occupied[i] = false;
            } 
             collision_grid();
             allow = new Object()
             allow.left = 0;
             allow.right = 0;
             allow.top = 0;
             allow.bottom = 0;

            
             $('.car')
                .drag("start",function( ev, dd ){
                    if (!end){
                   car = set[this.id];
                   prevx = car.x
                   prevy = car.y
                   dd.limit = div.offset();
                   dd.limit.top += 5;
                   dd.limit.left += 5;
                   dd.limit.bottom = dd.limit.top + div.outerHeight() - $( this ).outerHeight() - 10;
                   dd.limit.right = dd.limit.left + div.outerWidth() - $( this ).outerWidth() - 10;

                   if (car.orientation){ 
                       allow.left = dd.limit.left + (car.x - car.freespace().minus - 1) * gridsize;
                       //console.log(allow.left);
                       allow.right = dd.limit.left + (car.x + car.freespace().plus - 1) * gridsize;
                       //console.log(allow.right);
                       if (car.target && car.x + car.freespace().plus == 5){
                           allow.right = dd.limit.left + 6 * gridsize + 5;
                       }

                  }
                  else {
                       allow.top = dd.limit.top + (car.y - car.freespace().minus - 1) * gridsize;
                       allow.bottom = dd.limit.top + (car.y + car.freespace().plus - 1) * gridsize;
                       //allow.bottom = dd.limit.top + car.freespace().plus * gridsize;
                       //console.log(allow.bottom);
                       }
                    }
                })
                .drag("end", function(ev,dd){
                    //console.log(dd);
                    if (!end){
                        car = set[this.id]
                    if (car.orientation) {
                        if (car.target && car.x > 6){
                            $( this ).css({
                               //top: Math.min( dd.limit.bottom, Math.max( dd.limit.top, Math.round(dd.offsetY/gridsize) * gridsize ) ),
                               left: allow.right
                            });   
                            
                        }
                        else {
                            //console.log(dd.offsetX);
                            
                        $( this ).css({
                           //top: Math.min( dd.limit.bottom, Math.max( dd.limit.top, Math.round(dd.offsetY/gridsize) * gridsize ) ),
                           left: Math.min( allow.right, Math.max( allow.left, Math.round((dd.offsetX - left_limit)/gridsize) * gridsize + left_limit) )
                        });   
                        }
                    }
                    else {

                        $( this ).css({
                           top: Math.min(allow.bottom, Math.max( allow.top, Math.round((dd.offsetY - top_limit)/gridsize) * gridsize + top_limit)  ),
                           //left: Math.min( dd.limit.right, Math.max( dd.limit.left, Math.round(dd.offsetX/gridsize) * gridsize ) )
                        });   
                    }
                    update(this.id);
                }
                })
                .drag(function( ev, dd ){
                    if (!end){
                   if (set[this.id].orientation) {
                       $( this ).css({
                          //top: Math.min( dd.limit.bottom, Math.max( dd.limit.top, dd.offsetY) ),
                          left: Math.min( allow.right, Math.max( allow.left, dd.offsetX) )
                       });   
                  }  
                  else {
                      $( this ).css({
                          top: Math.min( allow.bottom, Math.max( allow.top, dd.offsetY) ),
                          //left: Math.min( dd.limit.right, Math.max( dd.limit.left, dd.offsetX) )
                       });
                  }}
                });

        
        
        

});    

 


