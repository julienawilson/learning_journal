import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import MyModel


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    entries = [
        {"title": "Starting out Final Projects",
         "id": '12',
         "date": "December 20, 2016",
         "body": "Big news today was finalizing projects and getting our groups.  I'm pretty excited to see how all of the projects pan out.  I think they're all pretty ambitious.  Lecture this morning was challenging.  A lot of new material that seemed daunting.  The bin heap was hard.  I think Patrick and I benefited some lots of diagramming.  I think that might be the key to these daa structures.  Also reading the instructions carefully. I tend to make mistakes there.  The pyramid stuff today felt satisfying once we got it working.  It feels like a real website... almost.      Part 2:  I just finished a debugging effort, which led me through the pyramid debugger toolbar, into the filter function (and its diferences in py2 and py3) some other steps.  None of these solutions fixed my problem, but I learned a lot about other things."},
        {"title": "Day 11 - Heroku seemed easier last time",
         "id": '11',
         "date": "December 19, 2016",
         "body": "My main accomplishment today was debugging Heroku. My initial push (and my second attempt) failed, but I was able to read the errror messages and figure out what was going on.  I moved some files around and was able to make it work.  Generally, one of the things I've learned the most about in this class is reading error messages and figuring out how to fix them. Besides that, we presented ideas today.  Despite almost nobody having any ideas 5 minutes before the meeting, there were A LOT of great ideas.  I think people are thinking big.  Would be excited to work on a number of them. Data Structures are starting to feel more natural.  The Deque wasnt too tough today.  I've heard the heap is a little more exciting.  We'll see what that brings tomorrow."},
        {"title": "Start Bootstrap",
         "id": '10',
         "date": "today",
         "body": "learned stuff again"},
        {"title": "post3",
         "id": '9',
         "date": "today",
         "body": "learned stuff again again"},
    ]

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for entry in entries:
            model = MyModel(title=entry['title'], date=entry['date'], body=entry['body'])
            dbsession.add(model)
