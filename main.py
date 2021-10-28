import discord
import time
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import asyncio
import re
import requests
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import random

class previous_user_data:
    def __init__(self):
        self.friends = []
        self.following = []
        self.badges = []

class User:
  def __init__(self):
    self.friends = "0"
    self.followers = "0"
    self.following = "0"
    self.name = "0"
    self.display_name = "0"
    self.about_status = "0"
    self.avatar_url = "0"
    self.badges = []
    self.badge_descriptions = []
    self.friend_names_list = []
    self.friend_online = []
    self.friend_ids = []

def fetch_profile_information(soup, current_user):
    friends = str(soup.find("span", {"class": "font-header-2 ng-binding"}))
    friends = friends.replace('<span class="font-header-2 ng-binding" ng-bind="profileHeaderLayout.friendsCount | abbreviate" title="', '')
    friends = friends.split('"')[0]
    current_user.friends = friends

    followers = str(soup.find("span", {"ng-bind": "getAbbreviatedStringFromCountValue(profileHeaderLayout.followersCount)"}))
    followers = followers.replace('<span class="font-header-2 ng-binding" ng-bind="getAbbreviatedStringFromCountValue(profileHeaderLayout.followersCount)" title="', '')
    followers = followers.split('"')[0]
    current_user.followers = followers

    following = str(soup.find("span", {"ng-bind": "getAbbreviatedStringFromCountValue(profileHeaderLayout.followingsCount)"}))
    following = following.replace('<span class="font-header-2 ng-binding" ng-bind="getAbbreviatedStringFromCountValue(profileHeaderLayout.followingsCount)" title="', '')
    following = following.split('"')[0]
    current_user.following = following

    display_name = str(soup.find("h2", {"class": "profile-name text-overflow"})).replace("\n", "")
    display_name = display_name.split(">")[1].split("<")[0].replace(" ", "")
    current_user.display_name = display_name

    name = str(soup.find("div", {"class": "profile-display-name font-caption-body text text-overflow"})).replace("\n", "")
    name = name.replace(" ", "")
    name = name.split(">")[1].split("<")[0].replace("@", "")
    current_user.name = name
        
    about_status = str(soup.find("meta", {"name": "description"})).replace("\n", "")
    about_status = about_status.replace('<meta content="', "").split('"')[0]
    about_status = about_status.split("!")[1]
    current_user.about_status = about_status

    avatar_url = str(soup.find("meta", {"property": "og:image"})).replace("\n", "")
    avatar_url = avatar_url.replace('<meta content="', "").split('"')[0]
    current_user.avatar_url = avatar_url

def fetch_badges(soup, current_user): # Browser must be on https://badges.roblox.com/v1/users/81827160/badges?limit=10&sortOrder=Asc
    s = str(soup)
    badge_names = s.split('"name":"')
    for i in range(0, len(badge_names)):
        if i % 2 != 0:
            current_user.badges.append(badge_names[i].split('"')[0])
    
    badge_descriptions = s.split('"description":"')
    for i in range(0, len(badge_descriptions)):
        if i % 2 != 0:
            current_user.badge_descriptions.append(badge_descriptions[i].split('"')[0])

def fetch_friends(soup, current_user): # Browser must be on https://friends.roblox.com/v1/users/81827160/friends?limit=25&sortOrder=Desc
    print("Fetching friends")
    s = str(soup)
    friend_names_list = s.split('"name":"')
    for i in range(0, len(friend_names_list)):
        if i % 2 != 0:
            current_user.friend_names_list.append(friend_names_list[i].split('"')[0])

    friend_online = s.split('"isOnline":')
    for i in range(0, len(friend_online)):
        if i % 2 != 0:
            current_user.friend_online.append(friend_online[i].split(',')[0])

    friend_ids = s.split('"id":')
    for i in range(0, len(friend_ids)):
        if i % 2 != 0:
            current_user.friend_ids.append(friend_ids[i].split(',')[0])

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
browser = webdriver.Chrome(chrome_options=chrome_options)
time.sleep(2)

# URL = "http://free-proxy.cz/en/proxylist/country/all/socks5/ping/all/"
# r = browser.get(URL)
# soup = BeautifulSoup(browser.page_source, "html.parser")
# print(soup.prettify())

conversation = False

client = discord.Client()
@client.event
async def on_ready():
    print("ready")

@client.event
async def on_message(message):
    if str(message.content).split(" ")[0] == ";watch":
        await message.channel.send("Fetching information... :eye:")
        r = browser.get("https://www.roblox.com/users/" + str(message.content).split(" ")[1] + "/profile")
        soup = BeautifulSoup(browser.page_source, "html.parser")
        current_user = User()
        fetch_profile_information(soup, current_user)

        embedVar = discord.Embed(title=current_user.name, description=current_user.display_name, color=0xfab6dd)
        embedVar.add_field(name="Friends: ", value=str(current_user.friends), inline=False)
        embedVar.add_field(name="Followers: ", value=str(current_user.followers), inline=False)
        embedVar.add_field(name="Following: ", value=str(current_user.following), inline=False)
        embedVar.add_field(name="About status: ", value=str(current_user.about_status), inline=False)
        embedVar.set_image(url=current_user.avatar_url)    #the image itself
        await message.channel.send(embed=embedVar)

        asyncio.sleep(3)
        r = browser.get("https://badges.roblox.com/v1/users/" + str(message.content).split(" ")[1] + "/badges?limit=25&sortOrder=Desc")
        soup = BeautifulSoup(browser.page_source, "html.parser")
        fetch_badges(soup, current_user)

        embedVar2 = discord.Embed(title=str(current_user.name) + "'s last few badges", description=current_user.display_name, color=0x0B646D)
        try:
            for i in range(0, len(current_user.badges)):
                embedVar2.add_field(name=str(current_user.badges[i]), value=str(current_user.badge_descriptions[i]), inline=False)
        except Exception as e:
            print("Problem with the badge names/descriptions")
        await message.channel.send(embed=embedVar2)

        r = browser.get("https://friends.roblox.com/v1/users/" + str(message.content).split(" ")[1] + "/friends?limit=10&sortOrder=Desc")
        soup = BeautifulSoup(browser.page_source, "html.parser")
        fetch_friends(soup, current_user)
        print(str(current_user.friend_names_list))
        print(str(current_user.friend_online))

        asyncio.sleep(3)
        embedVar3 = discord.Embed(title=str(current_user.name) + "'s last few friends", description=current_user.display_name, color=0x2acaea)
        try:
            for i in range(0, len(current_user.friend_names_list)):
                embedVar3.add_field(name=str(current_user.friend_names_list[i]), value="Is online: " + str(current_user.friend_online[i]), inline=False)
        except Exception as e:
            print("Problem with the friend names/online_bools")
        await message.channel.send(embed=embedVar3)
    
    if str(message.content).split(" ")[0] == ";probe":
        current_user = User()
        r = browser.get("https://www.roblox.com/users/" + str(message.content).split(" ")[1] + "/profile")
        soup = BeautifulSoup(browser.page_source, "html.parser")
        fetch_profile_information(soup, current_user)

        G=nx.Graph()
        user_id = message.content.split(" ")[1]
        number_of_people = int(message.content.split(" ")[2])
        soup = str(requests.get("https://friends.roblox.com/v1/users/" + str(user_id) + "/friends?limit=10&sortOrder=Desc").content)
        fetch_friends(soup, current_user)
        if number_of_people > len(current_user.friend_names_list):
            number_of_people = len(current_user.friend_names_list)
        for i in range(0, number_of_people):
            if current_user.friend_online[i] == "true":
                G.add_edge(current_user.friend_names_list[i], current_user.name, color='green', weight=2)
            else:
                G.add_edge(current_user.friend_names_list[i], current_user.name, color='yellow', weight=2)

        # Plotting graph
        pos = nx.circular_layout(G)
        edges = G.edges()
        colors = [G[u][v]['color'] for u,v in edges]
        weights = [G[u][v]['weight'] for u,v in edges]
        nx.draw(G, pos, edge_color=colors, width=1, with_labels=True, font_size=8)
        file_name = "graph" + str(random.randint(0, 1000)) + ".png"
        plt.savefig(file_name)
        await message.channel.send(file=discord.File(file_name))
        G.clear()
        plt.clf()

        
        


client.run("ODg2MzE3MTEyMzY3MzkwNzYw.YTz1Ig.qmRNuLGNQI1M_GqipDtRsyCHhqE", bot=True)
