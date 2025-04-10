import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from .models import Bank, Branch


class BankNode(DjangoObjectType):

    class Meta:
        model = Bank
        interfaces = (relay.Node, )
        fields = ['id', 'name', 'branches']
        filter_fields = ['id', 'name', 'branches']


class BranchNode(DjangoObjectType):

    class Meta:
        model = Branch
        interfaces = (relay.Node, )
        fields = ['id', 'ifsc', 'branch', 'address', 'city', 'district', 'state', 'bank']
        filter_fields = ['id', 'ifsc', 'branch', 'address', 'city', 'district', 'state', 'bank']
