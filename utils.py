
import os
import re
import settings


def get_reviewers(name):
    reviewers = set()
    for group in settings.GROUPS:
        if name in group:
            reviewers.update(group)

    reviewers.update(settings.SEPECIAL_REVIEWERS.get(name, []))

    # Remove the author
    if name in reviewers:
        reviewers.remove(name)
    return reviewers or settings.DEFAULT_REVIEWERS


def get_committor(new):
    # Get the author name
    cmd = '''git show %s --pretty="%%an"''' % new
    result = os.popen(cmd).readlines()
    if result:
        name = result[0].strip()
    else:
        name = None

    return name


def need_review(branch):
    # Check the branch need to be reviewed or not
    for re_str in settings.SKIPPED_BRANCHES_RE:
        if re.match(re_str, branch):
            return False
    return True
