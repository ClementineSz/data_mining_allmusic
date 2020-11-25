from sqlalchemy import create_engine, ForeignKey, Table, UniqueConstraint
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()


# https://stackoverflow.com/questions/5756559/how-to-build-many-to-many-relations-using-sqlalchemy-a-good-example
# https://stackoverflow.com/questions/18022326/sqlalchemy-insert-many-to-one-entries

class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, autoincrement=True)
    album_id = Column(Integer, ForeignKey('album.id'))
    date = Column(Date)
    author = Column(String)
    rating = Column(Integer)
    content = Column(String)

    album = relationship("Album", back_populates="reviews")


#
#
class MoodAlbum(Base):
    __tablename__ = 'mood_album'

    album_id = Column(Integer, ForeignKey('album.id'), primary_key=True)
    mood_id = Column(Integer, ForeignKey('mood.id'), primary_key=True)


#
#
class StyleAlbum(Base):
    __tablename__ = 'style_album'

    album_id = Column(Integer, ForeignKey('album.id'), primary_key=True)
    style_id = Column(Integer, ForeignKey('style.id'), primary_key=True)


class ThemeAlbum(Base):
    __tablename__ = 'theme_album'

    album_id = Column(Integer, ForeignKey('album.id'), primary_key=True)
    theme_id = Column(Integer, ForeignKey('theme.id'), primary_key=True)


class Track(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    duration = Column(Integer)

    album_id = Column(Integer, ForeignKey('album.id'))
    album = relationship('Album', back_populates='tracks')


class Credit(Base):
    __tablename__ = 'credit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    album_id = Column(Integer, ForeignKey('album.id'))
    artist = Column(String)
    role = Column(String)

    album = relationship('Album', back_populates='credits')


class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reference_number = Column(Integer)
    title = Column(String)
    headline_review_author = Column(String)
    headline_review_content = Column(String)

    artist_id = Column(Integer, ForeignKey('artist.id'))
    label_id = Column(Integer, ForeignKey('label.id'))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    review_body_id = Column(Integer, ForeignKey('review_body.id'))

    # One to Many
    artist = relationship("Artist", back_populates='albums')
    label = relationship("Label", back_populates='albums')
    genre = relationship("Genre", back_populates="albums")

    # One to One
    review_body = relationship("ReviewBody", back_populates='album')

    # Many to Many
    moods = relationship("Mood", secondary=MoodAlbum.__tablename__, back_populates="albums")
    styles = relationship("Style", secondary=StyleAlbum.__tablename__, back_populates="albums")
    themes = relationship("Theme", secondary=ThemeAlbum.__tablename__, back_populates="albums")

    # Many to one
    reviews = relationship("Review", order_by=Review.id, back_populates="album")
    tracks = relationship("Track", order_by=Track.id, back_populates="album")
    credits = relationship("Credit", order_by=Credit.id, back_populates="album")

    __table_args__ = (UniqueConstraint('reference_number'),)


class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    albums = relationship("Album", back_populates="artist")

    __table_args__ = (UniqueConstraint('name'),)


class Label(Base):
    __tablename__ = 'label'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    albums = relationship("Album", back_populates="label")

    __table_args__ = (UniqueConstraint('name'),)


class ReviewBody(Base):
    __tablename__ = 'review_body'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)
    album = relationship("Album", back_populates="review_body")


class Mood(Base):
    __tablename__ = 'mood'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    albums = relationship("Album", secondary=MoodAlbum.__tablename__, back_populates='moods')

    __table_args__ = (UniqueConstraint('description'),)


class Theme(Base):
    __tablename__ = 'theme'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    albums = relationship("Album", secondary=ThemeAlbum.__tablename__, back_populates='themes')

    __table_args__ = (UniqueConstraint('description'),)


class Style(Base):
    __tablename__ = 'style'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    albums = relationship("Album", secondary=StyleAlbum.__tablename__, back_populates='styles')

    __table_args__ = (UniqueConstraint('description'),)


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    albums = relationship("Album", back_populates='genre')

    __table_args__ = (UniqueConstraint('description'),)
