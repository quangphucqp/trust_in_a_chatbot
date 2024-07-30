from otree.api import *
from parameters import Params


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'consent_waitpage'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # IRB NUMBER
    irb_number = Params.irb_number
    participation_fee = Params.participation_fee
    reward_correct = Params.reward_correct
    maximum_additional_reward = reward_correct * 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

    consent = models.BooleanField(
        choices=[
            [True, 'I have read the above information and agree to participate in this research.'],
            [False, 'I do not want to participate in this research.']
        ],
        widget=widgets.RadioSelect
    )


# PAGES
class ConsentPage(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            irb_number=C.irb_number,
            participation_fee=C.participation_fee,
            maximum_additional_reward=C.maximum_additional_reward
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.vars['consent'] = player.consent


class ConfirmPage(WaitPage):

    # Hold all participants here so that when the main app starts, all active ones ('consent' == True) enter
    # the same group

    body_text = "Please wait for all players before progressing."


page_sequence = [ConsentPage, ConfirmPage]

