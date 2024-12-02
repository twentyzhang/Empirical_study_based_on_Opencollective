import requests
import timeModel
import redis
import json
from pymongo import MongoClient

r = redis.StrictRedis(host='localhost', port=6379, db=0)
cli = MongoClient('localhost', 27017)
db = cli['oc']
collection = db['data']

# OpenCollective API URL
url = "https://api.opencollective.com/graphql/v2"

token = "f448ae7ff711ab4653ccf393676d2c9e77662368"

# GraphQL query template
base_query = """
query CollectiveData($slug: String!) {
  collective(slug: $slug) {
    id
    name
    slug
    description
    currency
    expensePolicy
    isIncognito
    createdAt
    updatedAt
    socialLinks {
      type
      url
    }
  }
}
"""

member_query = """
query CollectiveData(
    $slug: String!
    $limit: Int!
    $offset: Int!
    $role: [MemberRole]!
  ) {
  collective(slug: $slug) {
    members(
      limit: $limit
      offset: $offset
      role: $role
    ) {
      totalCount
      nodes {
        id
        role
        totalDonations {
          value
          currency
        }
        publicMessage
        description
        inherited
        account {
          id
          slug
          description
          location {
            address
            country
          }
          socialLinks {
            type
            url
          }
        }
      }
    }
  }
}
"""

transaction_query = """
query CollectiveData(
    $slug: String!
    $limit: Int!
    $offset: Int!
  ) {
  collective(slug: $slug) {
    transactions(
      limit: $limit
      offset: $offset
    ) {
      totalCount
      nodes {
        id
        type
        kind
        amount {
          value
          currency
        }
        createdAt
        description
        order {
          id
          description
          taxAmount {
            value
            currency
          }
          totalAmount {
            value
            currency
          }
          frequency
          hostFeePercent
          platformTipAmount {
            value
            currency
          }
        }
      }
    }
  }
}
"""

conversation_query = """
query CollectiveData(
    $slug: String!
    $limit: Int!
    $offset: Int!
  ) {
  collective(slug: $slug) {
    conversations(
      limit: $limit
      offset: $offset
    ) {
      totalCount
      nodes {
        id
        title
        createdAt
        updatedAt
        tags
        summary
      }
    }
  }
}
"""

# Headers for the request
headers = {
    "Personal-Token": f"{token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, object):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def fetch_base_data(slug):
    variables = {"slug": slug}
    while True:
      try:
          response = requests.post(url, headers=headers, json={'query': base_query, 'variables': variables})
          if response.status_code == 200:
              return response.json()
          else:
              print(f"Error when fetching base data, retrying {slug}")
              time.sleep(1)
      except:
          print(f"Error when fetching base data, retrying {slug}")
          time.sleep(1)
        
def fetch_members_data(slug):
    page = 1
    result = []
    while True:
      variables = {"slug": slug, "limit": 1000, "offset": 1000 * (page - 1), "role": ["FOLLOWER", "BACKER", "CONTRIBUTOR", "ADMIN", "HOST", "MEMBER"]}
      try:
        response = requests.post(url, headers=headers, json={'query': member_query, 'variables': variables})
        data = response.json()
        if 'errors' in data:
            print(f"Fail to fetch {slug}")
            r.sadd('not_done', slug)
            return None
        if response.status_code == 200:
            result += data['data']['collective']['members']['nodes']
            if page * 1000 >= data['data']['collective']['members']['totalCount']:
                return result
            else:
                page += 1
        else:
            print(data)
            print(f"Error when fetching members data, retrying {slug}")
            time.sleep(1)
      except:
        print(f"Error when fetching members data, retrying {slug}")
        time.sleep(1)
      
def fetch_transactions_data(slug):
    page = 1
    result = []
    while True:
      variables = {"slug": slug, "limit": 1000, "offset": 1000 * (page - 1)}
      try:
        response = requests.post(url, headers=headers, json={'query': transaction_query, 'variables': variables})
        data = response.json()
        if response.status_code == 200:
            data = response.json()
            result += data['data']['collective']['transactions']['nodes']
            if page * 1000 >= data['data']['collective']['transactions']['totalCount']:
                return result
            else:
                page += 1
        else:
            print(data)
            print(f"Error when fetching transaction data, retrying {slug}")
            time.sleep(1)
      except:
        print(f"Error when fetching transaction data, retrying {slug}")
        time.sleep(1)
      
def fetch_conversations_data(slug):
    page = 1
    result = []
    while True:
      variables = {"slug": slug, "limit": 1000, "offset": 1000 * (page - 1)}
      try:
        response = requests.post(url, headers=headers, json={'query': conversation_query, 'variables': variables})
        data = response.json()
        if response.status_code == 200:
            data = response.json()
            result += data['data']['collective']['conversations']['nodes']
            if page * 1000 >= data['data']['collective']['conversations']['totalCount']:
                return result
            else:
                page += 1
        else:
            print(data)
            print(f"Error when fetching conversations data, retrying {slug}")
            time.sleep(1)
      except:
        print(f"Error when fetching conversations data, retrying {slug}")
        time.sleep(1)

if __name__ == "__main__":
    while r.scard('oc_slug') > 0:
        slug = r.spop('oc_slug').decode('utf-8')
        base_data = fetch_base_data(slug)
        members_data = fetch_members_data(slug)
        if members_data is None:
            continue
        transactions_data = fetch_transactions_data(slug)
        conversation_data = fetch_conversations_data(slug)
        base_data['members'] = members_data
        base_data['transactions'] = transactions_data
        base_data['conversations'] = conversation_data
        print(f"Finished fetching data for {slug}")
        try:
          collection.insert_one(base_data)
        except:
          with open(f'data/{slug}.json', 'w') as file:
                file.write(json.dumps(base_data, cls=JSONEncoder))
        r.sadd('slug_done', slug) 