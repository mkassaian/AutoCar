function u(){
$.post("/forward");
}

function v(){
$.post("/left");
}

function w(){
$.post("/right");
}

function x(){
$.post("/stop");
}

function y(){
$.post("/reverse");
}

function success(data, status, xhr){
document.getElementById("shifter").innerHTML = data.replace(/\n/g, "<br/>");
}

function home(){
x();
poll();
document.getElementById("shifter").innerHTML = "Hello!";
}

function poll(){
$.post("/poll", null, pollSuccess);
}

function pollSuccess(data, status, xhr){
success(data, status, xhr);
setTimeout(poll, 250);
}