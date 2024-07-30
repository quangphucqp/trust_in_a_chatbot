from otree.api import *
from questions_from_xls import QuestionsFromXls
from parameters import Params
import ast
import random
import time


doc = """
This app is where participants answer the questions. 
All participants who gave consent form a single group.
"""


class C(BaseConstants):
    NAME_IN_URL = 'multiple_choice_task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = Params.num_rounds
    PARTICIPATION_FEE = Params.participation_fee
    REWARD_CORRECT = Params.reward_correct

    TIME_LIMIT_PRE = Params.time_limit_pre
    TIME_LIMIT_REC = Params.time_limit_rec
    TIME_LIMIT_POST = Params.time_limit_post


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


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

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'number_of_rounds': C.NUM_ROUNDS,
        }


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

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        player.rec_end_time = time.time()
        player.rec_duration = player.rec_end_time - player.rec_start_time

        # Logic if a timeout happened
        if timeout_happened:
            player.rec_timeout = True


class AfterFinalQuestionPage(Page):
    pass

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        available_rounds = list(range(1, C.NUM_ROUNDS + 1))

        # Select a random round for the pre-question raffle
        pre_random_round = random.choice(available_rounds)
        available_rounds.remove(pre_random_round)

        # Select a random round for the post-question raffle ensuring it's different from pre_random_round
        post_random_round = random.choice(available_rounds)

        player.participant.vars['pre_round'] = pre_random_round
        player.participant.vars['post_round'] = post_random_round


class LotteryandSurveyCover(Page):
    pass

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        pre_round = player.participant.vars.get('pre_round')
        post_round = player.participant.vars.get('post_round')

        COMPUTER_NUMBER = player.participant.label
        questions = QuestionsFromXls()
        qna_df = questions.qna_df[str(COMPUTER_NUMBER)]
        LABELS = qna_df['label'].tolist()

        def calculate_reward(round_number, task_type):
            if round_number is not None:
                correct_answer = LABELS[round_number - 1]
                belief_attr = f'{task_type}_belief_{chr(correct_answer + ord("a"))}'
                belief = getattr(player.in_round(round_number), belief_attr, None)

                if belief is not None:
                    random_number = random.random()
                    win = 1 if random_number < belief / 100 else 0
                    reward = C.REWARD_CORRECT if win else 0
                    return reward, correct_answer, belief, random_number
            return None, None, None, None

        player.pre_reward, pre_correct_answer, pre_belief, pre_random_number = calculate_reward(pre_round, 'pre')
        player.post_reward, post_correct_answer, post_belief, post_random_number = calculate_reward(post_round, 'post')
        player.total_reward = player.pre_reward + player.post_reward + C.PARTICIPATION_FEE

        player.participant.vars.update({
            'pre_round': pre_round,
            'post_round': post_round,
            'pre_correct_answer': pre_correct_answer,
            'post_correct_answer': post_correct_answer,
            'pre_belief': pre_belief,
            'post_belief': post_belief,
            'pre_reward': player.pre_reward,
            'post_reward': player.post_reward,
            'total_reward': player.total_reward,
            'pre_random_number': pre_random_number,  # store the random number for pre round
            'post_random_number': post_random_number,  # store the random number for post round
        })

        return {
            'pre_round': pre_round,
            'post_round': post_round,
            'pre_correct_answer': pre_correct_answer,
            'post_correct_answer': post_correct_answer,
            'pre_belief': pre_belief,
            'post_belief': post_belief,
            'pre_reward': player.pre_reward,
            'post_reward': player.post_reward,
            'total_reward': player.total_reward,
            'pre_random_number': pre_random_number,  # return the random number for pre round
            'post_random_number': post_random_number,  # return the random number for post round
        }

class GroupingWaitPage(WaitPage):
    body_text = "Please wait for the other participants to catch up."
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player: Player):
        # Only display this wait page in the first round if the player has consented
        return player.round_number == 1 and player.participant.vars.get('consent', False)


class OnHoldPage(WaitPage):
    body_text = "Please wait for the other participants to catch up."


page_sequence = [CoverPage,
                 PreQuestionPage,
                 OnHoldPage,
                 RecommendationPage,
                 OnHoldPage,
                 PostQuestionPage,
                 OnHoldPage,
                 AfterFinalQuestionPage, LotteryandSurveyCover]

