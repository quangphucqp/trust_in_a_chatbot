from otree.api import *
from question_and_rec_practice import QuestionsAndRecPractice
from parameters import Params
import ast
import time


doc = """
This app is where participants answer the questions. 
All participants who gave consent form a single group.
"""


class C(BaseConstants):
    NAME_IN_URL = 'multiple_choice_task_practice'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    TIME_LIMIT_PRE = Params.time_limit_pre
    TIME_LIMIT_REC = Params.time_limit_rec
    TIME_LIMIT_POST = Params.time_limit_post


class Subsession(BaseSubsession):
    consenting_group_formed = models.BooleanField(initial=False)
    non_consenting_group_formed = models.BooleanField(initial=False)



class Group(BaseGroup):
    pass

    recommendation_start_time = models.FloatField(initial=0)


class Player(BasePlayer):
    pass

    # BELIEFS:
    pre_belief_a = models.IntegerField(min=0, max=100)
    pre_belief_b = models.IntegerField(min=0, max=100)
    pre_belief_c = models.IntegerField(min=0, max=100)
    pre_belief_d = models.IntegerField(min=0, max=100)

    post_belief_a = models.IntegerField(min=0, max=100)
    post_belief_b = models.IntegerField(min=0, max=100)
    post_belief_c = models.IntegerField(min=0, max=100)
    post_belief_d = models.IntegerField(min=0, max=100)

    # RECORD DROPPED TASKS DUE TO TIMEOUT:
    pre_task_dropped = models.BooleanField(initial=False)
    post_task_dropped = models.BooleanField(initial=False)

    # RECORD SELECTED TASKS FOR RAFFLE:
    pre_selected_task = models.BooleanField(initial=False)
    post_selected_task = models.BooleanField(initial=False)

    # REWARDS (ONLY COUNT FOR LAST ROUND):
    pre_reward = models.IntegerField(initial=0)
    post_reward = models.IntegerField(initial=0)
    total_reward = models.IntegerField(initial=0)

    # RECORD TIME SPENT ON TASKS:
    pre_start_time = models.FloatField()
    pre_end_time = models.FloatField()
    pre_duration = models.FloatField()
    post_start_time = models.FloatField()
    post_end_time = models.FloatField()
    post_duration = models.FloatField()
    rec_start_time = models.FloatField()
    rec_end_time = models.FloatField()
    rec_duration = models.FloatField()
    rec_timeout = models.BooleanField(initial=False)


# PAGES
class CoverPage(Page):
    pass


class PreQuestionPage(Page):
    pass

    timeout_seconds = C.TIME_LIMIT_PRE

    form_model = 'player'
    form_fields = ['pre_belief_a', 'pre_belief_b', 'pre_belief_c', 'pre_belief_d']
    labels = {
        'pre_belief_a': '',
        'pre_belief_b': '',
        'pre_belief_c': '',
        'pre_belief_d': '',
    }

    # Display the content of the page
    @staticmethod
    def vars_for_template(player: Player):

        player.pre_start_time = time.time()

        COMPUTER_NUMBER = player.participant.label
        practicedata = QuestionsAndRecPractice()
        qna_df = practicedata.qna_df

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

    @staticmethod
    def error_message(player:Player, values):
        if values['pre_belief_a'] + values['pre_belief_b'] + values['pre_belief_c'] + values['pre_belief_d'] != 100:
            return 'The sum of the four beliefs must be 100.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        player.pre_end_time = time.time()
        player.pre_duration = player.pre_end_time - player.pre_start_time

        if timeout_happened:
            player.pre_task_dropped = True


class PostQuestionPage(Page):
    pass

    timeout_seconds = C.TIME_LIMIT_POST

    form_model = 'player'
    form_fields = ['post_belief_a', 'post_belief_b', 'post_belief_c', 'post_belief_d']
    labels = {
        'pre_belief_a': '',
        'pre_belief_b': '',
        'pre_belief_c': '',
        'pre_belief_d': '',
    }

    @staticmethod
    def vars_for_template(player: Player):

        player.post_start_time = time.time()

        # COMPUTER_NUMBER = player.participant.label
        practicedata = QuestionsAndRecPractice()
        qna_df = practicedata.qna_df

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

    @staticmethod
    def error_message(player:Player, values):
        if values['post_belief_a'] + values['post_belief_b'] + values['post_belief_c'] + values['post_belief_d'] != 100:
            return 'The sum of the four beliefs must be 100.'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        player.post_end_time = time.time()
        player.post_duration = player.post_end_time - player.post_start_time

        if timeout_happened:
            player.post_task_dropped = True


class RecommendationPage(Page):

    timeout_seconds = C.TIME_LIMIT_REC

    form_model = 'player'
    form_fields = []

    @staticmethod
    def vars_for_template(player: Player):

        player.rec_start_time = time.time()

        COMPUTER_NUMBER = player.participant.label
        practicedata = QuestionsAndRecPractice()
        qna_df = practicedata.qna_df

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

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        player.rec_end_time = time.time()
        player.rec_duration = player.rec_end_time - player.rec_start_time

        # Logic if a timeout happened
        if timeout_happened:
            player.rec_timeout = True


class GroupingWaitPage(WaitPage):
    body_text = "Please wait for the other participants to catch up."
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        # Create two empty lists to hold players who consented and did not consent
        consent_yes = []
        consent_no = []

        # Divide all the players by whether they've given consent
        for p in subsession.get_players():
            if p.participant.vars['consent']:
                consent_yes.append(p)
            else:
                consent_no.append(p)

        # Form groups
        subsession.set_group_matrix([consent_yes, consent_no])

        # Set participant variable for redirection
        for p in consent_no:
            p.participant.vars['redirect_to_last_app'] = True

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.vars.get('redirect_to_last_app', False):
            return upcoming_apps[-1]
        return None


class OnHoldPage(WaitPage):
    body_text = "Please wait for the other participants to catch up."


class ReadInstructionPage(Page):
    pass


page_sequence = [GroupingWaitPage,
                 ReadInstructionPage,
                 OnHoldPage,
                 CoverPage,
                 PreQuestionPage,
                 OnHoldPage,
                 RecommendationPage,
                 OnHoldPage,
                 PostQuestionPage,
                 OnHoldPage]

