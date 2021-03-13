# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name          : Oleg Luganskiy <arcbjorn>
# Collaborators : None
# Time spent    : 10101000110000 sec

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

# ======================
# Data structure design
# ======================

# Problem 1


class NewsStory:
    """
    Single news story from a RSS feed
    """

    def __init__(self, guid, title, description, link, pubdate):
        """
        :param guid: Unique ID
        :type guid: str
        :param title: Title
        :type title: str
        :param description: Description
        :type description: str
        :param link: Link
        :type link: str
        :param pubdate: Publication date
        :type pubdate: str
        """

        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        """
        :returns: Unique id
        :rtype: str
        """
        return self.guid

    def get_title(self):
        """
        :returns: Title
        :rtype: str
        """
        return self.title

    def get_description(self):
        """
        :returns: Description
        :rtype: str
        """
        return self.description

    def get_link(self):
        """
        :returns: Link
        :rtype: str
        """
        return self.link

    def get_pubdate(self):
        """
        :returns: Publication date
        :rtype: str
        """
        return self.pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2


class PhraseTrigger(Trigger):
    """
    Trigger for a phrase
    """

    def __init__(self, phrase):
        """
        :param phrase: Phrase for the trigger
        :type phrase: str
        """
        self.phrase = phrase

    def includes_phrase(self, text):
        """
        Checks if the phrase is in text
        :param text: Text
        :type text: str
        :returns: Is phrase in the text?
        :rtype: bool
        """

        phrase = self.phrase.lower()
        phrase_words = phrase.split(' ')

        # remove punctuation
        text = [' ' if c in string.punctuation else c for c in text.lower()]
        text_words = [word for word in ''.join(text).split(' ') if len(word)]

        if len(phrase_words) == 1:
            return phrase in text_words

        # work through multiple words
        try:
            start_w_index = text_words.index(phrase_words[0])
            phrase_word_count = 1
            index = start_w_index + phrase_word_count
            status = False

            # as long as other words follow
            while index < len(text_words):
                if phrase_words[phrase_word_count] == text_words[index]:
                    phrase_word_count += 1
                else:  # word is not in phrase
                    break
                if phrase_word_count == len(phrase_words):  # all words
                    status = True
                    break
                index += 1
            return status
        except ValueError:  # first phrase word not in text
            return False


# Problem 3
class TitleTrigger(PhraseTrigger):
    """
    Trigger for a phrase in story's title.
    """

    def __init__(self, phrase):
        """
        :param phrase: Phrase for trigger
        :type phrase: str
        """
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        """
        Checks if phrase is in the  title
        :param story: Story
        :type story: NewsStory
        :returns: is phrase in story's title?
        :rtype: bool
        """

        title = story.get_title()
        return self.includes_phrase(title)

# Problem 4


class DescriptionTrigger(PhraseTrigger):
    """
    Trigger for phrase in story's description
    """

    def __init__(self, phrase):
        """
        :param phrase: Phrase for trigger
        :type phrase: str
        """

        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        """
        Checks if phrase is in story's description
        :param story: Story
        :type story: NewsStory
        :returns: is pharase in desciption?
        :rtype: bool
        """

        description = story.get_description()
        return self.includes_phrase(description)

# TIME TRIGGERS

# Problem 5


class TimeTrigger(Trigger):
    """
    Trigger for a certain time
    """

    def __init__(self, time):
        """
        :param time: Time for trigger
        :type time: str
        """

        self.time = datetime.strptime(time, '%d %b %Y %H:%M:%S') \
                            .replace(tzinfo=pytz.timezone('EST'))

# Problem 6


class BeforeTrigger(TimeTrigger):
    """
    Trigger for story published before certain time
    """

    def __init__(self, time):
        """
        :param time: Time for trigger
        :type time: str
        """

        TimeTrigger.__init__(self, time)

    def evaluate(self, story):
        """
        Checks if the provided news story is published before the trigger's
        time.
        :param story: Story
        :type story: NewsStory
        :returns: Was published before trigger's time?
        :rtype: bool
        """

        before_time = story.get_pubdate().replace(tzinfo=pytz.timezone('EST'))
        return before_time < self.time


class AfterTrigger(TimeTrigger):
    """
    Trigger for story
    """

    def __init__(self, time):
        """
        :param time: Time for trigger
        :type time: str
        """

        TimeTrigger.__init__(self, time)

    def evaluate(self, story):
        """
        Checks if story is published after trigger's time.
        :param story: Story
        :type story: NewsStory
        :returns: is published after trigger's time?
        :rtype: bool
        """

        after_time = story.get_pubdate().replace(tzinfo=pytz.timezone('EST'))
        return after_time > self.time


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    """
    Trigger that inverts other trigger
    """

    def __init__(self, trigger):
        """
        :param trigger: The trigger to invert
        :type trigger: Trigger
        """

        self.trigger = trigger

    def evaluate(self, story):
        """
        :param story: The news story to check.
        :type story: NewsStory
        """

        return not self.trigger.evaluate(story)

# Problem 8


class AndTrigger(Trigger):
    """
    Trigger that checks if story satisfied by both triggers
    """

    def __init__(self, trigger1, trigger2):
        """
        :param trigger1: First trigger
        :type trigger1: Trigger
        :param trigger2: Second trigger
        :type trigger2: Trigger
        """

        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        """
        :param story: Story
        :type story: NewsStory
        :returns: both triggers satisfied ?
        :rtype: bool
        """

        res1 = self.trigger1.evaluate(story)
        res2 = self.trigger2.evaluate(story)
        return res1 and res2

# Problem 9


class OrTrigger(Trigger):
    """
    Trigger that checks if at least one trigger is satisfied by story
    """

    def __init__(self, trigger1, trigger2):
        """
        :param trigger1: The first trigger to check.
        :type trigger1: Trigger
        :param trigger2: The second trigger to check.
        :type trigger2: Trigger
        """
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        """
        :param story: Story
        :type story: Story
        :returns: is one or another trigger satidfied by story?
        :rtype: bool
        """

        res1 = self.trigger1.evaluate(story)
        res2 = self.trigger2.evaluate(story)
        return res1 or res2


# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    return [s for s in stories if any(t.evaluate(s) for t in triggerlist)]


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    trigger_dict = {}
    trigger_list = []

    for i in range(len(lines)):
        trig = lines[i].split(',')
        if trig[1] == 'TITLE':
            trigger_dict[trig[0]] = TitleTrigger(trig[2])
        elif trig[1] == 'DESCRIPTION':
            trigger_dict[trig[0]] = DescriptionTrigger(trig[2])
        elif trig[1] == 'AFTER':
            trigger_dict[trig[0]] = AfterTrigger(trig[2])
        elif trig[1] == 'BEFORE':
            trigger_dict[trig[0]] = BeforeTrigger(trig[2])
        elif trig[1] == 'NOT':
            trigger_dict[trig[0]] = NotTrigger(trig[2])
        elif trig[1] == 'AND':
            trigger_dict[trig[0]] = AndTrigger(
                trigger_dict[trig[2]], trigger_dict[trig[3]])
        elif trig[0] == 'ADD':
            for x in range(1, len(trig)):
                trigger_list.append(trigger_dict[trig[x]])
    return trigger_list


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14),
                    yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(
                    END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(
                    END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
