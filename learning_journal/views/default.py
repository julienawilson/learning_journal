"""Views for the Learning Journal App."""

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel
import datetime
from pyramid.httpexceptions import HTTPFound

from learning_journal.security import check_credentials

from pyramid.security import remember, forget
from pyramid.session import check_csrf_token


@view_config(route_name='home', renderer='../templates/posts.jinja2')
def home_view(request):
    if request.method == "GET":
        try:
            query = request.dbsession.query(MyModel)
            entries = query.all()[::-1]
        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)
        return {'ENTRIES': entries}

    if request.method == "POST":
        print("poting method")
        new_title = request.POST['title']
        new_body = request.POST['body']
        new_date = str(datetime.datetime.now().date())

        model = MyModel(title=new_title, date=new_date, body=new_body)
        print("done creating model")
        request.dbsession.add(model)
        print("posted model")
        return {}
        # return HTTPFound(request.route_url("home"))


@view_config(route_name='blog', renderer='../templates/detail.jinja2')
def blog_view(request):
    try:
        query = request.dbsession.query(MyModel)
        entry = query.filter(MyModel.id == request.matchdict["id"]).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'entry': entry}


@view_config(
    route_name='new',
    renderer='../templates/new_post_template.jinja2',
    permission='add'
)
def create_view(request):
    if request.method == "POST":
        new_title = request.POST['title']
        new_body = request.POST['body']
        new_date = str(datetime.datetime.now().date())

        model = MyModel(title=new_title, date=new_date, body=new_body)
        request.dbsession.add(model)

        return HTTPFound(request.route_url("home"))
    return{}


@view_config(
    route_name='edit',
    renderer='../templates/update_post_template.jinja2',
    permission='add'
)
def edit_view(request):
    the_id = request.matchdict["id"]
    try:
        query = request.dbsession.query(MyModel)
        entry = query.filter_by(id=the_id).first()

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


@view_config(route_name='login', renderer="../templates/login_template.jinja2")
def login_view(request):
    """View to login user."""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            auth_head = remember(request, username)
            return HTTPFound(
                request.route_url("home"),
                headers=auth_head)

    return {}


@view_config(route_name='logout')
def logout(request):
    """View to logout user."""
    auth_head = forget(request)
    return HTTPFound(request.route_url('home'), headers=auth_head)


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
