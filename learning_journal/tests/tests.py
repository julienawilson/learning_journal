import pytest
import transaction

from pyramid import testing

from learning_journal.models import MyModel, get_tm_session

from learning_journal.models.meta import Base
from learning_journal.scripts.initializedb import ENTRIES

import faker
import datetime


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
    config.include("learning_journal.models")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture(scope="function")
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate a fake HTTP request."""
    the_request = testing.DummyRequest(dbsession=db_session)
    return the_request


FAKE = faker.Faker()

POSTS = [MyModel(
    title=FAKE.name(),
    date=str(datetime.datetime.now()),
    body=FAKE.text(100),
) for i in range(20)]


@pytest.fixture
def add_models(dummy_request):
    """Add fake model instances to the database."""
    dummy_request.dbsession.add_all(POSTS)


# --------- Database Tests ---------

def test_model_gets_added(db_session):
    """Test that a single entry gets added to the model."""
    assert len(db_session.query(MyModel).all()) == 0
    model = MyModel(title="A new post", body="A thing story")
    db_session.add(model)
    assert len(db_session.query(MyModel).all()) == 1


def test_all_models_get_added(db_session):
    """Test that all data from the list of data gets added to db."""
    for entry in ENTRIES:
        model = MyModel(title=entry['title'], date=entry['date'], day=entry['day'], body=entry['body'])
        db_session.add(model)
    query = db_session.query(MyModel)
    assert len(ENTRIES) == len(query.all())


def test_correct_data_get_added(db_session):
    """Test that the correct data gets added to db."""
    model = MyModel(title="Zoolander 2", date='today', day='115', body='this is the body')
    db_session.add(model)
    query = db_session.query(MyModel).first()
    assert query.title == 'Zoolander 2'


def test_edit_data_in_db(db_session):
    """Test that all data from the list of data gets added to db."""
    model = MyModel(title="Zoolander 2", date='today', day='115', body='this is the body')
    db_session.add(model)
    query = db_session.query(MyModel).first()
    assert query.title == 'Zoolander 2'
    query.title = 'An Extremely Goofy Movie'
    assert query.title == 'An Extremely Goofy Movie'


# --------- Unit Tests ---------

def test_new_entries_are_added(db_session, add_models):
    """New entries get added to the database."""
    # db_session.add_all()
    query = db_session.query(MyModel).all()
    assert len(query) == len(POSTS)


def test_home_page_nothing_when_empty(dummy_request):
    """My home page view returns some appropriate data."""
    from learning_journal.views.default import home_view
    response = home_view(dummy_request)
    assert len(response['ENTRIES']) == 0


def test_home_page_renders_file_data(dummy_request, add_models):
    """My home page view returns some appropriate data."""
    from learning_journal.views.default import home_view
    response = home_view(dummy_request)
    assert len(response['ENTRIES']) == 20


def test_detail_page_renders_file_data(dummy_request, add_models):
    """My detail page view returns some appropriate data."""
    from learning_journal.views.default import blog_view
    dummy_request.matchdict['id'] = '10'
    response = blog_view(dummy_request)['entry'].body
    assert response


def test_edit_page_renders_file_data(dummy_request, add_models):
    """My edit page view returns data from the approriate post."""
    from learning_journal.views.default import edit_view
    dummy_request.matchdict['id'] = '12'
    response = edit_view(dummy_request)['entry'].body
    assert response


# --------- Functional Tests ---------


@pytest.fixture
def testapp():
    """Create an instance of webtests TestApp for testing routes."""
    from webtest import TestApp
    from learning_journal import main

    app = main({}, **{"sqlalchemy.url": 'sqlite:///:memory:'})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    """Fill the database with some model instances."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)

        dbsession.add_all(POSTS)


def test_home_view_renders(testapp):
    """The home page has a table in the html."""
    response = testapp.get('/', status=200)
    html = str(response.html)
    some_text = "Learning Blog"
    assert some_text in html


def test_home_view_renders_data(testapp, fill_the_db):
    """The home page displays data from the database."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("h2")) == 21


def test_home_view_renders_correct_data(testapp, fill_the_db):
    """The home page displays the correct data from the database."""
    response = testapp.get('/', status=200)
    html = response.html
    assert html.find_all("h2")[1]
