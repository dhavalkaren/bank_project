from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from banks.models import Bank, Branch

faker = Factory.create()


class BankFactory(DjangoModelFactory):
    class Meta:
        model = Bank

    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))


class BranchFactory(DjangoModelFactory):
    class Meta:
        model = Branch

    bank = factory.SubFactory('banks.tests.factories.BankFactory')
    ifsc = LazyAttribute(lambda o: faker.text(max_nb_chars=11))
    branch = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    address = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    city = LazyAttribute(lambda o: faker.text(max_nb_chars=50))
    district = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    state = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
