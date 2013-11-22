from twilio.rest import TwilioRestClient
from bs4 import BeautifulSoup
import requests
from datetime import date

URL = 'http://www.kickstarter.com/projects/397447350/vantage-sports-sports-analytics-from-the-future'
URL_SHORT = 'http://kck.st/1bxRPRu'
END_DATE = date(2013, 12, 14)
OUTPUT_FILE = 'daily_stats.txt'

# Twilio credentials
account = ''
token = ''
client = TwilioRestClient(account, token)

# Text message details
msg = ''
recipient = '+15555555555'
sender = '+5555555555'

today = date.today()
backers = ''
pledged = ''
pledged_clean = ''
days_left = ''

# request Kickstart page
r = requests.get(URL)
data = r.content
soup = BeautifulSoup(data)

# Find backers
for child in soup.find(id="backers_count").children:
    backers = child.text

# Find pledged amount
pledged = soup.find(id="pledged").text.strip()
pledged_clean = pledged.replace('$','').replace(',','')

# Find days left
days_left = (END_DATE - today).days

# Grab yesterdays info
with open(OUTPUT_FILE, 'r') as r:
    for line in r:
        pass
backers_yesterday = line.split('\t')[1]
pledged_yesterday = line.split('\t')[2]
backers_diff = str(int(backers) - int(backers_yesterday))
pledged_diff = str(int(pledged_clean) - int(pledged_yesterday))


# Compose message
msg = (backers + " backers. " + pledged + " pledged. " + str(days_left) + " days left. " + backers_diff + " new backers. ${} added. " + URL_SHORT).format(pledged_diff)


# Send a text message
message = client.messages.create(to=recipient, from_=sender, body=msg)


# Save to file
with open(OUTPUT_FILE, 'a') as f:
    f.write(today.isoformat() + '\t' + backers + '\t' + pledged_clean + '\t' + str(days_left) + '\n')

