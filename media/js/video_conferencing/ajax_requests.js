function invite_user(pk)
{
	$("#ajax_response").load("/video_conferencing/invite_user", "pk="+pk, invite_complete);		
}

function invite_complete(responseText, textStatus, XMLHttpRequest)
{
	window.location.reload()
}

function uninvite_user(pk)
{
	$("#ajax_response").load("/video_conferencing/uninvite_user", "pk="+pk, uninvite_complete);
}

function uninvite_complete(responseText, textStatus, XMLHttpRequest)
{
	window.location.reload()
}


function decline_complete(responseText, textStatus, XMLHttpRequest)
{
	window.location.reload()
}


function decline_video_request(pk)
{
    $("#ajax_response").load("/video_conferencing/decline_video_request", "pk="+pk, decline_complete);
}