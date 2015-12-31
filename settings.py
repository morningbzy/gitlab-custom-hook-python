

AUTHORS = (
    # Example:
    'lilei',
    'hanmeimei',
)

SKIPPED_BRANCHES_RE = (
    r'^dev_test$',
)

PRE_CHECKERS = (
    'checkers.generic.AuthorChecker',
    'checkers.generic.JiraTaskIdChecker',
)
