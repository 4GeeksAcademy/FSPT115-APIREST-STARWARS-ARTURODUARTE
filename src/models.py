from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

favorites_planets = Table(
    "favorites_planets",
    db.Model.metadata,
    Column("left_id", ForeignKey("users.id")),
    Column("right_id", ForeignKey("planets.id"))
)
favorites_people = Table(
    "favorites_people",
    db.Model.metadata,
    Column("left_id", ForeignKey("users.id")),
    Column("right_id", ForeignKey("people.id"))
)

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    #relationships

    favorites_planets: Mapped[List["Planet"]] = relationship(
        "Planet",
        secondary=favorites_planets,
        back_populates="favorites_planets_by"
    )
    favorites_people: Mapped[List["People"]] = relationship(
        "People",
        secondary=favorites_people,
        back_populates="favorites_people_by"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_people": [people.serialize() for people in self.favorites_people],
            "favorite_planet": [planet.serialize() for planet in self.favorites_planets]
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    image_url: Mapped[str] = mapped_column(String(120), nullable= False)

    #relationship
    favorites_people_by: Mapped[List[User]] = relationship(
        "User",
        secondary=favorites_people,
        back_populates="favorites_people"
    )


    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url
        }


class Planet(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    image_url: Mapped[str] = mapped_column(String(120), nullable= False)

    #relationship
    favorites_planets_by: Mapped[List[User]] = relationship(
        "User",
        secondary=favorites_planets,
        back_populates="favorites_planets"
    )    
    
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "image_url": self.image_url
        }        
    