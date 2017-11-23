function fwd() {
  document.getElementById("signali-brze").style.backgroundColor = '#5cb85c';
  document.getElementById("signali-sporije").style.backgroundColor = '#ef2929';
  document.getElementById("signali-pauza").style.backgroundColor = '#5cb85c';
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "?cmd=brze", true);
  xhttp.send();
}

function bwd() {
  document.getElementById("signali-sporije").style.backgroundColor = '#5cb85c';
  document.getElementById("signali-brze").style.backgroundColor = '#ef2929';
  document.getElementById("signali-pauza").style.backgroundColor = '#5cb85c';
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "?cmd=sporije", true);
  xhttp.send();
}

function lijevo() {
  document.getElementById("signali-lijevo").style.backgroundColor = '#5cb85c';
  document.getElementById("signali-desno").style.backgroundColor = '#ef2929';
  document.getElementById("signali-pauza").style.backgroundColor = '#5cb85c';
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "?cmd=lijevo", true);
  xhttp.send();
}

function desno() {
  document.getElementById("signali-desno").style.backgroundColor = '#5cb85c';
  document.getElementById("signali-lijevo").style.backgroundColor = '#ef2929';
  document.getElementById("signali-pauza").style.backgroundColor = '#5cb85c';
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "?cmd=desno", true);
  xhttp.send();
}

function pauziraj() {
  document.getElementById("signali-pauza").style.backgroundColor = '#5cb85c';
  document.getElementById("signali-desno").style.backgroundColor = '#ef2929';
  document.getElementById("signali-lijevo").style.backgroundColor = '#ef2929';
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "?cmd=pauziraj", true);
  xhttp.send();
}

function stop_linija() {
  document.getElementById("signali-brze").style.backgroundColor = '#ef2929';
  document.getElementById("signali-sporije").style.backgroundColor = '#ef2929';
  document.getElementById("signali-lijevo").style.backgroundColor = '#ef2929';
  document.getElementById("signali-desno").style.backgroundColor = '#ef2929';
  document.getElementById("signali-pauza").style.backgroundColor = '#ef2929';
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "?cmd=stop", true);
  xhttp.send();
}

function record() {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "?cmd=record", true);
  xhttp.send();
}

function stop_record() {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "?cmd=stop-record", true);
  xhttp.send();
}

function take_photo() {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "?cmd=take-photo", true);
  xhttp.send();
}

function send_mail() {
}
