from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from .types import BankNode, BranchNode


class Query(ObjectType):
    bank = relay.Node.Field(BankNode)
    branch = relay.Node.Field(BranchNode)

    banks = DjangoFilterConnectionField(BankNode)
    branches = DjangoFilterConnectionField(BranchNode)

