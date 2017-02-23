from urllib import request
from bs4 import BeautifulSoup

with open('이름 없는 문서', 'r') as in_file:
    data = in_file.read().split('\n')

quote_list = [i.strip() for i in data[:-1]]

for _quote in quote_list:
    quote = _quote.replace(" ", "%20")

    keyword = "https://twitter.com/search?q="+quote
    print(keyword)
    crawling_page = request.urlopen(keyword).read().decode('utf-8')

    soup = BeautifulSoup(crawling_page, 'html.parser')

    tweet_div = soup.findAll('div', attrs={'class':"original-tweet"})

    for div in tweet_div:
        reply_count = div.find('span', attrs={'class':'ProfileTweet-actionCountForPresentation'})
        if (reply_count.text).isdigit() == True and int(reply_count.text) >= 2:
        #print(reply_count.text)

            path = div.get('data-permalink-path')

            corpus_url = "https://twitter.com/"+path
            corpus_data = request.urlopen(corpus_url).read()
            corpus_soup = BeautifulSoup(corpus_data, 'html.parser')
            permalink_data = corpus_soup.find('div', attrs={'class':'permalink', 'role':'main'})

            _original_tweet = permalink_data.find('div', attrs={'class':'js-original-tweet'})
            original_tweet = _original_tweet.find('p', attrs={'class':'tweet-text'})
        #print(original_tweet.text)

            permalink_replies = permalink_data.find('div', attrs={'class':'replies-to'})
            _thread_tweet = permalink_replies.find('li', attrs={'class':'ThreadedConversation'})

            if _thread_tweet != None:
                thread_tweet = _thread_tweet.findAll('div', attrs={'class': 'ThreadedConversation-tweet'})
            #print(thread_tweet)

                print(original_tweet.text, "\n")
                for tweet in thread_tweet:
                    _tweet_text = tweet.find('div', attrs={'class': 'js-tweet-text-container'})
                    print((_tweet_text.find('p', attrs={'class': 'tweet-text'})).text)

                print("\n\n")


        break