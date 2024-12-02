import json
import csv

def sanitize_text(s):
    if s is None:
        return ""
    if type(s) is not str:
        s = str(s)
    s1 = s.split('\n')
    s2 = s1[0].split(',')
    if len(s1) > 1 or len(s2) > 1:
        return s2[0] + "..."
    else:
        return s2[0]

other = ['dim', 'logseq', 'phpfoundation', 'webpack']

def extract_media_info(data):
    target_media = ['WEBSITE', 'GITHUB', 'TWITTER', 'YOUTUBE', 'LINKEDIN']
    medias = {}
    for link in data['socialLinks']:
        medias[link['type']] = link['url']
    
    for media in target_media:
        medias[media] = sanitize_text(medias.get(media, None))
    return medias
    
def extract_base_info(oc, writer):
    id = sanitize_text(oc['id'])
    slug = sanitize_text(oc['slug'])
    name = sanitize_text(oc['name'])
    description = sanitize_text(oc['description'])
    currency = sanitize_text(oc['currency'])
    expensePolicy = sanitize_text(oc['expensePolicy'])
    isIncognito = sanitize_text(oc['isIncognito'])
    createdAt = sanitize_text(oc['createdAt'])
    updatedAt = sanitize_text(oc['updatedAt'])
    medias = extract_media_info(oc)

    writer.writerow([id, slug, name, description, currency, expensePolicy, isIncognito, createdAt, updatedAt, medias['WEBSITE'], medias['GITHUB'], medias['TWITTER'], medias['YOUTUBE'], medias['LINKEDIN']])

def extract_member_info(oc, writer):
    id = sanitize_text(oc['id'])
    slug = sanitize_text(oc['account']['slug'])
    role = sanitize_text(oc['role'])
    publicMessage = sanitize_text(oc['publicMessage'])
    description = sanitize_text(oc['description'])
    donations = sanitize_text(oc['totalDonations']['value'])
    currency = sanitize_text(oc['totalDonations']['currency'])
    if oc['account']['location'] is not None:
        country = sanitize_text(oc['account']['location']['country'])
    else:
        country = ""
    medias = extract_media_info(oc['account'])
    writer.writerow([id, slug, role, publicMessage, description, donations, currency, country, medias['WEBSITE'], medias['GITHUB'], medias['TWITTER'], medias['YOUTUBE'], medias['LINKEDIN']])

def extract_transaction_info(oc, writer):
    id = sanitize_text(oc['id'])
    type = sanitize_text(oc['type'])
    kind = sanitize_text(oc['kind'])
    amount = sanitize_text(oc['amount']['value'])
    currency = sanitize_text(oc['amount']['currency'])
    createdAt = sanitize_text(oc['createdAt'])
    description = sanitize_text(oc['description'])
    if oc['order'] is None:
        tax = ""
        taxCurrency = ""
        platformTipAmount = ""
        platformTipCurrency = ""
        hostFeePercent = ""
        frequency = ""
    else:
        if oc['order']['taxAmount'] is not None:
            tax = sanitize_text(oc['order']['taxAmount']['value'])
            taxCurrency = sanitize_text(oc['order']['taxAmount']['currency'])
        else:
            tax = ""
            taxCurrency = ""
        if oc['order']['platformTipAmount'] is not None:
            platformTipAmount = sanitize_text(oc['order']['platformTipAmount']['value'])
            platformTipCurrency = sanitize_text(oc['order']['platformTipAmount']['currency'])
        else:
            platformTipAmount = ""
            platformTipCurrency = ""
        hostFeePercent = sanitize_text(oc['order']['hostFeePercent'])
        frequency = sanitize_text(oc['order']['frequency'])
    writer.writerow([id, type, kind, amount, currency, createdAt, description, tax, taxCurrency, platformTipAmount, platformTipCurrency, hostFeePercent, frequency])

def extract_all_info():
    csvfile = open('oc_info/oc.csv', 'w')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Id', 'Slug', 'Name', 'Description', 'Currency', 'ExpensePolicy', 'IsIncognito', 'CreatedAt', 'UpdatedAt', 'Website', 'Github', 'Twitter', 'Youtube', 'LinkedIn'])
    
    file = open('collective.json', 'r')
    for line in file:
        oc = json.loads(line)
        extract_base_info(oc['data']['collective'], csvwriter)

        memberfile = open(f'member/{oc["data"]["collective"]["slug"]}.csv', 'w')
        memberwriter = csv.writer(memberfile)
        memberwriter.writerow(['Id', 'Slug', 'Role', 'PublicMessage', 'Description', 'Donations', 'Currency', 'Country', 'Website', 'Github', 'Twitter', 'Youtube', 'Linkedin'])
        for member in oc['members']:
            extract_member_info(member, memberwriter)
        
        transactionfile = open(f'transaction/{oc["data"]["collective"]["slug"]}.csv', 'w')
        transactionwriter = csv.writer(transactionfile)
        transactionwriter.writerow(['Id', 'Type', 'Kind', 'Amount', 'Currency', 'CreatedAt', 'Description', 'Tax', 'TaxCurrency', 'PlatformTipAmount', 'PlatformTipCurrency', 'HostFeePercent', 'Frequency'])
        for transaction in oc['transactions']:
            extract_transaction_info(transaction, transactionwriter)

    for name in other:
        file = open(f'{name}.json', 'r')
        oc = json.loads(file.read())
        extract_base_info(oc['data']['collective'], csvwriter)

        memberfile = open(f'member/{name}.csv', 'w')
        memberwriter = csv.writer(memberfile)
        memberwriter.writerow(['Id', 'Slug', 'Role', 'PublicMessage', 'Description', 'Donations', 'Currency', 'Country', 'Website', 'Github', 'Twitter', 'Youtube', 'Linkedin'])
        for member in oc['members']:
            extract_member_info(member, memberwriter)
        
        transactionfile = open(f'transaction/{name}.csv', 'w')
        transactionwriter = csv.writer(transactionfile)
        transactionwriter.writerow(['Id', 'Type', 'Kind', 'Amount', 'Currency', 'CreatedAt', 'Description', 'Tax', 'TaxCurrency', 'PlatformTipAmount', 'PlatformTipCurrency', 'HostFeePercent', 'Frequency'])
        for transaction in oc['transactions']:
            extract_transaction_info(transaction, transactionwriter)

if __name__ == '__main__':
    extract_all_info()