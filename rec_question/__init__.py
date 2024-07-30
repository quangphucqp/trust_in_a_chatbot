from otree.api import *
from questions_from_xls import QuestionsFromXls
from parameters import Params
import ast
import random
import time

doc = """
This app shows the questions on REC computer so that participants can 
either copy-paste (in CHATBOT) or refer to (in STATIC)
"""


class C(BaseConstants):
    NAME_IN_URL = 'CHATBOT_show_questions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = Params.num_rounds


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class CoverPage(Page):
    pass


class RecommendationPage(Page):

    form_model = 'player'
    form_fields = []

    @staticmethod
    def vars_for_template(player: Player):

        COMPUTER_NUMBER = player.participant.label
        questions = QuestionsFromXls()
        qna_df = questions.qna_df[str(COMPUTER_NUMBER)]

        CONTEXTS = qna_df['context'].tolist()
        QUESTIONS = qna_df['question'].tolist()
        ANSWER_OPTIONS = qna_df['answers'].tolist()

        context = CONTEXTS[player.round_number - 1]
        question = QUESTIONS[player.round_number - 1]
        answer_options_str = ANSWER_OPTIONS[player.round_number - 1]
        answer_options = ast.literal_eval(answer_options_str)

        return {
            'context': context,
            'question': question,
            'answer_a': answer_options[0],
            'answer_b': answer_options[1],
            'answer_c': answer_options[2],
            'answer_d': answer_options[3],
        }


page_sequence = [CoverPage, RecommendationPage]
