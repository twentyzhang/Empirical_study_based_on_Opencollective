import requests
import redis
import json
import threading
from pymongo import MongoClient

tokens = json.load(open('tokens.json', "r"))
r = redis.StrictRedis(host='localhost', port=6379, db=0)
cli = MongoClient('localhost', 27017)
db = cli['gh']
collection = db['repos']

def do_crawl(token):
  while r.scard('oc_repo') > 0:
    times = min(r.scard('oc_repo'), 10)
    query = "{"
    full_names = []
    for i in range(times):
      data = r.spop('oc_repo')
      if data is None:
        break
      repo = data.decode('utf-8').split('/')

      owner = repo[0]
      name = repo[1]
      full_names.append(owner + '/' + name)
      query += f"""
      repo{i}: repository(owner: "{owner}", name: "{name}") {{
          description
          stargazerCount
          forkCount
          watchers {{
          totalCount
          }}
          issues(states: OPEN) {{
          totalCount
          }}
          pullRequests(states: OPEN) {{
          totalCount
          }}
          releases {{
          totalCount
          }}
          diskUsage
          repositoryTopics(first: 10) {{
          nodes {{
              topic {{
              name
              }}
          }}
          }}
          languages(first: 10) {{
          edges {{
              node {{
              name
              }}
              size
          }}
          }}
          defaultBranchRef {{
          target {{
              ... on Commit {{
              history(first: 100) {{
                  edges {{
                  node {{
                      message
                      committedDate
                      author {{
                      name
                      email
                      }}
                  }}
                  }}
              }}
              }}
          }}
          }}
      }}

      """
    query += "}"
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    url = "https://api.github.com/graphql"

    try:
      response = requests.post(url, headers=headers, json={'query': query})
      data = response.json()['data']
      
      for i in range(len(data)):
        try:
          current = data['repo' + str(i)]
          document = {
            "full_name": full_names[i],
            "description": current['description'],
            "stargazerCount": current['stargazerCount'],
            "forkCount": current['forkCount'],
            "watcherCount": current['watchers']['totalCount'],
            "issueCount": current['issues']['totalCount'],
            "prCount": current['pullRequests']['totalCount'],
            "releaseCount": current['releases']['totalCount'],
            "diskUsage": current['diskUsage'],
            "topics": [topic['topic']['name'] for topic in current['repositoryTopics']['nodes']],
            "languages": {edge['node']['name']: edge['size'] for edge in current['languages']['edges']},
            "commits": [{"message": edge['node']['message'], "date": edge['node']['committedDate'], "author": edge['node']['author']['name'], "email": edge['node']['author']['email']} for edge in current['defaultBranchRef']['target']['history']['edges']]
          }

          collection.insert_one(document)
          r.sadd('oc_done', document['full_name'])
          print("Finish to crawl", document['full_name'])
        except:
          r.sadd('oc_repo', full_names[i])
          continue
    except:
      for i in range(len(full_names)):
        r.sadd('oc_repo', full_names[i])
      print(data)

def main():
  t = []
  for i in range(len(tokens)):
    t.append(threading.Thread(target=do_crawl, args=(tokens[i], )))
    t[i].start()
  
  for i in range(len(tokens)):
    t[i].join()

if __name__ == "__main__":
  main()