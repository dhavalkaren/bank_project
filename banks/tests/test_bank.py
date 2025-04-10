import json
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import to_global_id

from banks.models import Bank
from banks.types import BankNode
from .factories import BankFactory


class TestBank(GraphQLTestCase):
    def setUp(self):
        self.GRAPHQL_URL = "/gql"
        self.banks = BankFactory.create_batch(size=3)

    def test_fetch_all_banks(self):
        """
        Fetch all banks using allBank query and validate the response.
        """
        response = self.query(
            """
            query {
                banks {
                    edges {
                        node {
                            id
                            name
                        }
                    }
                }
            }
            """
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        banks_from_response = content['data']['banks']['edges']
        banks_from_db = Bank.objects.all()

        self.assertEqual(len(banks_from_response), banks_from_db.count())

        for i, edge in enumerate(banks_from_response):
            bank_node = edge['node']
            db_bank = banks_from_db[i]

            self.assertEqual(bank_node['id'], to_global_id(BankNode._meta.name, db_bank.id))
            self.assertEqual(bank_node['name'], db_bank.name)
