var flag;
var starttime;
var endtime;
var curblock;
var correct;
var curtrial = 0;
var blocknum = 1;
var tup;
var forestim;
var backstim;
var response;
var maxtrials;
var trialinstr = "";


function update()
	{
	    $('.hidable').hide();
	  
		switch(flag)
		{
		    //before anything's started
			case -2:
				    $('#instr').show();	
					break;	
            case -1:
                    $('#trial'+first).show();
                    first = "";
        			break;
            //1000ms fixation
			case 0: $('#flankfixation').show();
			        flag ++;
			        $(document).unbind('keypress');
			        window.setTimeout(update,1000);
			        break;
			//stimulus presented, time starts
        	case 1: tup = curblock.random_stim();
        	        $(document).bind('keypress',handler);
        	        forestim = tup[0];
        	        backstim = tup[1];
        	        var path = $('.backimg').attr("src");
        	        //console.log(path.slice(0,-5) + backstim +".png");
        	        $('.backimg').attr("src",path.slice(0,-5) + backstim +".png");
        	        $('.frontimg').attr("src",path.slice(0,-5) + forestim +".png");
                    $('#stimtable').show();
                    starttime = (new Date).getTime();

                    break;
            
            case 2: $('#done').show();
                    break;
            }
		}
	
	
function submit_trial() {
    //console.log("submit");
    curtrial ++;
    //console.log(curtrial);
    ts = (new Date).getTime()/1000.0;
    data = 'data=' + blocknum + ","+ forestim + "," + response + "," + ((forestim == response) ? "1" : "0") + "," + timetaken  +'&timestamp=' + ts +'&code=FLT';
    jQuery.post("/study/send-data", data, false);
    if (curtrial == maxtrials) {
        blocknum++;
        curtrial = 0;
        if (blocknum >= 9) {
                flag = 4;
        }
        flag --;
    }
    
}




function Block(){
    // 0 is left, 1 is right, 2 is square
    this.front = new Array(0,0,0,1,1,1)
    this.back = new Array(0,1,2,0,1,2)
    //0 is even, 1 is odd
    //0 is vowel, 1 is consonant

    
    this.random_stim = function(){
        var s = Math.floor(Math.random()*6)
        return [this.front[s],this.back[s]]
    };
    

}



    
$(document).keypress(handler);

function handler(e)
	{
		switch(e.which)
		{
			// user presses the "z" key
			case 122:	
			case 90:	
			        if (flag == 1) {
			            endtime = (new Date).getTime();
                        timetaken = endtime - starttime;
                        response = 0;
                        submit_trial();
			            flag--;

			            update();
			    }
				break;	

			// user presses the "m" key
			case 109:
			case 77:	    
			        if (flag == 1) {
		                endtime = (new Date).getTime();
                        timetaken = endtime - starttime;
                        response = 1;
                        submit_trial();
    		            flag--;
                        update();
		            
		    }
					break;	
		    

			// user presses the " " key
			case 32:	if (flag == -2 || flag == -1){
			                flag++;
			                update();
			                }
			            else if (flag == 2){
			                window.location = '/study/ftask/FLA';
			            }
			            break;

		}
		
	}


$(document).ready(function(){
    
    //display rules
        curblock = new Block();
        flag = -2;
        first = "first";
        blocknum = $("#stimtable").attr("blocks");
        maxtrials = $("#stimtable").attr("trials"); 
        update();
        
});    

 


