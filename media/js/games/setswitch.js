var flag;
var starttime;
var endtime;
var curblock;
var correct;
var curtrial = 0;
var blocknum = 1;
var tup;
var stim;
var response;
var maxtrials;

function trialinstr(){
    if (blocknum == 1) {return "digfirst";}
    else if (blocknum < 3) {return "dig";}
    else if (blocknum < 5) {return "let";}
    else {return "mix";}    
}

function stimtype(){
    if (blocknum < 3) {return [0,1];}
    else if (blocknum < 5) {return [1,0];}
    else {return [1,1];}    
}

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
                    $('#trial'+trialinstr()).show();
        			break;
            //1000ms fixation
			case 0: $('#fixation').show();
			        flag ++;
			        $(document).unbind('keypress');
			        window.setTimeout(update,1000);
			        break;
			//stimulus presented, time starts
        	case 1: tup = curblock.random_stim();
        	        $(document).bind('keypress',handler);
        	        stim = tup[0];
        	        correct = tup[1];
        	        $('#stim').html(stim);
                    $('#stim').show();
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
    data = 'data=' + blocknum + ","+ stim + "," + correct + "," + response + "," + ((correct == response) ? "1" : "0") + "," + timetaken  +'&timestamp=' + ts +'&code=SSW';
    //console.log(data);
    jQuery.post("/study/send-data", data, false);
    if (curtrial == maxtrials) {
        blocknum++;
        curtrial = 0;
        if (blocknum < 9) {curblock = new Block(stimtype()[0],stimtype()[1]);}
        else {
                flag = 4;
        }
        flag --;
    }
    
}




function Block(lett,num){
    this.letters = lett;
    this.numbers = num;

    if (this.letters == 1 && this.numbers == 1) {
        this.stimuli = new Array('2','3','4','5','6','7','8','9','A','D','I','N','U','S','E','R')
    }
    else if (this.letters == 1) {
        this.stimuli = new Array('A','D','I','N','U','S','E','R','A','D','I','N','U','S','E','R')     
    }
    else {
        this.stimuli = new Array('2','3','4','5','6','7','8','9','2','3','4','5','6','7','8','9')
    }
    this.set = new Array(0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1);
    //0 is even, 1 is odd
    //0 is vowel, 1 is consonant

    
    this.random_stim = function(){
        var s = Math.floor(Math.random()*16)
        return [this.stimuli[s],this.set[s]]
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
			                window.location = '/study/ftask/SET';
			            }
			            break;

		}
		
	}

$(document).ready(function(){
    
    //display rules
        blocknum = $("#stim").attr("blocks");
        maxtrials = $("#stim").attr("trials"); 
        
        //console.log(blocknum);
        //console.log(stimtype());
        curblock = new Block(stimtype()[0],stimtype()[1]);
        flag = -2;
        //console.log(blocknum);
        //trialinstr = "digfirst";
        update();
        
});    

 


