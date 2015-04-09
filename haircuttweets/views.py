from django.shortcuts import render_to_response,render
import os
from django.template import RequestContext
from models import *
from twitter import *
from django.http import HttpResponseRedirect,HttpResponse
from django.core import serializers
import json,nltk,operator
from django.db import connection

#import pdb

CONSUMER_KEY = 'mC0x6mpbprIF1sy4HJpofFThM'
CONSUMER_SECRET = 'VqkQKchPYkTykacZ0aOVbHvwdDudB5hsWGbvfi6NIYQ2lpNHel'

# Create your views here.
def index(request):
	output = TweetsSearched.objects.all()
	out = serializers.serialize("json",output)
	allField = json.loads(out)

	#pdb.set_trace()
	context = {'datas': allField}
	#return render_to_response('haircuttweets/index.html',context,context_instance=RequestContext(request))
	return render(request, 'haircuttweets/index.html', context)




'''
this method is used to get 1000 data using twitter api
'''
def search(request):

	MY_TWITTER_CREDS = os.path.expanduser('~/.twitter_oauth')
	#if not os.path.exists(MY_TWITTER_CREDS):
	oauth_dance("HairCutProApp", CONSUMER_KEY, CONSUMER_SECRET,MY_TWITTER_CREDS)

	oauth_token, oauth_token_secret = read_token_file(MY_TWITTER_CREDS)
	#pdb.set_trace()	
	twitter = Twitter(auth=OAuth(
	    oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),retry=1)

	# Now work with Twitter
	status = []
	tweet_len = 0
	max_id = False
	while(tweet_len<1000):
		try:
			js =  twitter.search.tweets(q="haircut -filter:retweets",count=100,max_id=max_id)

		except:
			js =  twitter.search.tweets(q="haircut -filter:retweets",count=100)
	#js_all = serializers.serialize("json", js)
	#allField = json.loads(js_all)
		abc = dict(js)
		for i in abc['statuses']:
			status.append(i['text'])
		tweet_len += 100
		max_id = abc['statuses'][99]['id']
	#pdb.set_trace()	
	for i in status:
		stat = TweetsSearched(tweets_result = i)
		stat.save()
	#thefile = open('teststat.txt', 'w') 
	#context = {'datas': False}
	return index(request)
	#output = TweetsSearched.objects.all()
	#out = serializers.serialize("json",output)
	#allField = json.loads(out)

	#pdb.set_trace()
	#context = {'datas': allField}
	#return render(request, 'haircuttweets/index.html', context)
	#return HttpResponse("success")
	#for item in status:    print>>thefile, item.encode('utf-8')

	#print js

'''
this method is used to get top 5 trending haircut
'''
def trends(request):

	output = TweetsSearched.objects.all()
	out = serializers.serialize("json",output)
	allField = json.loads(out)
	hair_trend_list = []
	for i in allField:
		status = i['fields']['tweets_result']
		trend = process(status)
		if(trend):
			hair_trend_list.append(trend)
	#pdb.set_trace()
	top_trend = {}
	ex_list = ['New', 'Miss', 'First', 'My', 'Send', 'Great', 'Post', 'Dat', 'Free', 'Your', 'Need']
	for i in hair_trend_list:
		if i not in ex_list:
			if '.' in i:
				i = i.replace(".", "")
			if i in top_trend:
				top_trend.update({i:top_trend[i]+1})
			else:
				top_trend.update({i:1})
	sor = sorted(top_trend.items(), key=operator.itemgetter(1))
	sor.reverse()
	top_five = [i[0] for i in sor[0:5]]
	context = {'datas': top_five}
	return render(request, 'haircuttweets/trending.html', context)


'''
this method is used to process all the trending haircut
'''
def process(status):
	text_tok = nltk.word_tokenize(status)
	pos_list = nltk.pos_tag(text_tok)
	try:
		#pdb.set_trace()
		begin = [x for x, y in enumerate(pos_list) if y[1] == 'NNP'][0]
		end = [x for x, y in enumerate(pos_list) if y[0] == 'haircut'][0]

		trend_list = []
		trend_flag = 0
		for i in range(begin,(end+1)):
			#pdb.set_trace()
			if(pos_list[i][1] == 'NNP'):
				trend_list.append(pos_list[i][0])
				trend_flag = 1
			elif(pos_list[i][1] == 'POS' and trend_flag):
				continue
			elif(pos_list[i][1] == 'JJ' and trend_flag):
				continue
			elif(pos_list[i][1] == 'NN' and trend_flag):
				continue
			elif((pos_list[i][1] == 'VBD' and i == end) and trend_flag):
				continue
			else:
				trend_flag = 0
				trend_list = []

		if (trend_list):
			#trend_list.reverse()
			#pdb.set_trace()
			return " ".join(trend_list)
	except:
		return False

'''
this method is used to Truncate the database
'''
def trunc(request):
	cursor = connection.cursor()
	cursor.execute("TRUNCATE TABLE `haircuttweets_tweetssearched`")
	context = {'datas': False}
	return render(request, 'haircuttweets/index.html', context)
