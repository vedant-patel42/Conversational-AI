
const switcher = document.getElementById("myonoffswitch");
const select_menu = document.getElementById("selectMenu");

switcher.addEventListener('change', event => {
	console.log("Changed Propertyl");
	const update = document.getElementById('updating');
	update.textContent = "Updating...";
	console.log(switcher.checked);
	updatePreference();
});


document.querySelector('#fileUpload').addEventListener('change', event => {
	const files = event.target.files;
	handleUpload(files)
});

select_menu.addEventListener('change', event => {
	console.log("Changed");
	console.log(event);
	console.log(select_menu.value);
	const url = `${window.origin}/upload`;

	data = {sampledata:select_menu.value}

	fetch(url,{
		method: 'post',
		body: JSON.stringify(data),
		headers: {
	      'Content-Type': 'application/json'
	    },
	}).then(response => response.json())
	.then(data => {
		displayData(data);
	})
	.catch (error => {
		console.log(error);
	})
});

let dropArea = document.getElementById('drop-area');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
	dropArea.addEventListener(eventName, preventDefaults, false)
});

function preventDefaults (e) {
	e.preventDefault()
	e.stopPropagation()
}

;['dragenter', 'dragover'].forEach(eventName => {
	dropArea.addEventListener(eventName, highlight, false)
})

;['dragleave', 'drop'].forEach(eventName => {
	dropArea.addEventListener(eventName, unhighlight, false)
})

function highlight(e) {
	dropArea.classList.add('highlight')
}

function unhighlight(e) {
	dropArea.classList.remove('highlight')
}

dropArea.addEventListener('drop', handleDrop, false)

function handleDrop(e) {
	let dt = e.dataTransfer
	let files = dt.files

	handleUpload(files)
}


const handleUpload = files => {
	const url = `${window.origin}/upload`;
	const url1 = `${window.origin}/getanswer`;
	console.log(url);

	const formData = new FormData()
	console.log('file',files);
	formData.append('table', files[0], files[0].name)
	console.log('formdata',formData)

	fetch(url, {
		method: 'POST',
		body: formData
	}).then(response => response.json())
	.then(data => {

		console.log(data);
		displayData(data);
	  })
	.catch(error => {
		console.error(error)
	})
}

function updatePreference(){

	const url = `${window.origin}/updatelangauge`;

	console.log(switcher.checked);
	let data;
	if (switcher.checked){
		console.log("Send switch to English");
		data = {
			language:'en-IN'
		}
	}
	else{
		console.log("Sending switch to hindi");
		data = {
			language:'hi-IN'
		}
	}

	fetch(url,{
		method: 'post',
		body: JSON.stringify(data),
		headers: {
	      'Content-Type': 'application/json'
	    },
	}).then(response => response.json())
	.then(data => {
		const update = document.getElementById('updating');
		update.textContent = "Updated Language preference";
		console.log(data);
		update.textContent = "";
	})
	.catch (error => {
		console.log(error);
	})
	
}

function displayData(data){
	document.getElementById('tabledis').innerHTML = data.ans;
	const box = document.getElementById('chat1');
	const inp = document.getElementById("inputbox");
	const rec_btn = document.getElementById("recordButton");
	const upload_box = document.getElementById("drop-area");

	rec_btn.style.display = "inline";
	inp.setAttribute('type','text');
	inp.setAttribute('size',50);
	inp.style.display = "inline";
	inp.focus();
	box.style['text-align'] = 'center';
	upload_box.style.display = "none";
}