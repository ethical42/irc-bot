#!/usr/bin/env python

from datetime import datetime
import socket
import random
import requests
import json

server = "irc.host.x"
port = 6667
channel = "#channel"
nick = "nick"
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "[!] Connecting to: " + server
irc.connect((server, port))
print irc.recv(4096)

irc.send("NICK " + nick + "\r\n")
irc.send("USER "+ nick +" "+ nick +" "+ nick +" :AES!\n")
irc.send("NICK " + nick + "\n")
irc.send("JOIN " + channel + "\n")

def ircMsg(msg):
    irc.send("PRIVMSG " + channel + " :" + msg + "\r\n")

# Fetch data from reddit's API
def fetchRedditAPI(query):
    url = "https://www.reddit.com/search.json?q="+query+"&limit=5"

    r = requests.get(url, headers={"User-agent": "Chrome"})
    j = r.json()

    for post in j["data"]["children"]:
        title = post["data"]["title"]
        score = post["data"]["score"]
        url = post["data"]["url"]
        ircMsg("[Score: " + str(score) + "] " + str(title.encode('utf-8')) + " <" + str(url.encode('utf-8')) + ">")

while True:
    data = irc.recv(4096)
    user = data.split("!")[0].replace(":"," ") # Get latest user who typed

    if data.find("PING") != -1:
        irc.send("PONG " + data.split()[1] + "\r\n")
    if data.find("KICK") != -1:
        irc.send("JOIN " + channel + "\r\n")
    if data.find(":!reddit ") != -1:
       query = data.split("!reddit ")
       fetchRedditAPI(query[1])
    if data.find("hey") != -1:
       ircMsg("Oh... Hey there," + user)
    if data.find("how are you") != -1:
        words = ["it's all shit, thanks for asking",
        "I am pretending to be a tomato.",
        "I'm good, thanks for asking. How are you," + user + "?",
        "back off! The ice cream is mine!",
        "DO NOT DISTURB, evil genius at work."]
        ircMsg(random.choice(words))
    if data.find("sleep") != -1:
        ircMsg("Oh, are you sleepie" + user + "?")
    if data.find("slaps "+nick) != -1:
        ircMsg("That wasn't nice of you... :(")
    if data.find(".datetime") != -1:
        ircMsg("Here you go" + user + ", it's currently: " + str(datetime.now()))
    if data.find(".morn") != -1:
        words = ["you can find food in the bathroom",
        "come to the dark side. We have cookies.",
        "never set yourself on fire.",
        "even my issues have issues.",
        "oh no! You're going to speak again, aren't you?"]
        ircMsg("Morning, " + random.choice(words))
    if data.find(".funfact") != -1:
        words = ["You can't hum while holding your nose.",
        "Anne Frank and Martin Luther King Jr. were born in the same year.",
        "The population of Mars consists entirely of robots.",
        "It rains diamonds on Saturn and Jupiter.",
        "Every two minutes, we take more pictures than all of humanity did in the 19th century.",
        "There are more atoms in a glass of water than there are glasses of water in all the oceans on Earth.",
        "There's enough water in Lake Superior to cover all of North and South America in 1 foot of water.",
        "An octopus has three hearts.",
        "Every year, hundreds of new trees grow because of squirrels forgetting where they buried their nuts.",
        "If you put your finger in your ear and scratch, it sounds just like Pac-Man.",
        "Cleopatra lived closer to the invention of the iPhone than she did to the building of the Great Pyramid.",
        "The probability of you drinking a glass of water that contains a molecule of water that also passed through a dinosaur is almost 100%.",
        'The YKK on your zipper stands for "Yoshida Kogyo Kabushikigaisha."',
        "If a piece of paper were folded 42 times, it would reach to the moon.",
        "Humans share 50 percent of their DNA with bananas.",
        "The toy Barbie's full name is Barbara Millicent Roberts.",
        "The name Jessica was created by Shakespeare in the play Merchant of Venice.",
        "Oxford University is older than the Aztec Empire.",
        "France was still executing people with a guillotine when the first Star Wars film came out.",
        "Carrots were originally purple.",
        "Vending machines are twice as likely to kill you as a shark is.",
        "There's only one hole in a straw.",
        "Dolphins have names for one another.",
        "Maine is the closest U.S. state to Africa.",
        "Saudi Arabia imports camels from Australia.",
        "There are about twice as many nipples on Earth as there are people.",
        '"umop apisdn" is "upside down" spelled upside down with different letters of the alphabet.',
        "There are more public libraries than McDonald's in the U.S.",
        "There were still people making their way across the United States via the Oregon Trail the year the fax machine was invented.",
        "1998 is as far away as 2030.",
        "New York City is further south than Rome, Italy.",
        "Mammoths went extinct 1,000 years after the Egyptians finished building the Great Pyramid.",
        "There are more fake flamingos in the world than real flamingos.",
        "The surface area of Russia is slightly larger than that of the surface area of Pluto."]
        ircMsg("Fun fact: " + random.choice(words))
    print data
