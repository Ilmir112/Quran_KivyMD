import os
import requests

from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.gridlayout import GridLayout

import random
import dataloader as dt

word = []
word_dict = dt.data_from_json(word)  # база данных из суры 30 в виде словаря


class CustomOverFlowMenu(MDDropdownMenu):
    pass

class AnswerButton(Button): # Класс кнопки в quiz.kv
    bg_color = ListProperty([1, 1, 1, 1])

class LearnButton(Button): # Класс кнопки в learn.kv
    bg_color = ListProperty([1, 1, 1, 1])

class SelectAyatsButton(Button):
    bg_color = ListProperty([1, 1, 1, 0])

class SelectGameButton(Button):
    bg_color = ListProperty([1, 1, 1, 0])

class SelectGameButton(Button):
    bg_color = ListProperty([1, 1, 1, 0])


class SelectAyatButton(Button):
    bg_color = ListProperty([1, 1, 1, 0])

class Quran_KivyMD(MDApp):
    selected_word = ''
    right_answer = ''
    selected_game = ''
    filename = ''
    correct = 0
    wrong = 0
    success_rate = 0
    ayat_more = 0
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"

        global sm
        sm = ScreenManager(transition=NoTransition())
        # sm.add_widget(Builder.load_file('main.kv'))
        sm.add_widget(Builder.load_file('select_ayats.kv'))
        sm.add_widget(Builder.load_file('select_ayat.kv'))
        sm.add_widget(Builder.load_file('select_game.kv'))
        sm.add_widget(Builder.load_file('quiz.kv'))
        sm.add_widget(Builder.load_file('learn.kv'))
        return sm

    def select_word(self, instance):  # функция подбора слова для изучения из выбранного аята
        word1 = word_dict[self.selected_word]
        word_random = random.choice(word1)
        url = word_random[1]
        word_sel = f'data/files_mp3{url[4:-4]}.mp3'
        self.filename = f'data/files_mp3{url[4:-4]}.mp3'
        self.btn_word_pressed(url, word_sel)
        print("Файл успешно сохранен.")
        sm.get_screen('learn').ids.word.text = f'{word_random[2]}'
        sm.get_screen('learn').ids.word1.text = f'{word_random[0]}'
        sm.get_screen('learn').ids.transition_1.text = f'Транскрипция [{word_random[3]}]'

        sm.current = 'learn'

    def next_word(self):
        self.select_word(self.selected_word)
    def text_ayat_id(self, instance):
        if instance == 'айты 1-20':
            self.ayat_more = 0

        elif instance == 'айты 21-40':
            self.ayat_more = 1

        elif instance == 'айты 41-60':
            self.ayat_more = 2
        ayat_more = self.ayat_more

        for i in range(1, 21):
            sm.get_screen('select_ayat').ids[f'ayat{i}'].text = f'Айат {i + (20 * ayat_more)}'

        sm.current = 'select_ayat'

    def next_question(self):
        self.quiz_game(self.selected_game)
        for i in range(1, 7):
            sm.get_screen('quiz').ids[f'answer{i}'].disabled = False
            sm.get_screen('quiz').ids[f'answer{i}'].bg_color = (40 / 255, 6 / 255, 109 / 255, 1)
            sm.get_screen('quiz').ids[f'answer{i}'].disabled_color = (1, 1, 1, 0.3)

    def final_score(self):
        if self.correct == 0 and self.wrong == 0:
            sm.correct = 'main'
        else:
            for i in range(1, 7):
                sm.get_screen('quiz').ids[f'answer{i}'].disabled = False
                sm.get_screen('quiz').ids[f'answer{i}'].bg_color = (40 / 255, 6 / 255, 109 / 255, 1)
                sm.get_screen('quiz').ids[f'answer{i}'].disabled_color = (1, 1, 1, 0.3)
            success_rate = round((self.correct / (self.correct + self.wrong)) * 100)
            sm.get_screen('final_score').correct.text = f'{self.correct} - Верно'
            sm.get_screen('final_score').wrong.text = f'{self.wrong} - Неверно'
            sm.get_screen('final_score').success_rate.text = f'{success_rate}% верных ответов'

            sm.current = 'final_score'

    def select_game(self, instance):
        self.select_word_dict(self, instance)
        sm.current = 'select_game'

    def select_ayats(self, instance):
        print(self.ayat_more)
        sm.current = 'select_ayats'

    def select_word_dict(self, word_dict, instance):
        self.selected_word = int(str(instance)[-2:])

    def quiz_game(self, game):
        self.selected_game = game
        question_random = random.choice(word_dict[self.selected_word])

        url = question_random[1]
        filename = f'data/files_mp3{url[4:-4]}.mp3'
        self.filename = f'data/files_mp3{url[4:-4]}.mp3'
        self.btn_word_pressed(url, filename)

        print("Файл успешно сохранен.")
        guestion1 = question_random[0]
        self.right_answer = question_random[2]
        answer_list = [self.right_answer]

        while len(answer_list) != 6:
            answer_random = random.choice(word_dict[self.selected_word])
            if answer_random[2] not in answer_list:
                answer_list.append(answer_random[2])

        random.shuffle(answer_list)
        sm.get_screen('quiz').ids.question.text = f'{guestion1}'

        for i in range(1, 7):
            sm.get_screen('quiz').ids[f'answer{i}'].text = f'{answer_list[i - 1]}'

        sm.current = 'quiz'

    answer_dict = {}

    def get_id(self, instance):

        for id, widget in instance.parent.parent.parent.ids.items():
            if widget.__self__ == instance:
                return id

    def quiz(self, answer, instance):
        if answer == self.right_answer:
            self.correct += 1
            sm.get_screen('quiz').ids[self.get_id(instance)].bg_color = (0, 1, 0, 1)
            answer_id_list = ['answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'answer6']
            answer_id_list.remove(self.get_id(instance))
            for i in range(1, 7):
                sm.get_screen('quiz').ids[f'{answer_id_list[i]}'].disabled = True
        else:

            sm.get_screen('quiz').ids[self.get_id(instance)].bg_color = (1, 0, 0, 0)
            for i in range(1, 7):
                if sm.get_screen('quiz').ids[f'answer{i}'].text == self.right_answer:
                    sm.get_screen('quiz').ids[f'answer{i}'].bg_color = (0, 1, 0, 1)
                else:
                    sm.get_screen('quiz').ids[f'answer{i}'].disabled = True
            sm.get_screen('quiz').ids[self.get_id(instance)].bg_color = (1, 0, 1, 0)
            sm.get_screen('quiz').ids[self.get_id(instance)].disabled_color = (1, 1, 1, 1)
        sm.get_screen('quiz').ids.correct_answer.text == f'верно {self.correct}'
        sm.get_screen('quiz').ids.wrong_answer.text == f'верно {self.wrong}'
        # sm.get_screen('quiz').correct.text = f'{self.wrong_answer} верно'

    def callback(self, instance_action_top_appbar_button):
        self.root.current = instance_action_top_appbar_button

    def download_mp3(self, url, filename):
        http = "https://audio.qurancdn.com/"
        filename = f'data/files_mp3/{url[4:-4]}.mp3'
        self.filename = filename
        response = requests.get(f'{http}{url}')
        response.raise_for_status()
        print(filename)

        with open(filename, "wb") as file:
            file.write(response.content)

    def btn_word_pressed(self, url, filename):
        http = "https://audio.qurancdn.com/"
        filename = f'data/files_mp3/{url[4:-4]}.mp3'
        self.filename = filename
        response = requests.get(f'{http}{url}')
        response.raise_for_status()

        with open(filename, "wb") as file:
            file.write(response.content)

        sound = SoundLoader.load(filename)
        sound.play()


if __name__ == '__main__':
    Quran_KivyMD().run()
