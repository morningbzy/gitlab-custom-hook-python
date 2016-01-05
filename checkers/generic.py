
import re
import logging

import settings
from utils import get_reviewers
from .base import Checker


class AuthorChecker(Checker):
    """Check whether the push author is in the settings.AUTHORS or not.
    Reject if not.
    """
    def check(self):
        # Get the author name
        name = self.get_commit_author(self.new)

        # Get the reviewers
        reviewers = get_reviewers(name)

        # check the name and all reviewers
        checklist = list(reviewers) + [name]
        for checking in checklist:
            if checking not in settings.AUTHORS:
                return self.error('Name "%s" is not in author list. Please '
                                  'check your commit author name, or contact '
                                  'adminto add you in the list.' % checking)
        return self.OK


class JiraTaskIdChecker(Checker):
    """Check whether the commit messages contains 'Merge' or a JIRA task ID.
    Warn if not.
    """

    def check(self):
        regex = r'Merge|[A-Z]{,10}-\d+'

        for commit, commit_message in self.get_commit_messages():
            if not re.findall(regex, commit_message):
                warning_txt = 'No JIRA task ID found in the commit message: '\
                    + 'Please remember to add the task ID next time.\n'\
                    + '-' * 80\
                    + '\nCommit %s:\n\n%s\n' % (commit, commit_message.strip())\
                    + '-' * 80
                return self.warning(warning_txt)
        return self.OK


class MultiCommitsChecker(Checker):
    def check(self):
        for commit_message in self.get_commit_messages(self.old, self.new):
            logging.debug(commit_message)
            break
        logging.debug(len(self.get_commits()))
        return commit_message.startswith('Merge') or len(self.get_commits()) < 2


class UnclosedCodereviewRequestChecker(Checker):
    """Reject the push if there is an unclosed codereview request
    in reviewboard in the same branch.
    """
    def check(self):
        # TODO
        return self.OK
