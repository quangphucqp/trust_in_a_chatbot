from os import environ

SESSION_CONFIGS = [
    dict(
        name='questions_solving',
        app_sequence=['consent_waitpage',
                      'questions_practice', 'questions_seq_groupmove',
                      'survey_comprehensive', 'survey_demographics',
                      'end'],
        num_demo_participants=3,
    ),
    dict(
        name='rec_display_questions',
        app_sequence=['rec_question_practice', 'rec_question'],
        num_demo_participants=3,
    ),
    dict(
        name='rec_display_staticrec',
        app_sequence=['rec_static_practice', 'rec_static'],
        num_demo_participants=3,
    )
]

ROOMS = [
    dict(
        name='room_question_solving',
        display_name='room_question_solving',
        participant_label_file='_rooms/computer_number_solving.txt',
    ),
    dict(
        name='room_question_viewing',
        display_name='room_question_viewing',
        participant_label_file='_rooms/computer_number_viewing.txt',
    ),
    dict(
        name='room_rec',
        display_name='room rec',
        participant_label_file='_rooms/computer_number_rec.txt',
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6018060494160'

DEBUG = False
