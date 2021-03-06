

AUTHORS = (
    'lilei',
    'hanmeimei',
    'lily',
    'lucy',
    'morning',
)

SKIPPED_BRANCHES_RE = (
    r'dev_test',
)

PRE_CHECKERS = (
    'checkers.generic.AuthorChecker',
    'checkers.generic.JiraTaskIdChecker',
)

GROUPS = (
    ('lilei', 'hanmeimei'),
)

SEPECIAL_REVIEWERS = {
    'lucy': ('lily', ),
}

DEFAULT_REVIEWERS = ('morning', )

LOGGER_LEVEL = 'INFO'


REVIEWBOARD_USERNAME = 'gitlab'
REVIEWBOARD_PASSWORD = 'gitlab'
