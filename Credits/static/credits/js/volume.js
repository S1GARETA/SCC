var audioPlayer = document.getElementById("audioplayer"),
audioTrack = document.getElementById("audiotrack"),
playButton = document.createElement("button"),
muteButton = document.createElement("button"),
volumeSlider = document.createElement("input");

audioTrack.volume = 0.05;

setText(muteButton, "");

setAttributes(volumeSlider, { "type": "range",
                              "min": "0",
                              "max": "1",
                              "step": "any",
                              "value": "0.05",
                              "class": "volume_slider" });
setAttributes(muteButton, { "type": "button", "class": "volume_mute fa-solid fa-volume-xmark" });

audioPlayer.appendChild(muteButton);
audioPlayer.appendChild(volumeSlider);

muteButton.addEventListener("click", muter, false);
volumeSlider.addEventListener("input", function(){ audioTrack.volume = volumeSlider.value; }, false);
audioTrack.addEventListener('volumechange', volumizer, false);

// типо автозапуск музыки
document.addEventListener('click', musicPlay);
function musicPlay() {
  document.getElementById('audiotrack').play();
  document.removeEventListener('click', musicPlay);
}

function setText(el,text) {
  el.innerHTML = text;
}

function volumizer() {
  if (audioTrack.volume == 0) {
    muteButton.classList.remove("fa-volume-high");
    muteButton.classList.add("fa-volume-xmark");
    setText(muteButton,"");
  }
  else {
    muteButton.classList.add("fa-volume-high");
    muteButton.classList.remove("fa-volume-xmark");
    setText(muteButton,"");
  }
}

function muter() {
  if (audioTrack.volume == 0) {
    audioTrack.volume = restoreValue;
    volumeSlider.value = restoreValue;
  } else {
    audioTrack.volume = 0;
    restoreValue = volumeSlider.value;
    volumeSlider.value = 0;
  }
}

function setAttributes(el, attrs) {
  for(var key in attrs){
    el.setAttribute(key, attrs[key]);
  }
}
