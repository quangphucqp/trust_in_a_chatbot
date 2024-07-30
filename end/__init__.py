from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'end'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class EndPageNoConsent(Page):

    @staticmethod
    def is_displayed(player: Player):
        return not player.participant.vars['consent']


class EndPage(Page):
    pass

    @staticmethod
    def map_to_letter(num):
        mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
        return mapping.get(num, '')

    @staticmethod
    def vars_for_template(player):
        return {
            'pre_round': player.participant.vars['pre_round'],
            'post_round': player.participant.vars['post_round'],
            'pre_correct_answer': EndPage.map_to_letter(player.participant.vars['pre_correct_answer']),
            'post_correct_answer': EndPage.map_to_letter(player.participant.vars['post_correct_answer']),
            'pre_belief': player.participant.vars['pre_belief'],
            'post_belief': player.participant.vars['post_belief'],
            'pre_reward': player.participant.vars['pre_reward'],
            'post_reward': player.participant.vars['post_reward'],
            'total_reward': player.participant.vars['total_reward'],
            'pre_random_number': round(player.participant.vars['pre_random_number'] * 100, 2),
            'post_random_number': round(player.participant.vars['post_random_number'] * 100, 2)
        }


page_sequence = [EndPageNoConsent, EndPage]
