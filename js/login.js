import { get_user_questions } from "./database.js";


const loginModal = document.getElementById('loginModal');
const createAccountModal = document.getElementById('createAccountModal');
const createAccount = document.getElementById('createAccount');
const createAccountForm = document.getElementById('createAccountForm');
const loginForm = document.getElementById('loginForm');

export let userID;

createAccount.addEventListener('click', () => {
    loginModal.style.display = 'none';
    createAccountModal.style.display = 'block';
  
  });
  
  createAccountForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const newUsername = document.getElementById('newUsername').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const email = document.getElementById('email').value;
  
    if (newPassword !== confirmPassword) {
        Swal.fire({
            icon: 'success',
            title: 'Success',
            text: 'Passwords do not match',
          });      return;
    }
  
    try {
      const response = await fetch('http://127.0.0.1:8001/save_user', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: newUsername, password: newPassword, email: email })
      });
      const result = await response.json();
      if (response.ok) {
        Swal.fire({
          icon: 'success',
          title: 'Success',
          text: result.message,
        });
        createAccountModal.style.display = 'none';
        loginModal.style.display = 'block';
      } else {
        Swal.fire({
            icon: 'error',
            title: 'An error occurred while creating the account',
            text: result.error,
            });
      }
    } catch (error) {
      console.error('Error:', error);
      Swal.fire({
        icon: 'error',
        title: 'An error occurred while creating the account',
        text: result.error,
      });
    }
  });
  
  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
      const response = await fetch('http://127.0.0.1:8001/login', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
      });
      const result = await response.json();
      if (response.ok) {
        Swal.fire({
          icon: 'success',
          title: 'Success',
          text: 'Login successful',
        });
        loginModal.style.display = 'none';
        document.querySelector('.question-list').classList.remove('hidden');
        userID = result.id;
        console.log('userID:', userID);
        get_user_questions();
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