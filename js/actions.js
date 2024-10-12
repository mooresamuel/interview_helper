import { removeLibraryQuestion, addUserQuestion } from "./database.js";
import { updateQuestions } from "./main.js";

const generateQuestions = document.getElementById('generate-questions');
const deleteQuestions = document.getElementById('delete-questions');
const importQuestions = document.getElementById('import-questions');
const play = document.getElementById('play');
const userQuestionsWindow = document.getElementById('user-questions-window');
const questionLibraryWindow = document.getElementById('question-library-window');

console.log("actions.js");  

importQuestions.addEventListener('click', () => {
    const buttons = questionLibraryWindow.querySelectorAll('.btn-check');
    console.log("clcik: ");
    buttons.forEach(button => {
        if (button.checked) {
            console.log(button);
            // userQuestionsWindow.innerHTML += question.nextElementSibling.outerHTML;
            addUserQuestion(button.id);
            removeLibraryQuestion(button.id);
            updateQuestions();
            // console.log("question: ", question);
        }
    });
});
