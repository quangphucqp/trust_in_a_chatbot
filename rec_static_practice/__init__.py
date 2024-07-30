from otree.api import *
from question_and_rec_practice import QuestionsAndRecPractice
from parameters import Params
import ast
import random
import time


doc = """
This app displays the pre-generated recommendations in STATIC treatment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'STATIC_show_rec_practice'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


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
    pass

    form_model = 'player'
    form_fields = []

    @staticmethod
    def vars_for_template(player: Player):

        # COMPUTER_NUMBER = player.participant.label
        RecClass = QuestionsAndRecPractice()
        rec_df = RecClass.rec_df

        REC = rec_df['rec'].tolist()
        rec = REC[player.round_number - 1]


        return {
            'recommendation': rec
        }


page_sequence = [CoverPage, RecommendationPage]
