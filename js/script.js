
const questions = document.querySelector('.questions');
const logout = document.getElementById('logout');
const userInfoButton = document.getElementById('user-info');
const infoScreen = document.getElementById('info-screen');
const mainScreen = document.getElementById('main-screen');
const interviewScreen = document.getElementById('interview-screen');
const playButton = document.getElementById('play');

let infoShowing = false;
let interviewShowing = false;
let activescreen = mainScreen;

function hideMain(direction) {
  mainScreen.classList.remove('animate__animated', 'animate__fadeInUp');
  mainScreen.classList.remove('animate__animated', 'animate__fadeInDown');
  mainScreen.classList.add('animate__animated', direction);
}

function showMain(direction) {
  mainScreen.classList.remove('animate__animated', 'animate__fadeOutDown');
  mainScreen.classList.remove('animate__animated', 'animate__fadeOutUp');
  mainScreen.classList.add('animate__animated', direction);
  activescreen = mainScreen;
}

function hideInfo() {
  infoScreen.classList.remove('animate__animated', 'animate__fadeInDown');
  infoScreen.classList.add('animate__animated', 'animate__fadeOutUp');
}

function showInfo() {
  infoScreen.classList.remove('animate__animated', 'animate__fadeOutUp');
  infoScreen.classList.add('animate__animated', 'animate__fadeInDown');
  infoScreen.classList.remove('hidden');
  activescreen = infoScreen;
}

function hideInterview() {
  interviewScreen.classList.remove('animate__animated', 'animate__fadeInUp');
  interviewScreen.classList.add('animate__animated', 'animate__fadeOutDown');
}

function showInterview() {
  interviewScreen.classList.remove('animate__animated', 'animate__fadeOutDown');
  interviewScreen.classList.add('animate__animated', 'animate__fadeInUp');
  interviewScreen.classList.remove('hidden');
  activescreen = interviewScreen;
}

playButton.addEventListener('click', () => {
  if (interviewShowing) {
    hideInterview();
    showMain('animate__fadeInDown');
  } else if (infoShowing) {
    hideInfo();
    showInterview();
    infoShowing = false;
  } else {
    hideMain('animate__fadeOutUp');
    showInterview();
  }
  interviewShowing = !interviewShowing;
});

userInfoButton.addEventListener('click', () => {
  if (infoShowing) {
    hideInfo();
    showMain('animate__fadeInUp');
  } else if (interviewShowing) {
    hideInterview();
    showInfo();
    interviewShowing = false;
  } else {
    hideMain('animate__fadeOutDown');
    showInfo();
  }
  infoShowing = !infoShowing;
});

logout.addEventListener('click', () => {
  const actions = document.getElementById('actions');
  const moreActions = document.getElementById('more-actions');
  document.querySelector('.goodbye').classList.remove('hidden');
  localStorage.removeItem('userID');
  activescreen.classList.add('animate__animated', 'animate__hinge');
  actions.classList.remove('animate__animated', 'animate__fadeInRight');
  moreActions.classList.remove('animate__animated', 'animate__fadeInRight');
  actions.classList.add('animate__animated', 'animate__fadeOutRight');
  moreActions.classList.add('animate__animated', 'animate__fadeOutRight');
});
