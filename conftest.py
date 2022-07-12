import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def engine():
    return create_engine("postgresql://localhost/test_database")


class TestQuery(unittest.TestCase):

    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setUp(self):
        CarsModel.metadata.create_all(self.engine)
        self.session.add(Panel(1, 'ion torrent', 'start'))
        self.session.commit()

    def tearDown(self):
        CarsModel.metadata.drop_all(self.engine)
