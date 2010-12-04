var gridsize = 50;
var div;
var occupied = new Array(36);
var allow;    



    

function update(id){
  
 //poll for position
     set[id].move(gettopleftsquare(id));
     collision_grid();
     //print_grid();
     if (set[id].target && set[id].x == 5){
         console.log("victory");
     }

}

function print_grid() {
     var i;
     for (i = 0; i < 6; i++) {
         console.log(occupied[6*i] + "," + occupied[6*i+1] + "," + occupied[6*i+2] + "," + occupied[6*i+3] + "," + occupied[6*i+4] + "," + occupied[6*i+5]);
    }
}

function gettopleftsquare(id){
    pos = $('#'+id).offset();
    d = div.offset();
    pos.top = (pos.top - d.top - 5)/gridsize + 1;
    pos.left = (pos.left - d.left - 5)/gridsize + 1;
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
            this.color = '#f00'
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
    
    this.tojson = function(){
        if (this.x > 0 && this.x < 7 && this.y > 0 && this.y < 7 ){
        return '{"len": ' + this.length + ', "or": ' + this.orientation + ', "x": ' + this.x + ', "y": ' + this.y + ', "theone": ' + this.target + '},';
        }
        else { return ""}
    }
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
return colors[id%16];
}

$(document).ready(function(){
    
    $('#button').click(function(){
        astring = '{"cars" : [';
       for (var a in set){
          astring += set[a].tojson();
       }
       astring += ']}'
       alert(astring);
    });
    set = {};
    for (var i = 0; i <= 32; i++) {
        if (i==0) {set[i] = new Car(i,2,true, 7,7,true);}
        else if (i<=8) {set[i] = new Car(i,2,true, 7,7,false);}
        else if (i<=16) {set[i] = new Car(i,3,true, 7,7,false);}
        else if (i<=24) {set[i] = new Car(i,2,false, 7,7,false);}
        else {set[i] = new Car(i,3,false, 7,7,false);}
    }
    for (var carr in set) {
        set[carr].init();
    }
    div = $('#grid');
    div.css({
        width: gridsize * 6,
        height: gridsize * 6
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
           /*car = set[this.id];
           dd.limit = div.offset();
           dd.limit.top += 5;
           dd.limit.left += 5;
           dd.limit.bottom = dd.limit.top + div.outerHeight() - $( this ).outerHeight() - 10;
           dd.limit.right = dd.limit.left + div.outerWidth() - $( this ).outerWidth() - 10;

           if (car.orientation){ 
               allow.left = dd.limit.left + (car.x - car.freespace().minus - 1) * gridsize;
               allow.right = dd.limit.left + (car.x + car.freespace().plus - 1) * gridsize;
          }
          else {
               allow.top = dd.limit.top + (car.y - car.freespace().minus - 1) * gridsize;
               allow.bottom = dd.limit.top + (car.y + car.freespace().plus - 1) * gridsize;
               //allow.bottom = dd.limit.top + car.freespace().plus * gridsize;
               //console.log(allow.bottom);
               }
*/
        })
        .drag("end", function(ev,dd){
            $(this).css({
                top: Math.round(dd.offsetY/gridsize) * gridsize,
                left: Math.round(dd.offsetX/gridsize) * gridsize 
            });
            update(this.id);
/*  
            if (set[this.id].orientation) {

                $( this ).css({
                   //top: Math.min( dd.limit.bottom, Math.max( dd.limit.top, Math.round(dd.offsetY/gridsize) * gridsize ) ),
                   left: Math.min( allow.right, Math.max( allow.left, Math.round(dd.offsetX/gridsize) * gridsize ) )
                });   
            }
            else {

                $( this ).css({
                   top: Math.min(allow.bottom, Math.max( allow.top, Math.round(dd.offsetY/gridsize) * gridsize ) ),
                   //left: Math.min( dd.limit.right, Math.max( dd.limit.left, Math.round(dd.offsetX/gridsize) * gridsize ) )
                });   
            }
            
*/
        })
        .drag(function( ev, dd ){
            $( this ).css({
               top:  dd.offsetY,
               left: dd.offsetX
            });   

            /*
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
          }*/
        });
});
