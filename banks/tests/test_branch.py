import json

from faker import Factory
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import to_global_id

from banks.models import Branch
from banks.types import BranchNode

from .factories import BranchFactory

faker = Factory.create()


class TestBranch(GraphQLTestCase):
    def setUp(self):
        self.GRAPHQL_URL = "/gql"
        BranchFactory.create_batch(size=3)


    def test_fetch_all(self):
        """
        fetch all using branches query and check that the 3 objects are returned following
        Relay standards.
        """
        response = self.query(
            """
            query {
                branches{
                    edges{
                        node{
                            id
                            ifsc
                            branch
                            address
                            city
                            district
                            state
                        }
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        branch_list = content['data']['branches']['edges']
        branch_list_qs = Branch.objects.all()
        for i, edge in enumerate(branch_list):
            branch = edge['node']
            self.assertEqual(branch['id'], to_global_id(
                BranchNode._meta.name, branch_list_qs[i].id))
            self.assertEqual(branch['ifsc'], branch_list_qs[i].ifsc)
            self.assertEqual(branch['branch'], branch_list_qs[i].branch)
            self.assertEqual(branch['address'], branch_list_qs[i].address)
            self.assertEqual(branch['city'], branch_list_qs[i].city)
            self.assertEqual(branch['district'], branch_list_qs[i].district)
            self.assertEqual(branch['state'], branch_list_qs[i].state)

    def test_fetch_branch_with_bank(self):
        """
        Fetch all branches and ensure each branch includes associated bank data.
        """
        response = self.query(
            """
            query {
                branches {
                    edges {
                        node {
                            id
                            ifsc
                            branch
                            address
                            city
                            district
                            state
                            bank {
                                id
                                name
                            }
                        }
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        branch_list = content['data']['branches']['edges']
        branch_list_qs = Branch.objects.select_related('bank').all()

        for i, edge in enumerate(branch_list):
            branch = edge['node']
            branch_obj = branch_list_qs[i]

            self.assertEqual(branch['id'], to_global_id(BranchNode._meta.name, branch_obj.id))
            self.assertEqual(branch['ifsc'], branch_obj.ifsc)
            self.assertEqual(branch['branch'], branch_obj.branch)
            self.assertEqual(branch['address'], branch_obj.address)
            self.assertEqual(branch['city'], branch_obj.city)
            self.assertEqual(branch['district'], branch_obj.district)
            self.assertEqual(branch['state'], branch_obj.state)

            self.assertIsNotNone(branch['bank'])
            self.assertEqual(branch['bank']['id'], to_global_id("BankNode", branch_obj.bank.id))
            self.assertEqual(branch['bank']['name'], branch_obj.bank.name)