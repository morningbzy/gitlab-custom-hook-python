
import os


def __get_opts(old, new, ref):
    return {'old': old, 'new': new, 'ref': ref}


def get_commits(old, new, ref):
    """Get all of the commits between old and new

    If creating a new branch (i.e. old is '0000000'), return the whole commit list on this branch
    If deleting a branch (i.e. new is '0000000'), return []
    """
    ZERO = '0000000'
    opts = __get_opts(old, new, ref)

    # Deleting branch
    if new.startswith(ZERO):
        return []
    # Creating branch
    elif old.startswith(ZERO):
        cmd = """git rev-list $(git for-each-ref --format='%%(refname)' refs/heads/** | grep -x -v '%(ref)s' | sed 's/^/\^/') %(new)s""" % opts
    else:
        cmd = """git rev-list %(old)s..%(new)s""" % opts

    return os.popen(cmd).readlines()


def get_commit_messages(old, new, ref):
    """Generator of commit messages for old..new
    Returns a tuple of (REV, commit_message)
    """
    for commit in get_commits(old, new, ref):
        commit = commit.strip()
        cmd = "git cat-file commit %s | sed '1,/^$/d'" % commit
        yield commit, ''.join(os.popen(cmd).readlines())


def get_commit_author(commit):
    cmd = '''git show %s --pretty="%%an"''' % commit
    return os.popen(cmd).readlines()[0].strip()
