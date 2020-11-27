from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.config import TableNames

Base = declarative_base()


class Review(Base):
    __tablename__ = TableNames.REVIEW

    id = Column(Integer, primary_key=True, autoincrement=True)
    album_id = Column(Integer, ForeignKey('album.id'))
    date = Column(Date)
    author = Column(String(255))
    rating = Column(Integer)
    content = Column(Text())

    album = relationship("Album", back_populates="reviews")


class MoodAlbum(Base):
    __tablename__ = TableNames.MOOD_ALBUM

    album_id = Column(Integer, ForeignKey('album.id'), primary_key=True)
    mood_id = Column(Integer, ForeignKey('mood.id'), primary_key=True)


class StyleAlbum(Base):
    __tablename__ = TableNames.STYLE_ALBUM

    album_id = Column(Integer, ForeignKey('album.id'), primary_key=True)
    style_id = Column(Integer, ForeignKey('style.id'), primary_key=True)


class ThemeAlbum(Base):
    __tablename__ = TableNames.THEME_ALBUM

    album_id = Column(Integer, ForeignKey('album.id'), primary_key=True)
    theme_id = Column(Integer, ForeignKey('theme.id'), primary_key=True)


class ArtistAlbum(Base):
    __tablename__ = TableNames.ARTIST_ALBUM

    album_id = Column(Integer, ForeignKey('album.id'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artist.id'), primary_key=True)


class ComposerTrack(Base):
    __tablename__ = TableNames.COMPOSER_TRACK

    track_id = Column(Integer, ForeignKey('track.id'), primary_key=True)
    composer_id = Column(Integer, ForeignKey('artist.id'), primary_key=True)


class Track(Base):
    __tablename__ = TableNames.TRACK

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    duration = Column(Integer)

    album_id = Column(Integer, ForeignKey('album.id'))
    album = relationship('Album', back_populates='tracks')

    composers = relationship("Artist", secondary=ComposerTrack.__tablename__, back_populates="tracks")


class Credit(Base):
    __tablename__ = TableNames.CREDIT

    id = Column(Integer, primary_key=True, autoincrement=True)

    album_id = Column(Integer, ForeignKey('album.id'))
    artist_id = Column(Integer, ForeignKey('artist.id'))
    role_id = Column(Integer, ForeignKey('role.id'))

    role = relationship('Role', back_populates='credits')
    album = relationship('Album', back_populates='credits')
    artist = relationship('Artist', back_populates='credits')


class Role(Base):
    __tablename__ = TableNames.ROLE
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    credits = relationship('Credit', back_populates='role')


class Album(Base):
    __tablename__ = TableNames.ALBUM

    id = Column(Integer, primary_key=True, autoincrement=True)
    reference_number = Column(String(255))
    title = Column(String(255))
    headline_review_author = Column(String(255))
    headline_review_content = Column(String(255))

    label_id = Column(Integer, ForeignKey('label.id'))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    review_body_id = Column(Integer, ForeignKey('review_body.id'))

    # One to Many
    label = relationship("Label", back_populates='albums')
    genre = relationship("Genre", back_populates="albums")

    # One to One
    review_body = relationship("ReviewBody", back_populates='album')

    # Many to Many
    moods = relationship("Mood", secondary=MoodAlbum.__tablename__, back_populates="albums")
    styles = relationship("Style", secondary=StyleAlbum.__tablename__, back_populates="albums")
    themes = relationship("Theme", secondary=ThemeAlbum.__tablename__, back_populates="albums")
    artists = relationship("Artist", secondary=ArtistAlbum.__tablename__, back_populates='albums')

    # Many to one
    reviews = relationship("Review", order_by=Review.id, back_populates="album")
    tracks = relationship("Track", order_by=Track.id, back_populates="album")
    credits = relationship("Credit", order_by=Credit.id, back_populates="album")

    __table_args__ = (UniqueConstraint('reference_number'),)


class Artist(Base):
    __tablename__ = TableNames.ARTIST

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    credits = relationship('Credit', back_populates='artist')

    albums = relationship("Album", secondary=ArtistAlbum.__tablename__, back_populates="artists")
    tracks = relationship('Track', secondary=ComposerTrack.__tablename__, back_populates='composers')

    __table_args__ = (UniqueConstraint('name'),)


class Label(Base):
    __tablename__ = TableNames.LABEL

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    albums = relationship("Album", back_populates="label")

    __table_args__ = (UniqueConstraint('name'),)


class ReviewBody(Base):
    __tablename__ = TableNames.REVIEW_BODY

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text())
    album = relationship("Album", back_populates="review_body")


class Mood(Base):
    __tablename__ = TableNames.MOOD

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255))
    albums = relationship("Album", secondary=MoodAlbum.__tablename__, back_populates='moods')

    __table_args__ = (UniqueConstraint('description'),)


class Theme(Base):
    __tablename__ = TableNames.THEME

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255))
    albums = relationship("Album", secondary=ThemeAlbum.__tablename__, back_populates='themes')

    __table_args__ = (UniqueConstraint('description'),)


class Style(Base):
    __tablename__ = TableNames.STYLE

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255))
    albums = relationship("Album", secondary=StyleAlbum.__tablename__, back_populates='styles')

    __table_args__ = (UniqueConstraint('description'),)


class Genre(Base):
    __tablename__ = TableNames.GENRE

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255))
    albums = relationship("Album", back_populates='genre')

    __table_args__ = (UniqueConstraint('description'),)
