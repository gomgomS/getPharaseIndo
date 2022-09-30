/*!
* Start Bootstrap - Grayscale v7.0.5 (https://startbootstrap.com/theme/grayscale)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

// dibawh ini set up video
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


// autoplay setup
// let videoSource = new Array();
// videoSource[0] = 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4';
// videoSource[1] = '../static/videos/moon.mp4';
// let i = 0; // global
// const videoCount = videoSource.length;
// const element = document.getElementById("videoPlayer");

// function videoPlay(videoNum) {
//     element.setAttribute("src", videoSource[videoNum]);
//     element.autoplay = true;
//     element.load();
// }
// document.getElementById('videoPlayer').addEventListener('ended', myHandler, false);

// videoPlay(0); // load the first video
// ensureVideoPlays();	// play the video automatically

// function myHandler() {
//     i++;
//     if (i == videoCount) {
//         i = 0;
//         videoPlay(i);
//     } else {
//         videoPlay(i);
//     }
// }

// function ensureVideoPlays() {
//     const video = document.getElementById('videoPlayer');

//     if(!video) return;
    
//     const promise = video.play();
//     if(promise !== undefined){
//         promise.then(() => {
//             // Autoplay started
//         }).catch(error => {
//             // Autoplay was prevented.
//             video.muted = true;
//             video.play();
//         });
//     }
}