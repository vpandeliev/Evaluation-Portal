var flag = -1;
var starttime;
var endtime;
var curblock;
var correct;
var curtrial = 0;
var blocksdone;
var tup;
var stim;
var response;

function update()
	{
	    $('.hidable').hide();
		switch(flag)
		{
		    //before anything's started
			case -1:	
			        $('#instr').show();
			        
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
        	case 2: window.location = "/study/assess/done";
		}
	}
	
function submit_trial() {
    //console.log("submit");
    curtrial ++;
    //console.log(curtrial);
   ts = (new Date).getTime()/1000.0;
    data = 'data=' + stim + "," + correct + "," + response + "," + ((correct == response) ? "1" : "0") + "," + timetaken  +'&timestamp=' + ts +'&code=SSW';
    //console.log(data);
    jQuery.post("/study/send-data", data, false);
    if (curtrial == 10) {
        flag = 2;
        update();
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
			case 32:	if (flag == -1){
			                flag = 0;
			                update();
			                }
			            break;

		}
		
	}


$(document).ready(function(){
    
    //display rules
    
        curblock = new Block(1,1);
        update();
});    

 


