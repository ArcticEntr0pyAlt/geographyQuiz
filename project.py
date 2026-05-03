import easygui
import json
import os
import random
# Libraries used. The only externally sourced library that isnt a native part of python (it is however built on Tkinter which is native to python).

QUESTIONS_FILE = 'questions.json'
LEADERBOARD_FILE = 'leaderboard.json'
MAX_QUESTIONS = 20
MAX_ATTEMPTS = 5
POINTS_PER_CORRECT = 10
# Variables used through the game

# Project: Geography Quiz Game, utilising the EasyGUI library.
# Description: A simple quiz game that tests players' knowledge of geography and specific countries. Players will be given facts about a country and must guess which country it is. The game keeps track of scores and automatically creates a leaderboard json file if such doesnt already exit (do not make a file yourself or it will break. let the code make one for you.)

def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        easygui.msgbox(f'Error: {QUESTIONS_FILE} not found. Create the file and try again.')
        return []
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)
    # Checks if the questions file exists and loads it


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)
    # checks if the leaderboard file exists and loads it.
    # if the file does not exist, one will be created at the end of a game once a name is provided.


def save_leaderboard(entries):
    with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries[:10], f, indent=2, ensure_ascii=False)


def record_score(name, score):
    entries = load_leaderboard()
    entries.append({'name': name, 'score': score})
    entries.sort(key=lambda e: e['score'], reverse=True)
    save_leaderboard(entries)
    # this function records a player's score in the leaderboard.json file.


def show_leaderboard():
    entries = load_leaderboard()
    if not entries:
        easygui.msgbox('Leaderboard is empty yet.')
        return
    lines = '\n'.join(f"{idx + 1}. {e['name']} - {e['score']}" for idx, e in enumerate(entries[:10]))
    easygui.msgbox('----- LEADERBOARD -----\n' + lines)
    # Shows the leaderboard at the end of the game if the leaderboard.json file exists and has data in it.


def player_info_for_leaderboard(score):
    name = easygui.enterbox(f'Congratulations! Your final score is: {score}\nPlease enter your name for the leaderboard:')
    if name is None or not name.strip():
        return 'Anonymous', score
    return name.strip(), score
# Asks for your name to add to the leaderboard. If a name is not given, you will be named "Anonymous."


def run_game_once():
    questions = load_questions()
    if not questions:
        return None

    random.shuffle(questions)
    questions = questions[:MAX_QUESTIONS]

    score = 0
    attempts = MAX_ATTEMPTS

    for question in questions:
        if attempts <= 0:
            break

        fact_text = question.get('fact', 'No fact provided. Guess the country')
        answer = easygui.enterbox(fact_text)

        if answer is None:
            easygui.msgbox('Game cancelled.')
            return None

        answer_clean = answer.strip().lower()
        if not answer_clean:
            easygui.msgbox('Please enter a country to continue.')
            continue

        correct_country = str(question.get('country', '')).strip().lower()
        if answer_clean == correct_country:
            score += POINTS_PER_CORRECT
            easygui.msgbox(f'Correct! Your score is now {score}.')
        else:
            attempts -= 1
            easygui.msgbox(f'Incorrect. Attempts left: {attempts}.')

    easygui.msgbox(f'Game over! Your final score is: {score}')
    return score
# Main game function that adds score based on correct answer and deducts your remaining attempts if you get a question wrong.
# It also grabs the 20 random questions from questions.json.

def main():
    easygui.msgbox('Welcome to the Geography Quiz! You have 5 attempts and 20 questions per game.')

    while True:
        score = run_game_once()
        if score is None:
            break

        name, final_score = player_info_for_leaderboard(score)
        record_score(name, final_score)
        show_leaderboard()

        if not easygui.ynbox('Play again?', 'Continue?', choices=['Yes', 'No']):
            break

    easygui.msgbox('Thanks for playing!')
    # the introduction screen you're met with upon starting the game or playing again.
    # there's also the end screen that asks if you wanna play again or not.
    # and it appends the name you give for your score (if one is not provided, it will default to anonymous), and your score, to the leaderboard.json file.
    # Scores and names are displayed at the end of the game if there are scores that exist.


if __name__ == '__main__':
    main()

# yah this is the project hope u enjoy