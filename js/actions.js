import { addUserQuestion, assignQuestion, unassignQuestion } from "./database.js";
import { updateQuestions, experience, jobTitle } from "./main.js";
import { source, userQuestions, questionLibrary } from "./database.js";
import { userID } from "./login.js";

const generateQuestions = document.getElementById('generate-questions');
const deleteQuestions = document.getElementById('delete-questions');
const transferQuestions = document.getElementById('transfer-questions');
const play = document.getElementById('play');
const userQuestionsWindow = document.getElementById('user-questions-window');
const questionLibraryWindow = document.getElementById('question-library-window');
const generatedQuestionsWindow = document.getElementById('generated-questions-window');
const customQuestion = document.getElementById('custom-question');

console.log("actions.js");  

customQuestion.addEventListener('click', () => {
    const question = prompt('Enter your custom question:');
    if (question) {
        addUserQuestion(question);
    }
});

generateQuestions.addEventListener('click', () => {
    fetch(`${source}generate_questions`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userID,
            job_title: jobTitle,
            experience: experience
        })
    })
    .then(() => {
        updateQuestions();
        console.log("update questions");
    })
    .catch(error => {
        console.error('Error:', error);
    });
});



transferQuestions.addEventListener('click', () => {
    const libraryButtons = questionLibraryWindow.querySelectorAll('.btn-check');
    let matched = 0;
    console.log("clcik: ");
    libraryButtons.forEach(button => {
        if (button.checked) {
            console.log(button);
            assignQuestion(button.id);
            // removeLibraryQuestion(button.id);
            // updateQuestions();
            matched++;
        }
    });
    const generatedButtons = generatedQuestionsWindow.querySelectorAll('.btn-check');
    generatedButtons.forEach(button => {
        if (button.checked) {
            console.log(button);
            assignQuestion(button.id, 'generated');
            matched++;
        }
    });
    const userButtons = userQuestionsWindow.querySelectorAll('.btn-check');
    userButtons.forEach(button => {
        if (button.checked) {
            console.log(button);
            unassignQuestion(button.id);
            // removeLibraryQuestion(button.id);
            // updateQuestions();
            matched++;
        }
    });
    if (matched === 0) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No questions selected, choose some questions to move!',
        });
    }
});
