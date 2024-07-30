from otree.api import *


doc = """
Comprehensive Demographic Survey
"""


class Constants(BaseConstants):
    name_in_url = 'demographic_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Existing fields
    age = models.IntegerField(min=16, max=99, label='What is your age? Please fill in a number.')
    sex = models.IntegerField(choices=[[1, "Man"],
                                       [2, "Woman"],
                                       [3, "Prefer not to say"],
                                       [4, "Other (you can indicate in next page)"]],
                              widget=widgets.RadioSelect,
                              label='Are you a:'
                              )
    sex_other = models.StringField(blank=True, label="If you chose Other, please indicate. "
                                                     "You can also leave the field empty.")

    # New fields
    home_country = models.IntegerField(
        label='Where is your home country?',
        choices=[
            [1, 'Netherlands'],
            [2, 'Europe (other than the Netherlands)'],
            [3, 'Africa'],
            [4, 'USA/Canada'],
            [5, 'Latin/South America'],
            [6, 'West/Central Asia'],
            [7, 'East/South East Asia & South Asia'],
            [8, 'Other']
        ],
        widget=widgets.RadioSelect
    )
    field_of_study = models.IntegerField(
        label='What is your field of study?',
        choices=[
            [1, 'Economics and Management'],
            [2, 'Law'],
            [3, 'Social and Behavioral Sciences'],
            [4, 'Theology'],
            [5, 'Humanities'],
            [6, 'Other']
        ],
        widget=widgets.RadioSelect
    )
    study_program = models.IntegerField(
        label='Which program do you follow?',
        choices=[
            [1, 'Bachelor'],
            [2, 'Master'],
            [3, 'PhD'],
            [4, 'Other']
        ],
        widget=widgets.RadioSelect
    )


# PAGES
class SexAgeSurvey(Page):
    form_model = 'player'
    form_fields = ['age', 'sex']


class SexOther(Page):
    form_model = 'player'
    form_fields = ['sex_other']

    @staticmethod
    def is_displayed(player: Player):
        return player.sex == 4


class DemographicSurvey(Page):
    form_model = 'player'
    form_fields = ['home_country', 'field_of_study', 'study_program']


page_sequence = [SexAgeSurvey, SexOther, DemographicSurvey]
