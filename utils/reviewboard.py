
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
