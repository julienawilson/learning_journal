import pytest
import transaction

from pyramid import testing

from learning_journal.models import (
    MyModel,
    get_tm_session,
)
from learning_journal.models.meta import Base
from learning_journal.scripts.initializedb import ENTRIES


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
    """Test that all data from the list of data gets added to db."""
    model = MyModel(title="Title", date='today', day='115', body='this is the body')
    db_session.add(model)
    query = db_session.query(MyModel).first()
    assert query.title == 'Title'
