import requests
import json
import redis
import timeModel
import threading

url = "https://api.github.com/search/repositories"

r = redis.StrictRedis(host='localhost', port=6379, db=0)
tokens = json.load(open('tokens.json', "r"))

def do_crawl(token):
    while r.scard('date_queue') > 0:
      try:
        date = r.spop('date_queue').decode('utf-8')
      except:
        return
      print(f"Current date: {date}")
      headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
      }
      query = f"created:{date}+stars:>=10"
      per_page = 100
      page = 1
      while True:
        try:
          response = requests.get(f"{url}?q={query}&per_page={per_page}&page={page}", headers=headers)
          data = response.json()
        except:
          print(f"Error when fetching date {date}, retrying")
          time.sleep(1)
        if 'items' in data:
          for item in data['items']:
            r.sadd('repo_queue', item['full_name'])
          if page * 100 >= data['total_count']:
            print(f"Date {date} finished, total {data['total_count']} repos")
            r.sadd('date_done', date)
            break
          page += 1
        time.sleep(1)

if __name__ == '__main__':
    threads = []
    for token in tokens:
        t = threading.Thread(target=do_crawl, args=(token,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
