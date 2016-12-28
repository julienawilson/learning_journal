from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel
import datetime
from pyramid.httpexceptions import HTTPFound


@view_config(route_name='home', renderer='../templates/posts.jinja2')
def home_view(request):
    import pdb; pdb.set_trace()
    try:
        entries = request.dbsession.query(MyModel).all()
        # entries = query.all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'ENTRIES': entries}


@view_config(route_name='blog', renderer='../templates/detail.jinja2')
def blog_view(request):
    try:
        query = request.dbsession.query(MyModel)
        entry = query.filter(MyModel.id == request.matchdict["id"]).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'entry': entry}


@view_config(route_name='new', renderer='../templates/new_post_template.jinja2')
def create_view(request):
    if request.method == "POST":
        new_title = request.POST['title']
        new_body = request.POST['body']
        new_date = str(datetime.datetime.now().date())

        model = MyModel(title=new_title, date=new_date, body=new_body)
        request.dbsession.add(model)

        return HTTPFound(request.route_url("home"))
    return{}


@view_config(route_name='edit', renderer='../templates/update_post_template.jinja2')
def edit_view(request):
    the_id = request.matchdict["id"]
    try:
        query = request.dbsession.query(MyModel)
        entry = query.filter(MyModel.id == the_id).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

    if request.method == "POST":
        new_title = request.POST['title']
        new_body = request.POST['body']
        new_date = str(datetime.datetime.now().date())

        model = request.dbsession.query(MyModel).get(the_id)

        model.title = new_title
        model.body = new_body
        model.date = new_date

        return HTTPFound(request.route_url("home"))
    return {'entry': entry}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
