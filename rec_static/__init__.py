from otree.api import *
from rec_from_xls import RecFromXls
from parameters import Params



doc = """
This app displays the pre-generated recommendations in STATIC treatment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'STATIC_show_rec'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = Params.num_rounds


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

    rec_label = models.StringField()
    rec_content = models.LongStringField()


# PAGES
class CoverPage(Page):
    pass


class RecommendationPage(Page):
    pass

    form_model = 'player'
    form_fields = []

    @staticmethod
    def vars_for_template(player: Player):
        COMPUTER_NUMBER = player.participant.label
        RecClass = RecFromXls()
        print(f"COMPUTER_NUMBER: {COMPUTER_NUMBER}")
        print(f"RecClass.rec_df keys: {list(RecClass.rec_df.keys())}")
        rec_df = RecClass.rec_df[int(COMPUTER_NUMBER)]

        REC = rec_df['rec'].tolist()
        rec = REC[player.round_number - 1]

        # Record the rec_label for the current round
        player.rec_label = rec_df['rec_label'][player.round_number - 1]

        # Record the rec content for the current round
        player.rec_content = rec

        return {
            'recommendation': rec
        }


page_sequence = [CoverPage, RecommendationPage]
