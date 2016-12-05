# -*- encoding:utf-8 -*-

import jieba
from jieba import analyse
import pandas as pd
import PIL
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt

path = '/Users/zidongceshi/Downloads/DoubanMovie/'
data = pd.read_csv(path+'MrDonkey.csv',names = ['name','comment','grade'])
#a = []
fenci = {}
for i in range(10000):
    comment = data['comment'][i]
    words = list(jieba.cut(comment))
    for word in words:
        if(word>1):
            #a.append(word)
            fenci[word] = fenci.get(word,0) + 1
fenciSort = sorted(fenci.iteritems(),key= lambda d:d[1],reverse=True)
strFenci = [fenciSort[i][0] for i in range(2000)]
strFenci = ','.join(strFenci)

alice_mask = np.array(PIL.Image.open(path+'water.jpg'))
wordcloud = WordCloud(font_path=path+'华文细黑.ttf',
                      background_color='white',
                      width=1800,
                      height=800,
                      margin=5,
                      mask=alice_mask,
                      max_words=2000,
                      max_font_size=60,
                      random_state=42)
wordcloud = wordcloud.generate(strFenci)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()