
import logging

import settings
from utils.git import get_commits, get_commit_messages, get_commit_author


class Checker(object):
    def __init__(self, old, new, ref):
        self.old = old
        self.new = new
        self.ref = ref
        self.opts = self.__dict__
        self.OK = True
        self.__logger = None

    @property
    def logger(self):
        if self.__logger is None:
            self.__logger = logging.getLogger(self.__class__.__name__)
            hdlr = logging.StreamHandler()
            hdlr.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
            self.__logger.addHandler(hdlr)
            self.__logger.setLevel(level=getattr(settings,
                                                 'LOGGER_LEVEL',
                                                 'WARN'))
        return self.__logger

    def get_commits(self):
        """Get all of the commits between self.old and self.new"""
        return get_commits(self.old, self.new, self.ref)

    def get_commit_messages(self):
        """Generator of commit messages for (self.old)..(self.new)
        Returns a tuple of (REV, commit_message)
        """
        return get_commit_messages(self.old, self.new, self.ref)

    def get_commit_author(self, commit):
        return get_commit_author(commit)

    def warning(self, txt):
        """Warning, display the warning message, but not reject"""
        self.logger.warning('\n%s\n' % txt)
        return True

    def error(self, txt):
        """Error, reject and display the error message"""
        self.logger.error('\n%s\n' % txt)
        return False
