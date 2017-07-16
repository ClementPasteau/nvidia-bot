import os
import time
import requests
import random
from slackclient import SlackClient
from pyquery import PyQuery

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    if command == "hello":
        slack_client.api_call("chat.postMessage", channel=channel,
                                    text=":nvidia: Hello my friend :nvidia:", as_user=True)
    elif command == "last":
        pre_url = 'http://www.guru3d.com/'
        url = 'http://www.guru3d.com/files-categories/videocards-nvidia-geforce-vista-%7C-7.html'
        headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0"}
        forum_page = requests.get(url, headers=headers).content
        pq = PyQuery(forum_page)
        first_post_title = pq("h1")[0]
        driver_version = first_post_title.text_content().split('driver')[0].strip()
        page_url = pre_url + first_post_title.getnext().getnext().find('a').get('href')

        response = ":nvidia: *%s* ! %s :nvidia:" % (driver_version, page_url)
        slack_client.api_call("chat.postMessage", channel=channel,
                                    text=response, as_user=True)
    else:
        slack_client.api_call("chat.postMessage", channel=channel,
            text=":nvidia: Oops I don't understand. Try using 'hello' or'last' commands. :nvidia:", as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("NvidiaBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
