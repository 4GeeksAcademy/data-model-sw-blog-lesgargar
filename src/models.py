from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, ForeignKey, List

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    characters: Mapped[List["Character"]] = relationship(
        back_populates="origin_planet")


class Character(db.Model):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    about: Mapped[str] = mapped_column(Text, nullable=False)

    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=False)
    origin_planet: Mapped["Planet"] = relationship(back_populates="characters")


class Favorite_planet(db.model):
    __tablename__ = "favorite_planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id"), nullable=False)  # referenciado al user id
    # referenciado al planet id de la tabla planets
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=False)

    user: Mapped["User"] = relationship(
        back_populates="favorite_planets")  # relacion con el usuario
    planet: Mapped["Planet"] = relationship()  # relacion del planet


class Favorite_charachters(db.model):
    __tablename__ = "favorite_characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorite_characters")
    character: Mapped["Character"] = relationship()
