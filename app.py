
import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
import nltk
import googletrans
import time

computation_done = False



consumerKey = 'eFXpeZrW6u5OybnzQnJRbONOI'
consumerSecret = 'IYHl3MDWjbRBfRrhto4wefeOUNhgrtq7RK97ZZGxxrv2Y0GfAc'
accessToken = '1590586197490794497-Whtnh9xHAN63QoLBpHhMtSRZBnB6FY'
accessTokenSecret = '6G158lSuZVdy1i3qLxbXXFkQw0lkmnu3BNCJMOhYJQ8jG'


#Create the authentication object
auth= tweepy.OAuthHandler(consumerKey, consumerSecret) 
    
# Set the access token and access token secret
auth.set_access_token(accessToken, accessTokenSecret) 
    
# Creating the API object while passing in auth information
api = tweepy.API(auth, wait_on_rate_limit = True)















#plt.style.use('fivethirtyeight')










def app():
	img = Image.open("logo.jpeg")
	#st.image(img, width=400, caption="[Link](https://www.designboxed.com/)")
	#st.image(img, width=0.5, use_column_width=False, caption='',  format='JPEG', width_default=None, width_min=None, width_max=None, 
         #alt_text=None, link='https://www.designboxed.com/')

	activities=["Tweet Analyzer","Generate Twitter Data"]
	choice = st.sidebar.selectbox("Select Your Activity",activities)
	#[![logo.jpg](https://i.postimg.cc/N0DL61mc/logo.jpg)](https://postimg.cc/GBBcrTX7)
	#st.markdown("[![logo.jpg](https://i.postimg.cc/N0DL61mc/logo.jpg)](https://www.designboxed.com/)")
	
	
	st.markdown(
    """
    <style>
        .icon {{
            height: 30px;
            width: 30px;
            margin-left: 10px;
			
        }}
    </style>
    <div style="float: right;">
        <a href="https://www.facebook.com/DesignBoxedCreatives" target="_blank">
            <img class="icon" src="https://i.postimg.cc/wvJDk283/317752-facebook-social-media-social-icon.png"/>
        </a>
        <a href="https://twitter.com/DesignBoxed" target="_blank">
            <img class="icon" src="https://i.postimg.cc/pLzxRnHz/5296514-bird-tweet-twitter-twitter-logo-icon.png"/>
        </a>
        <a href="https://www.instagram.com/designboxedcreatives" target="_blank">
            <img class="icon" src="https://i.postimg.cc/bJzq6Y4b/4102579-applications-instagram-media-social-icon.png"/>
        </a>
    </div>
    """
    ,unsafe_allow_html=True)

	#st.image(img, width=400, caption="[Link](https://www.designboxed.com/)")
	#[![logo.jpg](https://i.postimg.cc/T1hjDDq3/logo.jpg)](https://postimg.cc/p5bnNy6w)

	st.markdown(
    """
    <style>
        .icon {{
            height: 30px;
            width: 30px;
            margin-left: 10px;
			
        }}
    </style>
    <div style="float: left;margin-top:-45px;">
        <a href="https://www.designboxed.com/" target="_blank">
            <img class="icon" src="https://i.postimg.cc/V62T5mnp/logo1.jpg"/>
        </a>
       
    </div>
    """
    ,unsafe_allow_html=True)
	st.markdown("<h1 style='text-align: center; color: red;'>Twitter Sentiment Analyser</h1>", unsafe_allow_html=True)


	

	if choice=="Tweet Analyzer":
		st.markdown("<h4 style='text-align: center; color: black;'>Analyze the tweets of your favourite Personalities</h4>", unsafe_allow_html=True)
		#st.subheader("Analyze the tweets of your favourite Personalities")
		raw_text = st.text_area("Enter the exact Twitter handle of the Personality (without @)")
		#st.write("1. Fetches the 5 most recent tweets from the given twitter handle")
		#st.write("2. Generates a Word Cloud")
		#st.write("3. Performs Sentiment Analysis and displays it in the form of a Bar Graph")

		Analyzer_choice=st.selectbox("Select the activities",['Show Recent Tweets','Generate WordCloud','Visualize the Sentiment Analysis'])
	
		
		if st.button("Analyze"):
			with st.spinner():

			
				if Analyzer_choice == "Show Recent Tweets":

					def Show_Recent_Tweets(raw_text):
						# Extract 100 tweets from the twitter user
						posts = api.user_timeline(screen_name=raw_text, count = 100, tweet_mode="extended")

						def get_tweets():

							l=[]
							i=1
							for tweet in posts[:5]:
								l.append(tweet.full_text)
								i= i+1
							return l

						recent_tweets=get_tweets()		
						return recent_tweets
						
					recent_tweets= Show_Recent_Tweets(raw_text)
					
					st.write(recent_tweets)



				elif Analyzer_choice=="Generate WordCloud":

					st.success("Generating Word Cloud")

					def gen_wordcloud():

						posts = api.user_timeline(screen_name=raw_text, count = 500, tweet_mode="extended")
						

						df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
						from googletrans import Translator
						translator=Translator()
						df['Tweets_eng']=df['Tweets'].apply(lambda row: translator.translate(row,dest='en').text)
						df['Tweets_eng']=df['Tweets_eng'].astype('string')
						df['Tweets_eng'] = df['Tweets_eng'].apply(lambda x: ' '.join(x.lower() for x in x.split()))
						
						#cleaning text
						emoji_pattern = re.compile("["
							u"\U0001F600-\U0001F64F"  # emoticons
							u"\U0001F300-\U0001F5FF"  # symbols & pictographs
							u"\U0001F680-\U0001F6FF"  # transport & map symbols
							u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
							u"\U00002500-\U00002BEF"  # chinese char
							u"\U00002702-\U000027B0"
							u"\U00002702-\U000027B0"
							u"\U000024C2-\U0001F251"
							u"\U0001f926-\U0001f937"
							u"\U00010000-\U0010ffff"
							u"\u2640-\u2642"
							u"\u2600-\u2B55"
							u"\u200d"
							u"\u23cf"
							u"\u23e9"
							u"\u231a"
							u"\ufe0f"  # dingbats
							u"\u3030"  # flags (iOS)
							"]+", flags=re.UNICODE)
						
						def cleanTxt(text):
							text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
							text = re.sub('#', '', text)  # Removing '#' hash tag
							text = re.sub('RT[\s]+', '', text)  # Removing 
							text = re.sub('https?:\/\/\S+', '', text)
							text = re.sub("\n", "", text)  # Removing hyperlink
							text = re.sub(":", "", text)  # Removing hyperlink
							text = re.sub("_", "", text)  # Removing hyperlink
							text = re.sub("|", "", text)
							text = re.sub(",", "", text)
							text = re.sub("\d+", "", text) #removing digits

							text= ' '.join(text.lower() for text in text.split())
							text = re.sub("%", "", text)
							text = re.sub("!", "", text)
							text = emoji_pattern.sub(r'', text)
							
							return text
						
						df['Tweets_eng']=df['Tweets_eng'].apply(cleanTxt)

						#stopword removal
						from nltk.corpus import stopwords
						stop=stopwords.words('english')
						df['Tweets_eng'] = df['Tweets_eng'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

						# word cloud visualization
						allWords = ' '.join([twts for twts in df['Tweets_eng']])
						wordCloud = WordCloud(width=700, height=400, random_state=21, max_font_size=110).generate(allWords)
						plt.imshow(wordCloud, interpolation="bilinear")
						plt.axis('off')
						plt.savefig('WC.jpg')
						img= Image.open("WC.jpg") 
						return img

					img=gen_wordcloud()

					st.image(img)



				else :
					
					def Plot_Analysis():

						st.success("Generating Visualisation for Sentiment Analysis")

					
						posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")

						df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])


						
						# Create a function to clean the tweets
						def cleanTxt(text):
							text = re.sub('@[A-Za-z0–9]+', '', text) 
							text = re.sub('#', '', text) # Removing '#' has
							text = re.sub('RT[\s]+', '', text) # Removing RT
							text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
							return text


						# Clean the tweets
						df['Tweets'] = df['Tweets'].apply(cleanTxt)


						def getSubjectivity(text):
							return TextBlob(text).sentiment.subjectivity

						# Create a function to get the polarity
						def getPolarity(text):
							return  TextBlob(text).sentiment.polarity


						# Create two new columns 'Subjectivity' & 'Polarity'
						df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
						df['Polarity'] = df['Tweets'].apply(getPolarity)


						def getAnalysis(score):
							if score < 0:
								return 'Negative'
							elif score == 0:
								return 'Neutral'
							else:
								return 'Positive'
						
							
						df['Analysis'] = df['Polarity'].apply(getAnalysis)


						return df
					df= Plot_Analysis()
					fig=plt.figure(figsize=(7,4))
					sns.countplot(x=df['Analysis'],data=df,color='Red')
					st.pyplot(fig)


           

				#st.pyplot(use_container_width=True)

				

	

	else:

		st.subheader("This tool fetches the last 100 tweets from the Twitter handle & creates a DataFrame")

		st.write("The DataFrame includes Subjectivity,Polarity,Sentiment of the Tweet")
		

		user_name = st.text_area("*Enter the exact twitter handle of the Personality (without @)*")

		

		def get_data(user_name):

			posts = api.user_timeline(screen_name=user_name, count = 100, lang ="en", tweet_mode="extended")

			df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

			def cleanTxt(text):
				text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
				text = re.sub('#', '', text) # Removing '#' hash tag
				text = re.sub('RT[\s]+', '', text) # Removing RT
				text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
				text= re.sub(':','',text)
				return text

			# Clean the tweets
			df['Tweets'] = df['Tweets'].apply(cleanTxt)

			return df

		if st.button("Show Data"):

			st.success("Fetching Last 100 Tweets")

			df=get_data(user_name)

			st.write(df)

	st.subheader(' ------ Created By : Automation team(DesignBoxed) ------ :sunglasses:')

if __name__ == "__main__":
	app()