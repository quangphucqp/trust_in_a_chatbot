from otree.api import *


doc = """
Comprehensive Survey Module
"""


class Constants(BaseConstants):
    name_in_url = 'comprehensive_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Risk-aversion
    risk_aversion = models.IntegerField(
        label='Now I would like to ask you something about how you see yourself. '
              'On a scale from 1 to 10, where 1 means "not at all willing to take risks" '
              'and 10 means "very willing to take risks", how would you rate yourself?',
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal
    )

    # Confidence and Overconfidence (adapted following Dunning-Kruger 1999)
    correct_answers_estimate = models.IntegerField(
        label='In this experiment, suppose that you answer each question by selecting one single answer option A, B, C, or D. '
              'Thinking about your responses, how many questions out of 5 do you think you answered correctly? Please provide your estimate below.',
        choices = [1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal
    )
    performance_percentile = models.IntegerField(
        label='Compared to other participants in this experiment, how well do you think you performed? '
              'Please rate your performance on a percentile scale from 0 to 99, where 0 means you performed worse than all other participants, '
              '50 means you performed better than half of the participants, and 99 means you performed better than almost all other participants.',
        min=0,
        max=99
    )
    logical_ability = models.IntegerField(
        label='How would you rate your ability to solve logical reasoning questions? '
              '(Responses were made on a scale ranging from 1 to 10, with 1 representing "very poor" and 10 representing "excellent.")',
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        widget=widgets.RadioSelectHorizontal
    )

    # Trust (European Value Survey)
    trust_people = models.IntegerField(
        label='Generally speaking, would you say that most people can be trusted or that you can\'t be too careful in dealing with people?',
        choices=[[1, 'Most people can be trusted'], [0, 'Can\'t be too careful']],
        widget=widgets.RadioSelect
    )
    fair_people = models.IntegerField(
        label='Do you think that most people would try to take advantage of you if they got the chance, or would they try to be fair? '
              'Please rate on a scale from 1 to 10, where 1 means "definitely take advantage of you" and 10 means "definitely try to be fair".',
        choices=list(range(1, 11)),
        widget=widgets.RadioSelectHorizontal
    )

    helpful_people = models.IntegerField(
        label='Would you say that most of the time people try to be helpful or that they are mostly looking out for themselves? '
              'Please rate on a scale from 1 to 10, where 1 means "mostly looking out for themselves" and 10 means "try to be helpful".',
        choices=list(range(1, 11)),
        widget=widgets.RadioSelectHorizontal
    )

    # AI skills
    use_ai_assistants = models.IntegerField(
        label='How often do you use AI assistants (such as Siri, Alexa, Google Assistant) in your daily life?',
        choices=[[1, 'Never'], [2, 'Rarely'], [3, 'Sometimes'], [4, 'Often'], [5, 'Daily']],
        widget=widgets.RadioSelect
    )
    interact_ai_chatbots = models.IntegerField(
        label='How frequently do you interact with AI-powered chatbots, such as ChatGPT?',
        choices=[[1, 'Never'], [2, 'Rarely'], [3, 'Sometimes'], [4, 'Often'], [5, 'Daily']],
        widget=widgets.RadioSelect
    )
    pay_for_ai = models.BooleanField(
        label='Do you currently pay for or subscribe to any premium versions of AI assistants or chatbots?',
        choices=[[True, 'Yes'], [False, 'No']],
        widget=widgets.RadioSelect
    )
    specify_ai_services = models.StringField(
        blank=True,
        label='If yes, please specify which service(s):'
    )
    ai_experience_level = models.IntegerField(
        label='How would you describe your experience level with AI assistants and chatbots?',
        choices=[[1, 'Novice (little to no experience)'], [2, 'Beginner (some basic experience)'], [3, 'Intermediate (moderate experience)'], [4, 'Advanced (extensive experience)']],
        widget=widgets.RadioSelect
    )
    ai_skill_comparison = models.IntegerField(
        label='Compared to other students, how would you rate your skills in using AI assistants and chatbots? '
              'Please rate your skills on a scale from 0 to 100, where 0 means you have lower skills than all other students, '
              '50 means you have average skills, and 100 means you have better skills than all other students.',
        min=0,
        max=100
    )


# PAGES
class RiskAversion(Page):
    form_model = 'player'
    form_fields = ['risk_aversion']


class ConfidenceOverconfidence(Page):
    form_model = 'player'
    form_fields = ['correct_answers_estimate', 'performance_percentile', 'logical_ability']


class Trust(Page):
    form_model = 'player'
    form_fields = ['trust_people', 'fair_people', 'helpful_people']


class AISkills(Page):
    form_model = 'player'
    form_fields = ['use_ai_assistants', 'interact_ai_chatbots', 'pay_for_ai', 'specify_ai_services', 'ai_experience_level', 'ai_skill_comparison']




page_sequence = [RiskAversion, ConfidenceOverconfidence, Trust, AISkills]
