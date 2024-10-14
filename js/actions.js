import { addUserQuestion, moveIntoUserQuestions, moveOutOfUserQuestions } from "./database.js";
import { updateQuestions } from "./main.js";
import { userQuestions, questionLibrary } from "./database.js";

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


transferQuestions.addEventListener('click', () => {
    const libraryButtons = questionLibraryWindow.querySelectorAll('.btn-check');
    let matched = 0;
    console.log("clcik: ");
    libraryButtons.forEach(button => {
        if (button.checked) {
            console.log(button);
            moveIntoUserQuestions(button.id);
            // removeLibraryQuestion(button.id);
            // updateQuestions();
            matched++;
        }
    });
    const userButtons = userQuestionsWindow.querySelectorAll('.btn-check');
    userButtons.forEach(button => {
        if (button.checked) {
            console.log(button);
            moveOutOfUserQuestions(button.id);
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
