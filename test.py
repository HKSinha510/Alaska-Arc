from asyncore import read
import json
from random import choice
import requests

def read_json(id, value):
    j = open("test.json")
    js = j.read()
    jso = json.loads(js)

    return jso[id][value]

def test():
    with open('test.json', 'r+') as f:
        data = json.load(f)
        data[client.guild.id] = {"": "ok"} # <--- add `id` value.
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining 
        
def l():
    ls = ['k', 'j', 'h']
    j = choice(ls)
    print(j)

def meme():
    subred = ['SaimanSays', 'memes', 'india', 'IncredibleIndia', 'bakchodi', 'indianpeoplequora', 'unitedstatesofindia']

    link = [f'http://aio-api-discord.herokuapp.com/reddit/hot?subreddit={choice(subred)}', f'http://aio-api-discord.herokuapp.com/reddit/new?subreddit={choice(subred)}', f'http://aio-api-discord.herokuapp.com/reddit/random?subreddit={choice(subred)}']

    #try: 

    g = str(choice(link))
    print(g)
    response = requests.get(g)
    json_data = json.loads(response.text)
    title = json_data['title']
    description = json_data['description']
    url = json_data['url']
    post = json_data['post_url']
    data = [title, description, url, post]

    '''except Exception as e:
        print(e)
        data = ['API Error', 'error', 'https://cdn.discordapp.com/attachments/795547584604143646/846637578233184256/PicsArt_05-03-10.png', 'https://cdn.discordapp.com/attachments/795547584604143646/846637578233184256/PicsArt_05-03-10.png']
'''
    print(data)

def give_():
    return "errr"

def check():
    give = give_()
    while give == "error":
        print("give")

    print("no")

if __name__ == "__main__":
    a = "fghjkl;.png"
    print(a[-3:])
    #print(take)
    #check()