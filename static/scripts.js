const videoContainer = document.querySelector(".video-container");

const playPauseBtn = document.querySelector(".playPauseBtn");
const progress = document.querySelector(".progress");
const progressBar = document.querySelector(".progress__filled"); 

function togglePlay() {
  console.log(videoContainer.paused, videoContainer.ended)
  if (videoContainer.paused || videoContainer.ended) {
    videoContainer.play();
  } else {
    videoContainer.pause();
  }
}

function updatePlayBtn() {
  console.log(playPauseBtn.innerHTML)
  playPauseBtn.innerHTML = videoContainer.paused ? "►" : "❚❚";
}

// function handleProgress() {
//   const progressPercentage = (videoContainer.currentTime / videoContainer.duration) * 100;
//   progressBar.style.flexBasis = `${progressPercentage}%`;
// }

function jump(e) {
  const position = (e.offsetX / progress.offsetWidth) * videoContainer.duration;
  videoContainer.currentTime = position;
}

playPauseBtn.addEventListener("click", togglePlay); 
videoContainer.addEventListener("click", togglePlay);
videoContainer.addEventListener("click", togglePlay);
videoContainer.addEventListener("play", updatePlayBtn);
videoContainer.addEventListener("pause", updatePlayBtn);
// videoContainer.addEventListener("timeupdate", handleProgress); 

let mousedown = false;
// progress.addEventListener("click", jump);
// progress.addEventListener("mousedown", () => (mousedown = true));
// progress.addEventListener("mousemove", (e) => mousedown && jump(e));
// progress.addEventListener("mouseup", () => (mousedown = false));