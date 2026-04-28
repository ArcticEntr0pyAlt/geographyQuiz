import easygui
import json
import os
import random

QUESTIONS_FILE = 'questions.json'
LEADERBOARD_FILE = 'leaderboard.json'
MAX_QUESTIONS = 20
MAX_ATTEMPTS = 5
POINTS_PER_CORRECT = 10

# Project: Geography Quiz Game
# Description: A simple quiz game that tests players' knowledge of geography and specific countries. Players will be given facts about a country and must guess which country it is. The game keeps track of scores and automatically creates a leaderboard json file if such doesnt already exit (do not make a file yourself or it will break. let the code make one for you.)
# Can this dev code? Absolutely not, but we ball.

def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        easygui.msgbox(f'Error: {QUESTIONS_FILE} not found. Create the file and try again.')
        return []
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_leaderboard(entries):
    with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries[:10], f, indent=2, ensure_ascii=False)


def record_score(name, score):
    entries = load_leaderboard()
    entries.append({'name': name, 'score': score})
    entries.sort(key=lambda e: e['score'], reverse=True)
    save_leaderboard(entries)


def show_leaderboard():
    entries = load_leaderboard()
    if not entries:
        easygui.msgbox('Leaderboard is empty yet.')
        return
    lines = '\n'.join(f"{idx + 1}. {e['name']} - {e['score']}" for idx, e in enumerate(entries[:10]))
    easygui.msgbox('----- LEADERBOARD -----\n' + lines)


def player_info_for_leaderboard(score):
    name = easygui.enterbox(f'Congratulations! Your final score is: {score}\nPlease enter your name for the leaderboard:')
    if name is None or not name.strip():
        return 'Anonymous', score
    return name.strip(), score


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
# what the fuck

def main():
    easygui.msgbox('Welcome to the Geography Quiz! You have 5 attempts and 15 questions per game.')

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


if __name__ == '__main__':
    main()
