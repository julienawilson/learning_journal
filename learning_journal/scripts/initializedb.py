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


ENTRIES = [
    {"title": "Like the rest of the week, but at a mortal pace.",
     "day": '14',
     "date": "December 212, 2016",
     "body": "Two big events today.  The first was that we (as a class) backtracked a little bit to review the pyramid flow.  This was very helpful.  I felt like we could see the whole picture and mostly knew all of the parts that were needed.  I'm still not solid on testing in pyramid.  But I'm working on it and I think I'll get there soon.  GerryPy spent abotu 2.5 hours today laying the groundwork for our strategy.  The first step in making our project a reality is a big one.  The algorithm is complex and we're not totally sure that we have all of the tools to make it possible.  The edge cases are also a pretty big issue.  If we can make it work though, I think we'll all be very proud.  Each person on the team has a different strength they're bringing to the table, and I think we can really take advantage of that.  I'm glad we have as much time as we do before presentation day.  We'll use it."},
    {"title": "Winter Solstice",
     "day": '13',
     "date": "December 21, 2016",
     "body": "Winter Solstice.  Today felt really hard.  The data structure felt more complicated than usual and the pyramid work was difficult to navigate.  I dont think the pyramid material is THAT difficult to understand, but its easy to lose track of where you are/what you've done/whats left to do.  There are lots of places to miss the connections.  The stress of today made it harder to learn.  The amount of work, and the feeling that you will always be behind, and usually not really learn the material, is becoming pretty disheartening."},
    {"title": "Starting out Final Projects",
     "day": '12',
     "date": "December 20, 2016",
     "body": "Big news today was finalizing projects and getting our groups.  I'm pretty excited to see how all of the projects pan out.  I think they're all pretty ambitious.  Lecture this morning was challenging.  A lot of new material that seemed daunting.  The bin heap was hard.  I think Patrick and I benefited some lots of diagramming.  I think that might be the key to these daa structures.  Also reading the instructions carefully. I tend to make mistakes there.  The pyramid stuff today felt satisfying once we got it working.  It feels like a real website... almost.      Part 2:  I just finished a debugging effort, which led me through the pyramid debugger toolbar, into the filter function (and its diferences in py2 and py3) some other steps.  None of these solutions fixed my problem, but I learned a lot about other things."},
    {"title": "Day 11 - Heroku seemed easier last time",
     "day": '11',
     "date": "December 19, 2016",
     "body": "My main accomplishment today was debugging Heroku. My initial push (and my second attempt) failed, but I was able to read the errror messages and figure out what was going on.  I moved some files around and was able to make it work.  Generally, one of the things I've learned the most about in this class is reading error messages and figuring out how to fix them. Besides that, we presented ideas today.  Despite almost nobody having any ideas 5 minutes before the meeting, there were A LOT of great ideas.  I think people are thinking big.  Would be excited to work on a number of them. Data Structures are starting to feel more natural.  The Deque wasnt too tough today.  I've heard the heap is a little more exciting.  We'll see what that brings tomorrow."},
    {"title": "Start Bootstrap",
     "day": '10',
     "date": "today",
     "body": "learned stuff again"},
    {"title": "post3",
     "day": '9',
     "date": "today",
     "body": "learned stuff again again"},
]


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
    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    # with transaction.manager:
    #     dbsession = get_tm_session(session_factory, transaction.manager)

    #     for entry in ENTRIES:
    #         model = MyModel(title=entry['title'], date=entry['date'], day=entry['day'], body=entry['body'])
    #         dbsession.add(model)
