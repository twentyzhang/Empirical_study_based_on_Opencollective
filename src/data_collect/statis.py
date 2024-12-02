import csv
import os
import redis
import chardet
r = redis.Redis(host='localhost', port=6379, db=0)

start = '2022-02'
end = '2024-08'

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']


def from_stamp_to_ym(stamp):
    return stamp[:7]

def add_month(stamp):
    y, m = stamp.split('-')
    m = int(m) + 1
    if m == 13:
        m = 1
        y = int(y) + 1
    return f"{y}-{m:02d}"

def sub_month(stamp):
    y, m = stamp.split('-')
    m = int(m) - 1
    if m == 0:
        m = 12
        y = int(y) - 1
    return f"{y}-{m:02d}"

def create_base_info():
    base_info = open('data/base_info.csv', 'w')
    csvwriter = csv.writer(base_info)

    header = ['Slug', 'Base','IsFunding']
    for i in range(-6, 7):
        header.append(f'{i}-Commit')
        header.append(f'{i}-Issue')
        header.append(f'{i}-Spend')
        header.append(f'{i}-Sponsor')
    csvwriter.writerow(header)
    get_all_info(csvwriter)

def get_trans_info(file):
    if file is None:
        return None, None, None
    trans = {}
    ctbt = {}
    t = start
    while t <= end:
        trans[t] = 0
        ctbt[t] = 0
        t = add_month(t)
    
    first_sponsor = '2025-01'
    csvfile = open(file, 'r', encoding='utf-8')
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        date = from_stamp_to_ym(row['CreatedAt'])
        if date < start or date > end:
            continue
        if float(row['Amount']) < 0:
            trans[date] += 1
        elif float(row['Amount']) > 0:
            ctbt[date] += 1
            if date >= '2023-02' and date <= '2024-02' and date < first_sponsor:
                first_sponsor = date
    
    if first_sponsor == '2025-01':
        first_sponsor = None
    collective = file.split('.')[0]
    csvfile.close()
    if first_sponsor is None:
        r.sadd('not_sponsor', collective)
    else:
        r.sadd('sponsored', collective)
    return first_sponsor, trans, ctbt

def get_commit_info(file):
    commit = {}
    t = start
    while t <= end:
        commit[t] = 0
        t = add_month(t)
    try:
        csvfile = open(file, 'r')
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if row['Date'] is None:
                continue
            date = from_stamp_to_ym(row['Date'])
            if date < start or date > end:
                continue
            commit[date] += 1
        csvfile.close()
    except:
        pass
    return commit

def get_issue_info(file):
    issue = {}
    t = start
    while t <= end:
        issue[t] = 0
        t = add_month(t)
    
    try:
        csvfile = open(file, 'r')
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            date = from_stamp_to_ym(row['Date'])
            if date < start or date > end:
                continue
            issue[date] += 1
        csvfile.close()
    except:
        pass
    return issue

def get_all_info(csvwriter):
    for _, _, files in os.walk('data/transaction'):
        for file in files:
            fs, spend, sponsor = get_trans_info(os.path.join('data/transaction', file))
            if spend is None:
                continue
            commit = get_commit_info(os.path.join('data/commit', file))
            issue = get_issue_info(os.path.join('data/issue', file))

            if fs is None:
                fs = '2023-02'
                data = [file.split('.')[0], '2023-08','0']
                for i in range(-6, 7):
                    data.append(commit[fs])
                    data.append(issue[fs])
                    data.append(spend[fs])
                    data.append(sponsor[fs])
                    fs = add_month(fs)
            else:
                data = [file.split('.')[0], fs,'1']
                for i in range(0, 6):
                    fs = sub_month(fs)
                for i in range(-6, 7):
                    data.append(commit[fs])
                    data.append(issue[fs])
                    data.append(spend[fs])
                    data.append(sponsor[fs])
                    fs = add_month(fs) 
            csvwriter.writerow(data)

if __name__ == "__main__":
    cw = create_base_info()
    get_trans_info(cw)