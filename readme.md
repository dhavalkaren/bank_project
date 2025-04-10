# Bank GraphQL API

## 📌 Overview
This project implements a GraphQL API server using Django and Graphene that provides access to bank and branch data
that is imported from [Bank & Branch Data Repository](https://github.com/Amanskywalker/indian_banks). 
The API supports both querying all branches and filtering branches.

The GraphQL endpoint is available at:
```
/gql
```

## ✅ Features
- `/gql` endpoint for GraphQL queries.
- Query all bank branches and their associated banks.
- Filter branches by `id`, `ifsc`, `branch`, `address`, `city`, `district`, `state`, `bank` code.
- Relay-compatible GraphQL structure (`edges` and `node`).
- Clean, modular Django project structure.
- SQLite for deployment.


---

## 🚀 How It Works

### 📘 Models
- `Bank`: stores the bank name
- `Branch`: stores IFSC, branch name, address, location, and FK to bank

### 🧠 GraphQL Schema
- `BranchNode` and `BankNode` implement Relay interfaces.
- Relay-style `branches` field supports filtering:

```python
class Query(ObjectType):
    bank = relay.Node.Field(BankNode)
    branch = relay.Node.Field(BranchNode)

    banks = DjangoFilterConnectionField(BankNode)
    branches = DjangoFilterConnectionField(BranchNode)
```

### 📥 Example Query
```graphql
query {
  branches(ifsc: "ABHY0065060") {
    edges {
      node {
        ifsc
        branch
        bank {
          name
        }
      }
    }
  }
}
```

---

## ▶️ Running Locally

```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```
```bash
python manage.py migrate
```
```bash
python manage.py runserver
```
Then open: `http://127.0.0.1:8000/gql`

---

## ✅ Running Tests

```bash
python manage.py test
```

---

## ⏱ Time Taken for this Assignment
~3-4 hours

---
