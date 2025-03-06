#!/usr/bin/env python

people = [
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Cho", "house": "Ravenclaw"},
    {"name": "Draco", "house": "Slytherin"},
]


def f(person):
    return person["name"]


people.sort(key=f)

print(people)


people.sort(key=lambda person: person["name"])
# lambda is function that takes <input> and returns : <output>
# this is equivalent to people.sort(key=f)
