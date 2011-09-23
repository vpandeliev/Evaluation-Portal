
var session;
var publisher;
var subscribers = {};

// Un-comment either of the following to set automatic logging and exception handling.
// See the exceptionHandler() method below.
// TB.setLogLevel(TB.DEBUG);
TB.addEventListener("exception", exceptionHandler);

if (TB.checkSystemRequirements() != TB.HAS_REQUIREMENTS) {
	alert("You don't have the minimum requirements to run this application."
		  + "Please upgrade to the latest version of Flash.");
} else {
	session = TB.initSession(sessionId);	// Initialize session

	// Add event listeners to the session
	session.addEventListener('sessionConnected', sessionConnectedHandler);
	session.addEventListener('sessionDisconnected', sessionDisconnectedHandler);
	session.addEventListener('connectionCreated', connectionCreatedHandler);
	session.addEventListener('connectionDestroyed', connectionDestroyedHandler);
	session.addEventListener('streamCreated', streamCreatedHandler);
	session.addEventListener('streamDestroyed', streamDestroyedHandler);
}

//--------------------------------------
//  LINK CLICK HANDLERS
//--------------------------------------

/*
If testing the app from the desktop, be sure to check the Flash Player Global Security setting
to allow the page from communicating with SWF content loaded from the web. For more information,
see http://www.tokbox.com/opentok/build/tutorials/helloworld.html#localTest
*/
function connect() {
	session.connect(apiKey, token);
}

function disconnect() {
	session.disconnect();
	hide('disconnectLink');
	hide('publishLink');
	hide('unpublishLink');
}

// Called when user wants to start publishing to the session
function startPublishing() {
	if (!publisher) {
		var parentDiv = document.getElementById("myCamera");
		var publisherDiv = document.createElement('div'); // Create a div for the publisher to replace
		publisherDiv.setAttribute('id', 'opentok_publisher');
		parentDiv.appendChild(publisherDiv);
		publisher = session.publish(publisherDiv.id); // Pass the replacement div id to the publish method
		show('unpublishLink');
		hide('publishLink');
	}
}

function stopPublishing() {
	if (publisher) {
		session.unpublish(publisher);
	}
	publisher = null;

	show('publishLink');
	hide('unpublishLink');
}

//--------------------------------------
//  OPENTOK EVENT HANDLERS
//--------------------------------------

function sessionConnectedHandler(event) {
	// Subscribe to all streams currently in the Session
	for (var i = 0; i < event.streams.length; i++) {
		addStream(event.streams[i]);
	}
	show('disconnectLink');
	show('publishLink');
	hide('connectLink');
	startPublishing();
}

function streamCreatedHandler(event) {
	// Subscribe to the newly created streams
	for (var i = 0; i < event.streams.length; i++) {
		addStream(event.streams[i]);
	}
}

function streamDestroyedHandler(event) {
	// This signals that a stream was destroyed. Any Subscribers will automatically be removed.
	// This default behaviour can be prevented using event.preventDefault()
}

function sessionDisconnectedHandler(event) {
	// This signals that the user was disconnected from the Session. Any subscribers and publishers
	// will automatically be removed. This default behaviour can be prevented using event.preventDefault()
	publisher = null;

	show('connectLink');
	hide('disconnectLink');
	hide('publishLink');
	hide('unpublishLink');
}

function connectionDestroyedHandler(event) {
	// This signals that connections were destroyed
}

function connectionCreatedHandler(event) {
	// This signals new connections have been created.
}

/*
If you un-comment the call to TB.addEventListener("exception", exceptionHandler) above, OpenTok calls the
exceptionHandler() method when exception events occur. You can modify this method to further process exception events.
If you un-comment the call to TB.setLogLevel(), above, OpenTok automatically displays exception event messages.
*/
function exceptionHandler(event) {
	alert("Exception: " + event.code + "::" + event.message);
}

//--------------------------------------
//  HELPER METHODS
//--------------------------------------

function addStream(stream) {
	// Check if this is the stream that I am publishing, and if so do not publish.
	if (stream.connection.connectionId == session.connection.connectionId) {
		return;
	}
	var subscriberDiv = document.createElement('div'); // Create a div for the subscriber to replace
	subscriberDiv.setAttribute('id', stream.streamId); // Give the replacement div the id of the stream as its id.
	document.getElementById("subscribers").appendChild(subscriberDiv);
	subscribers[stream.streamId] = session.subscribe(stream, subscriberDiv.id);
}

function show(id) {
	document.getElementById(id).style.display = 'block';
}

function hide(id) {
	document.getElementById(id).style.display = 'none';
}

