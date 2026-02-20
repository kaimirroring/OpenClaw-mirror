#!/usr/bin/env python3
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
import re

TOKEN='/home/jose/.openclaw/secrets/google/token.json'
SCOPES=[
 'https://www.googleapis.com/auth/gmail.modify',
 'https://www.googleapis.com/auth/gmail.labels',
 'https://www.googleapis.com/auth/drive.file'
]

LABELS=[
 'OC/Urgent','OC/Finance','OC/Work','OC/Newsletters','OC/Promotions','OC/Waiting-Reply','OC/To-Review'
]

FINANCE = re.compile(r'(invoice|receipt|payment|bank|billing|factura|pago|stripe|paypal)', re.I)
NEWS = re.compile(r'(newsletter|digest|bolet[ií]n|substack)', re.I)
PROMO = re.compile(r'(sale|discount|offer|promo|deal|coupon|black friday)', re.I)
URGENT = re.compile(r'(urgent|asap|immediate|hoy|importante|critical)', re.I)
WORK = re.compile(r'(github|deploy|server|openclaw|supabase|vercel|firebase|api)', re.I)

ARCHIVE_COOLDOWN_HOURS = 48


def ensure_label_map(svc):
    r=svc.users().labels().list(userId='me').execute()
    existing={x['name']:x['id'] for x in r.get('labels',[])}
    out={}
    for name in LABELS:
        if name in existing:
            out[name]=existing[name]
        else:
            created=svc.users().labels().create(userId='me', body={
                'name':name,'labelListVisibility':'labelShow','messageListVisibility':'show'
            }).execute()
            out[name]=created['id']
    return out


def classify(subject,sender,snippet):
    text=' '.join([subject or '', sender or '', snippet or ''])
    labels=[]
    if URGENT.search(text): labels.append('OC/Urgent')
    if FINANCE.search(text): labels.append('OC/Finance')
    if NEWS.search(text): labels.append('OC/Newsletters')
    if PROMO.search(text): labels.append('OC/Promotions')
    if WORK.search(text): labels.append('OC/Work')
    if not labels: labels.append('OC/To-Review')
    return labels


def should_archive(labels, internal_ms):
    low_value = ('OC/Newsletters' in labels) or ('OC/Promotions' in labels)
    protected = any(x in labels for x in ('OC/Urgent','OC/Finance','OC/Work'))
    if not low_value or protected:
        return False
    msg_time = datetime.fromtimestamp(int(internal_ms)/1000, tz=timezone.utc)
    age = datetime.now(timezone.utc) - msg_time
    return age >= timedelta(hours=ARCHIVE_COOLDOWN_HOURS)


def main():
    creds=Credentials.from_authorized_user_file(TOKEN, SCOPES)
    svc=build('gmail','v1',credentials=creds,cache_discovery=False)
    label_map=ensure_label_map(svc)

    after=(datetime.now(timezone.utc)-timedelta(days=14)).strftime('%Y/%m/%d')
    q=f'after:{after} -in:chats'
    msgs=[]
    page=None
    while True:
        resp=svc.users().messages().list(userId='me', q=q, maxResults=200, pageToken=page).execute()
        msgs.extend(resp.get('messages',[]))
        page=resp.get('nextPageToken')
        if not page or len(msgs)>=500:
            break

    labeled=0
    archived=0
    for m in msgs:
        full=svc.users().messages().get(userId='me', id=m['id'], format='metadata', metadataHeaders=['Subject','From']).execute()
        headers={h['name']:h['value'] for h in full.get('payload',{}).get('headers',[])}
        labels=classify(headers.get('Subject',''), headers.get('From',''), full.get('snippet',''))
        add=[label_map[x] for x in labels]

        body={'addLabelIds':add}
        current=set(full.get('labelIds',[]))
        if should_archive(labels, full.get('internalDate','0')) and 'INBOX' in current:
            body['removeLabelIds']=['INBOX']
            archived += 1

        svc.users().messages().modify(userId='me', id=m['id'], body=body).execute()
        labeled += 1

    print(f'TRIAGE_OK processed={len(msgs)} labeled={labeled} archived={archived}')

if __name__=='__main__':
    main()
