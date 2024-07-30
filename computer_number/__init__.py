from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'computer_number'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

    # COMPUTER NUMBER
    computer_number = models.IntegerField(
        label='Before beginning, please enter the computer number you are using:',
        min=1, max=30,
        widget=widgets.TextInput(),
    )
    computer_number_check = models.IntegerField(
        label='Please reenter the computer number to confirm:',
        min=1, max=30,
        widget=widgets.TextInput(),
    )


# PAGES
class ComputerNumberPage(Page):
    form_model = 'player'
    form_fields = ['computer_number', 'computer_number_check']

    @staticmethod
    def error_message(player: Player, values):
        if values['computer_number'] != values['computer_number_check']:
            return 'The two numbers you typed in do not match. Please try again.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.label = player.computer_number
        # add other var assignments as needed.


page_sequence = [ComputerNumberPage]
