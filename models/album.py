from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('mysql://username:password@host:port/database')
Base = declarative_base()


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True,  autoincrement=True)
    reference_number = Column(Integer)
    title = Column(String)
    artist_id = Column(Integer, ForeignKey('artist.id'))
    label_id = Column(Integer, ForeignKey('label.id'))
    headline_review_author = Column(String)
    artist = relationship("Artist")
    label = relationship("Label")
    reviews = relationship("Reviews")
    review_body = relationship("Review_Body", back_populates="albums")
    moods = relationship("Mood", secondary='link')


class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class Label(Base):
    __tablename__ = 'label'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Reviews(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    album_id = Column(Integer, ForeignKey('album.id'))
    date = Column(Date)
    author = Column(String)
    rating = Column(Integer)


class Tracks(Base):
    __tablename__ = 'tracks_album'

    album_id = Column(Integer, ForeignKey('album.id'))
    title = Column(String)
    duration = Column(Integer)


class Credits(Base):
    __tablename__ = 'credits_album'

    album_id = Column(Integer, ForeignKey('album.id'))
    artist = Column(String)
    role = Column(String)


class ReviewBody(Base):
    __tablename__ = 'review_body'

    album_id = Column(Integer, ForeignKey('album.id'))
    content = Column(String)
    albums = relationship("Album", back_populates="review_body", uselist=False)


class Moods(Base):
    __tablename__ = 'moods'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    albums = relationship("Album", secondary='link')


class MoodAlbum(Base):
    __tablename__ = 'mood_album'

    album_id = Column(Integer, ForeignKey('album.id'), primary_key=True)
    mood_id = Column(Integer, ForeignKey('moods.id'), primary_key=True)


class Themes(Base):
    __tablename__ = 'themes'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    albums = relationship("Album", secondary='link')


class ThemeAlbum(Base):
    __tablename__ = 'themes_album'

    album_id = Column(Integer, ForeignKey('album.id'), primary_key=True)
    theme_id = Column(Integer, ForeignKey('themes.id'), primary_key=True)


class Styles(Base):
    __tablename__ = 'styles'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    albums = relationship("Album", secondary='link')


class StylesAlbum(Base):
    __tablename__ = 'styles_album'

    album_id = Column(Integer, ForeignKey('album.id'), primary_key=True)
    style_id = Column(Integer, ForeignKey('styles.id'), primary_key=True)
