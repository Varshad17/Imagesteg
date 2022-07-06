
const image = document.querySelector("#img");
const out = document.querySelector("#target");

 var uploaded_image = "";

 image.addEventListener("change",function(){
     const reader = new FileReader();
     reader.addEventListener("load",()=> {
     uploaded_image = reader.result;
     out.src=uploaded_image;
     });
 reader.readAsDataURL(this.files[0]);
});

var toggled  = true;



//function show(){
//out.style.display = 'block';
//}

function show(){
if(toggled){
out.style.display = 'block';
toggled = false;
return;
}
if(!toggled){
out.style.display = 'none';
toggled = true;
return;
}
}

let inputVal = document.getElementById("msg");

var txt = document.getElementById("text");

inputVal.addEventListener("change",function(){
     const reader = inputVal.value;
     txt.value = reader;
});



function showText(){
if(toggled){
txt.style.display = 'block';
toggled = false;
return;
}
if(!toggled){
txt.style.display = 'none';
toggled = true;
return;
}
}