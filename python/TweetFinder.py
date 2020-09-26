import json
import pandas as pd
import tweepy
from random import randrange


# Enter keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] = "NIMZvJEPSU3SneNLofhQk0zCF"
credentials['CONSUMER_SECRET'] = "75qVaSEte2gq2E0PO9Mp3ru0neEeMuFB22Z0lI3LRwTqZ0Rmo9"
credentials['ACCESS_TOKEN'] = "1308982729581703172-gVyFA593mSdKPXXA5Z0fyLz6BTD16E"
credentials['ACCESS_SECRET'] = "TVgVGvEF2ONkul8UY64xjWFq84knWjUkBBlM2klKeTbRa"


# Save the credentials object to file
with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)

with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

#create dataframes to be filled in
kanyetweets = {'kanye': []}
elontweets = {'elon': []}


auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])

api = tweepy.API(auth)

#to filter out in tweets
matches = ["@", "#", "https://"]

#grab filtered kanye tweets
for status in tweepy.Cursor(api.user_timeline, screen_name='@kanyewest', tweet_mode="extended", count=3200).items():
    if not status.retweeted:
        if not any(x in status.full_text for x in matches):
            kanyetweets["kanye"].append(status.full_text)

#grab filtered elon tweets
for status in tweepy.Cursor(api.user_timeline, screen_name='@elonmusk', tweet_mode="extended", count=3200).items():
    if not status.retweeted:
        if not any(x in status.full_text for x in matches):
            elontweets["elon"].append(status.full_text)

elon_df = pd.DataFrame(elontweets)
kanye_df = pd.DataFrame(kanyetweets)

numKanye = len(kanye_df['kanye'])
numElon = len(elontweets['elon'])


#prompts player and displays tweet, keeping track of right and wrong guesses
def playGame(numRight, numWrong):
    numKanye = len(kanye_df['kanye'])
    numElon = len(elontweets['elon'])

    randtweetKanye = randrange(numKanye)
    randtweetElon = randrange(numElon)

    randuser = randrange(2)

    if randuser==0:
        mytweet = kanye_df.iloc[randtweetKanye]['kanye']
        user = "kanye"

    else:
        mytweet = elon_df.iloc[randtweetElon]['elon']
        user = "elon"

    print(mytweet)

    val2 = input("\nEnter your guess (kanye/elon): ")

    while (val2!="kanye" and val2!="elon"):
        val2 = input("\nPlease enter a valid user (kanye/elon):  ")

    if (val2==user):
        print("Correct!")
        numRight+=1

    else:
        print("Wrong guess!")
        numWrong+=1

    return numRight, numWrong



numRight = 0
numWrong = 0

print("Welcome to the Elon Musk vs Kanye West Twitter guessing game!"
      "\nI will print out a random Kanye West or Elon Musk tweet and you must guess which one it is.")

val = input("\nWant to play? (y/n):  ")
while (val != "y" and val != "n"):
    val = input("\nPlease enter a valid character y/n:  ")

while val=="y":
    game = playGame(numRight, numWrong)
    numRight = game[0]
    numWrong = game[1]
    val = input("\nWant to play again? (y/n):  ")

    while (val != "y" and val != "n"):
        val = input("\nPlease enter a valid character y/n:  ")


print("You recognized %s tweet(s) and guessed %s wrong (%s %% correct!)" % (numRight, numWrong, (100*(numRight/(numRight+numWrong)))))


