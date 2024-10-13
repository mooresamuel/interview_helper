import { loginSuccess } from './main.js';

const loginForm = document.getElementById('loginForm');
const loginBtn = document.getElementById('submit');
const accordian1 = document.getElementById('accordian1');
const emailInput = document.getElementById('email');
const confirmPassword = document.getElementById('confirm-password');

export let userID;
let register = false;



accordian1.addEventListener('show.bs.collapse', () => {
    loginBtn.innerText = 'Register';
    emailInput.disabled = false;
    confirmPassword.disabled = false;
    register = !register;
});

accordian1.addEventListener('hidden.bs.collapse', () => {
    loginBtn.innerText = 'Log in';
    emailInput.disabled = true;
    confirmPassword.disabled = true;
    register = !register;
});

  
async function createUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;
    const confirmPwd = document.getElementById('confirm-password').value;
    if (password !== confirmPwd) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Passwords do not match',
          });      return;
    } 
    try {
      const response = await fetch('https://samalmoore1.eu.pythonanywhere.com/save_user', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password, email: email })
      });
      const result = await response.json();
      if (response.ok) {
        Swal.fire({
          icon: 'success',
          title: 'Success',
          text: result.message,
        });
        loginSuccess();
      } else {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: result.error,
            });
      }
    } catch (error) {
      console.error('Error:', error);
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: error,
      });
    }
  }
  
  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (register) {
      createUser();
      return;
    }
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    try {
      const response = await fetch('https://samalmoore1.eu.pythonanywhere.com/login', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
      });
      const result = await response.json();
      if (response.ok) {

        userID = result.id;
        console.log('userID:', userID);
        loginSuccess();
      } else {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: result.error,
        });
      }
    } catch (error) {
      console.error('Error:', error);
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'An error occurred while logging in',
      });
    }
  });

  const savedUserID = localStorage.getItem('userID');
  if (savedUserID) {
      // User is logged in, show the main screen
        userID = savedUserID;
        loginSuccess();
  }
  