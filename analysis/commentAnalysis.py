# -*- encoding:utf--8 -*-

import pandas as pd
from pandas import DataFrame
import os
import json

path = '/Users/zidongceshi/Downloads/DoubanMovie/MrDonkey.json'
# pathNew = '/Users/zidongceshi/Downloads/DoubanMovie/MrDonkeyNew.json'
#
# newFp = open(pathNew,'w')
# datas= []
#
# for line in open(path).readlines():
#     newStr = line.replace(' ','').strip()
#     newFp.write(newStr)

# with open(path,'wr') as f:
#     line = f.readline()
#     line.replace('"','/"')
datas = [json.loads(line) for line in open(path)]
df = DataFrame(datas)





