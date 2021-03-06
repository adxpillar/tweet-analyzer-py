
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Boolean, DateTime, ARRAY, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", default="postgresql://username:password@localhost/dbname")
USER_FRIENDS_TABLE_NAME = os.getenv("USER_FRIENDS_TABLE_NAME", default="user_friends") # can customize different sizes, like "user_friends_10k", for testing
USER_DETAILS_TABLE_NAME = os.getenv("USER_DETAILS_TABLE_NAME", default="user_details")
RETWEETER_DETAILS_TABLE_NAME = os.getenv("RETWEETER_DETAILS_TABLE_NAME", default="retweeter_details")

db = create_engine(DATABASE_URL)
Base = declarative_base()
Base.metadata.bind = db # fixes sqlalchemy.exc.UnboundExecutionError: Table object 'books' is not bound to an Engine or Connection.  Execution can not proceed without a database to execute against.
BoundSession = sessionmaker(bind=db)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    author = Column(String(128))
    readers = Column(ARRAY(String(128)))

class UserFriend(Base):
    __tablename__ = USER_FRIENDS_TABLE_NAME
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger) # , primary_key=True
    screen_name = Column(String(128))
    friend_count = Column(Integer)
    friend_names = Column(ARRAY(String(128)))

class UserDetail(Base):
    __tablename__ = USER_DETAILS_TABLE_NAME
    user_id = Column(BigInteger, primary_key=True)

    screen_name = Column(String(50))
    name        = Column(String(150))
    description = Column(String(250))
    location    = Column(String(150))
    verified    = Column(Boolean)
    created_at  = Column(TIMESTAMP)

    screen_name_count = Column(Integer)
    name_count        = Column(Integer)
    description_count = Column(Integer)
    location_count    = Column(Integer)
    verified_count    = Column(Integer)
    created_count     = Column(Integer)

    screen_names  = Column(ARRAY(String(50)))
    names         = Column(ARRAY(String(150)))
    descriptions  = Column(ARRAY(String(250)))
    locations     = Column(ARRAY(String(150)))
    verifieds     = Column(ARRAY(Boolean))
    created_ats   = Column(ARRAY(TIMESTAMP))

    friend_count            = Column(Integer)

    status_count            = Column(Integer)
    retweet_count           = Column(Integer)

    # # these topics are specific to the impeachment dataset, so will need to generalize if/when working with another topic (leave for future concern)
    # impeach_and_convict     = Column(Integer)
    # senate_hearing          = Column(Integer)
    # ig_hearing              = Column(Integer)
    # facts_matter            = Column(Integer)
    # sham_trial              = Column(Integer)
    # maga                    = Column(Integer)
    # acquitted_forever       = Column(Integer)

class RetweeterDetail(Base):
    __tablename__ = RETWEETER_DETAILS_TABLE_NAME
    user_id = Column(BigInteger, primary_key=True)

    created_at = Column(TIMESTAMP)
    screen_name_count = Column(Integer)
    name_count = Column(Integer)

    retweet_count           = Column(Integer)
    # # these topics are specific to the impeachment dataset, so will need to generalize if/when working with another topic (leave for future concern)
    # ig_report               = Column(Integer)
    # ig_hearing              = Column(Integer)
    # senate_hearing          = Column(Integer)
    # not_above_the_law       = Column(Integer)
    # impeach_and_convict     = Column(Integer)
    # impeach_and_remove      = Column(Integer)
    # facts_matter            = Column(Integer)
    # sham_trial              = Column(Integer)
    # maga                    = Column(Integer)
    # acquitted_forever       = Column(Integer)
    # country_over_party      = Column(Integer)





if __name__ == "__main__":

    #breakpoint()
    #Book.__table__.drop(db)
    #Book.__table__.create(db)
    #if not Book.__table__.exists(): Book.__table__.create(db)
    #if not UserFriend.__table__.exists(): UserFriend.__table__.create(db)
    Base.metadata.create_all(db)

    session = BoundSession()

    try:
        book = session.query(Book).filter(Book.title=="Harry Potter").one()
    except NoResultFound as err:
        book = Book(title="Harry Potter", author="JKR", readers=["John", "Jane", "Sally"])
        session.add(book)
        session.commit()

    print("-------")
    print("BOOKS:")
    books = session.query(Book)
    for book in books:
        print("...", book.id, "|", book.title, "|", book.author, "|", book.readers)

    print("-------")
    print("USER FRIENDS:")
    results = db.execute(f"SELECT count(DISTINCT screen_name) as row_count FROM {USER_FRIENDS_TABLE_NAME};")
    #print(results.keys()) #> ["row_count"]
    #print(results.rowcount) #> 1
    print("...", results.fetchone()[0]) #TODO: row factory ... results.fetchone()["row_count"]

    print("-------")
    print("USER DETAILS:")
    results = db.execute(f"SELECT count(DISTINCT screen_name) as row_count FROM {USER_DETAILS_TABLE_NAME};")
    #print(results.keys()) #> ["row_count"]
    #print(results.rowcount) #> 1
    print("...", results.fetchone()[0]) #TODO: row factory ... results.fetchone()["row_count"]


    session.close()
