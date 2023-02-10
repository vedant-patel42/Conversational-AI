const url = `${window.origin}/uploadwiki`;
const url1 = `${window.origin}/getanswer`;

console.log(url);

fetch(url)
.then(data => {
    // console.log(data)

    const inp = document.getElementById("inputbox");
    const rec_btn = document.getElementById("recordButton");
    const upload_box = document.getElementById("drop-area");

    rec_btn.style.display = "inline";
    inp.setAttribute('type','text');
    inp.setAttribute('size',50);
    inp.style.display = "inline";
    inp.focus();
  })
.catch(error => {
    console.error(error)
})
