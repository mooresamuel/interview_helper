import os
import json

import pandas as pd
import numpy as np

from dotenv import load_dotenv
# from sqlite_calls import SQLiteCalls
from anthropic_calls import AnthropicCalls
from sklearn.metrics.pairwise import cosine_similarity
from flask import jsonify


load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

LLM_calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY, stream=True)

generate_questions_call = AnthropicCalls(
    api_key=ANTHROPIC_API_KEY, 
    max_tokens=1024,
    system_prompt="You are a helpful assistant that is helping the user to paractice for an interview. You will generate 2 questions to help them practice their interview skills. If the user has very little experience, please focus on questions that will explore how they will tackle scenarios that are new to them but also relevant to the position. Don't mention exactly how many years of experience they have as these are rouugh figures (especially if the user has 10 years experience). YOU MUST USE THE TOOL PROVIDED FOR YOUR REPLIES\n"
)

def generated_questions(query: str):
    generator_tool = {
        "name": "save_interview_questions",
        "description": "Provides interview questions in JSON format when the user asks for interview questions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "question1": {
                    "type": "string",
                    "description": "Interview question"
                },
                "question2": {
                    "type": "string",
                    "description": "Interview question"
                },
                "question3": {
                    "type": "string",
                    "description": "Interview question"
                },
                "question4": {
                    "type": "string",
                    "description": "Interview question"
                },
                "question5": {
                    "type": "string",
                    "description": "Interview question"
                }
            },
            "required": ["question"]
        },     
    }
    
    response = generate_questions_call.chat(
        f"Query: {query}\n\nSaves generated questions in JSON format.",
        should_print=False,
        tools = [generator_tool],
        clear_after_response=False
    )
    questions = []
    print('\n\n',response)


    # if response.stop_reason == "tool_use":
    for item in response.content:
        # print(item)
        if item.type == "tool_use":
            questions.append({'question_text': item.input["question1"], 'is_generated': True})
            questions.append({'question_text': item.input["question2"], 'is_generated': True})

        #     for question in item.input:
        #         obj = {"question_text": question["question"]}

            # if item.type == "tool_use":
            #     if item.name == "save_interview_questions":
            #         print("\nTool_use: ", item)
            #         print("------")
            #         return item.input.get("chunk", False)
    # questions_json = json.dumps(questions)
    return questions



def generate_questions_claude(user_questions, data):
    experience = data.get('experience')
    job_title = data.get('job_title')
    job_str = f"The user is applying for a position as a {job_title}" if job_title else ""
    exp_str = f"The user has {experience} years of experience" if experience else ""
    user_questions_list = user_questions.to_dict(orient='records')
    u_qs = [question["question_text"] for question in user_questions_list]
    message = f"Please generate 2 job interview questions for the user. {job_str} {exp_str}. The user already has some questions to work from so please make your suggestions not too similar to theirs. Their saved questions are: {u_qs}. IT IS IMPORTANT THAT YOU USE THE TOOL PROVIDED! "

    new_questions = generated_questions(message)
    print('\n\n',new_questions,'\n\n')
    if isinstance(new_questions, str):
        new_questions = json.loads(new_questions)
    # print ('\n\n',new_questions,'\n\n')
    return new_questions



# def get_context(embedding, role="", n=1):
#     chat_df = SQL_calls.load_chat_to_dataframe(role)
#     context = find_top_n_similar(chat_df, embedding, n)
#     return context


# def find_top_n_similar(df, user_input_embedding, n=5):
#     if df.empty or 'embedding' not in df.columns:
#         print("The DataFrame is empty or missing the 'embedding' column.")
#         return pd.DataFrame()
    
#     df['embedding'] = df['embedding'].apply(
#         lambda emb: json.loads(emb) if isinstance(emb, str) else emb
#     )
#     df['similarity'] = df['embedding'].apply(
#         lambda emb: similarty_search(user_input_embedding, emb)
#     )

#     top_n_df = df.sort_values(by='similarity', ascending=False).head(n)
#     # To have messages in the correct order
#     top_n_df = top_n_df.sort_values(by='date', ascending=True)

#     return top_n_df


# def similarty_search(embedding1, embedding2):
#     embedding1 = np.array(embedding1).reshape(1, -1)
#     embedding2 = np.array(embedding2).reshape(1, -1)

#     similarity = cosine_similarity(embedding1, embedding2)

#     return similarity[0][0]

# def is_relevant(chunk: str, query: str):
#     response = context_determinator.chat(
#         f"Query: {query}\n\nChunk: {chunk}\n\nIs this chunk relevant to the query? Respond in JSON format.",
#         should_print=False,
#         clear_after_response=True
#     )
#     print("Chunk:\n", chunk)
#     print("Response:\n", response.content[0].text)
#     return json.loads(response.content[0].text)["is_relevant"]

# if __name__ == "__main__":
#     load_dotenv()
#     ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

#     LLM_calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY, stream=True)
#     SQL_calls = SQLiteCalls("key_words.db")
#     context_determinator = AnthropicCalls(
#         api_key=ANTHROPIC_API_KEY, 
#         max_tokens=400,
#         system_prompt="You are a helpful assistant that determines if a chunk of text is relevant to a given query.\n" +
#             "Respond with JSON object containing a boolean 'is_relevant' field and a 'reason' field explaining your decision"
#     )

#     user_data_extractor = AnthropicCalls(
#         api_key=ANTHROPIC_API_KEY, 
#         max_tokens=1024,
#         system_prompt="You are a helpful assistant that extracts chunk of user related data from given query.\n"
#     )

#     conversation()
