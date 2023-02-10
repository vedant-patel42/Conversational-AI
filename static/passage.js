const sitebox = document.getElementById("sitetext");

sitebox.addEventListener('keyup', event => {scrape(event)});
const scrape = event => {
    const url = `${window.origin}/uploadpassage`;
    const url1 = `${window.origin}/getanswer`;
    console.log(url);

    if (event.keyCode === 13) {
        event.preventDefault();
		console.log("Click");

		inp = document.querySelector('#sitetext');
		let site = inp.value;
        inp.value = ''
        const entry = { site }

        fetch(url, {
            method: 'POST',
            body: JSON.stringify(entry),
			headers: new Headers({
				"Content-Type": "application/json"
			})
        }).then(response => response.json())
        .then(data => {
            // console.log(data)
            // print(data)
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
        })
        .catch(error => {
            console.error(error)
        })
    }
    
}

