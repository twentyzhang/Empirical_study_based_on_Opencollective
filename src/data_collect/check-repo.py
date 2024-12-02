import requests
import json
import redis
import timeModel
import threading

r = redis.StrictRedis(host='localhost', port=6379, db=0)
tokens = json.load(open('tokens.json', "r"))

url = "https://api.github.com/graphql"

# modify logic here
def is_target(repo):
    if repo is None:
        return False
    if repo['fundingLinks'] is None:
        return False
    for link in repo['fundingLinks']:
        if link['platform'] == 'OPEN_COLLECTIVE':
            return True
    return False

def do_crawl(token):
    headers = {
      'Authorization': f"Bearer {token}",
      'Content-Type': 'application/json'
    }
    while r.scard('repo_queue') > 0:
        query = "{"
        repos = []
        for i in range(10):
            try:
                repo = r.spop('repo_queue').decode('utf-8')
                repos.append(repo)
            except:
                break
            owner, name = repo.split('/')
            query += f"""
            repo{i}: repository(owner: "{owner}", name: "{name}") {{
                fundingLinks {{
                    platform
                    url
                }}
            }}
            """
        query += "}"
        if query == "{}":
            break

        try:
            response = requests.post(url, json={'query': query}, headers=headers)
            if response.status_code != 200:
                print(f"Error when fetching repos, retrying")
                for repo in repos:
                    r.sadd('repo_queue', repo)
                time.sleep(1)
                continue
            data = response.json()
        except:
            print(f"Error when fetching repos, retrying")
            for repo in repos:
                r.sadd('repo_queue', repo)
            time.sleep(1)
            continue

        for i in range(10):
            r.sadd('repo_done', repos[i])
            if f"repo{i}" in data['data']:
                if is_target(data['data'][f"repo{i}"]):
                    print(f"Found {repos[i]}")
                    r.sadd('oc_repo', repos[i])
        time.sleep(1)
               
def main():
  t = []
  for i in range(len(tokens)):
    t.append(threading.Thread(target=do_crawl, args=(tokens[i], )))
    t[i].start()
  
  for i in range(len(tokens)):
    t[i].join()

if __name__ == "__main__":
  main()