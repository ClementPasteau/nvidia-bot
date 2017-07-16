import os
import requests
from slackclient import SlackClient
from pyquery import PyQuery
import datetime

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def check_drivers():
    pre_url = 'http://www.guru3d.com/'
    url = 'http://www.guru3d.com/files-categories/videocards-nvidia-geforce-vista-%7C-7.html'
    headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0"}
    forum_page = requests.get(url, headers=headers).content
    pq = PyQuery(forum_page)
    first_post_title = pq("h1")[0]
    driver_version = first_post_title.text_content().split('driver')[0].strip()
    print("driver version: %s" % driver_version)
    date = pq(".newsstoryheader")[0].text_content().split('on:')[1].split('[')[0].strip()
    print(date)
    formatted_date = datetime.datetime.strptime(date, "%m/%d/%Y %I:%M %p")
    date_difference = datetime.datetime.now() - formatted_date
    seconds_difference = date_difference.seconds + date_difference.days * 86400
    if (seconds_difference <= 1800):
        print('New driver! Out %d minutes ago!' % (seconds_difference/60))
        page_url = pre_url + first_post_title.getnext().getnext().find('a').get('href')
        response = ":nvidia: @ryuken NEW DRIVER !! *%s* ! %s :nvidia:" % (driver_version, page_url)
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    else:
        print('Existing driver. Out %d minutes ago!' % (seconds_difference/60))

if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("NvidiaBot connected and running!")
        check_drivers()
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
