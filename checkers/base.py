
import os
import logging

import settings


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
        """Get all of the commits between self.old and self.new

        If creating a new branch (i.e. old is '0000000'), return the whole commit list on this branch
        If deleting a branch (i.e. new is '0000000'), return []
        """
        ZERO = '0000000'

        # Deleting branch
        if self.new.startswith(ZERO):
            return []
        # Creating branch
        elif self.old.startswith(ZERO):
            cmd = """git rev-list $(git for-each-ref --format='%%(refname)' refs/heads/** | grep -x -v '%(ref)s' | sed 's/^/\^/') %(new)s""" % self.opts
        else:
            cmd = """git rev-list %(old)s..%(new)s""" % self.opts

        self.logger.debug('Executing: %s' % cmd)
        return os.popen(cmd).readlines()

    def get_commit_messages(self):
        """Generator of commit messages for (self.old)..(self.new)
        Returns a tuple of (REV, commit_message)
        """
        for commit in self.get_commits():
            commit = commit.strip()
            cmd = "git cat-file commit %s | sed '1,/^$/d'" % commit
            yield commit, ''.join(os.popen(cmd).readlines())

    def get_commit_author(self, commit):
        cmd = '''git show %s --pretty="%%an"''' % commit
        return os.popen(cmd).readlines()[0].strip()

    def warning(self, txt):
        """Warning, display the warning message, but not reject"""
        self.logger.warning('\n%s\n' % txt)
        return True

    def error(self, txt):
        """Error, reject and display the error message"""
        self.logger.error('\n%s\n' % txt)
        return False
