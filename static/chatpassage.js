URL = window. URL|| window.webkitURL;
var gumStream;
var rec;
var input;

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext 

const recordButton = document.getElementById("recordButton");
const stopButton = document.getElementById("stopButton");
const inputbox = document.getElementById("inputbox");
var pageHeight = $('#chatbot').height();
let message_count = 0

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

console.log("I am here");
inputbox.addEventListener('keyup', event => {chat(event)});
recordButton.addEventListener('click', startRecording);
stopButton.addEventListener('click', stopRecording);

function startRecording() {
	console.log("recordButton clicked");
	stopButton.classList = 'btn btn-primary';
	stopButton.style.display = "inline-block";
	recordButton.style.display = "none";
	var constraints = { audio: true, video:false }

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
			console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
			audioContext = new AudioContext();

			
			gumStream = stream;
			input = audioContext.createMediaStreamSource(stream);

			rec = new Recorder(input,{numChannels:2})
			rec.record()
			console.log("Recording started");

		}).catch(function(err) {
			console.log(err);
	});
}

function stopRecording() {
	console.log("stopButton clicked");
	rec.stop();
	gumStream.getAudioTracks()[0].stop();
	recordButton.classList = 'btn btn-primary';
	recordButton.style.display = "inline-block";
	stopButton.style.display = 'none';
	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
	
	var url = URL.createObjectURL(blob);
	var filename = "12";
	const au = document.createElement('audio');
	// const audio_chat = document.getElementById('audbox');
	// const audio_question = document.getElementById('audque');
	// const audio_response = document.getElementById('audres');
	var xhr=new XMLHttpRequest();

	// au.controls = true;
	// au.src = url;

	xhr.onload=function(e) {
		if(this.readyState === 4) {
			console.log(e.target.responseText);
			var str = e.target.responseText;
			var response = JSON.parse(str);
			createChatBubble(response.query,"query");
			if (response.status === "OK"){
				createChatBubble(response.textres, "response");
			}
			else{
				createChatBubble(response.query, "response");
			}
			// const answer = document.getElementById('response');
			// answer.textContent = response.query;
			
			pageHeight = pageHeight + 5000;
  			$('#chatbot').scrollTop(pageHeight);
			aur = document.createElement('audio');
			aur.controls = true;
			aur.src = response.path;
			aur.autoplay = true;
			aur.style.display = "none";
			// audio_response.appendChild(aur);
		}
	};

	var fd=new FormData();
	fd.append("audio_data",blob, `question_${message_count}.wav`);
	xhr.open("POST","/speech");
	xhr.send(fd);
	// audio_question.appendChild(au);
}

const chat = event => {
	const url1 = `${window.origin}/getanswer`;

	// var pageHeight = $('#chatbot').height();

	if (event.keyCode === 13) {
		event.preventDefault();
		console.log("Click");

		inp = document.querySelector('#inputbox');
		let query = inp.value;

		//Creating a Chatbubble

		createChatBubble(query,'query');

		pageHeight = pageHeight + 5000;
  		$('#chatbot').scrollTop(pageHeight);
		inp.value = ''

		const entry = { query }
		fetch(url1,{
			method:'POST',
			credentials: "include",
			body: JSON.stringify(entry),
			cache: "no-cache",
			headers: new Headers({
				"content-type": "application/json"
			})
		}).then(response => response.json())
		.then(data => {
			console.log(data)
			createChatBubble(data,'response');
			
			pageHeight = pageHeight + 5000;
  			$('#chatbot').scrollTop(pageHeight);
			// reply.innerHTML = data
			// reply.style['text-align'] = "right";

			
		});
	}
}

function createChatBubble(text, type) {

	const cb = document.getElementById('chatbot');
	const que = document.createElement('div');

	if (type === "query"){
		message_count += 1;
		que.className = "talk-bubble tri-right round left-top";	
	}
	else{
		que.className = 'talk-bubble tri-right round right-top';
	}

	const que_text = document.createElement('div');
	que_text.className = "talktext";
	const pr = document.createElement('p');
	pr.innerHTML = text;
	que_text.appendChild(pr);
	que.appendChild(que_text);
	cb.appendChild(que);
	cb.appendChild(document.createElement("br"));

}