# -*- coding: utf-8 -*-
#url Base para legendas http://video.google.com/timedtext?lang={LANG}&v={VIDEOID}
#Base url to subtitles http://video.google.com/timedtext?lang={LANG}&v={VIDEOID}

#-----------------------------------------Inicio/Start--------------------------------------------
import urllib2
import xml.etree.ElementTree as ET
import json
from datetime import time

print '''
Os códigos de idiomas são: \n 
pt-BR       Portuguese (Brazil) \n 
pt-PT       Portuguese (Portugal) \n
pa          Punjabi \n
qu          Quechua \n
ro          Romanian \n
rm          Romansh \n
nyn         Runyakitara \n
ru          Russian \n
gd          Scots Gaelic \n
sr          Serbian \n
'''

# lang = raw_input("selecione um idioma para as legendas:")
# videoID = 'Z4Kz50LFiZk'

# req = urllib2.Request('http://video.google.com/timedtext?lang=%s&v=%s' %(lang,videoID))
# response = urllib2.urlopen(req)
# the_page = response.read()
# print the_page
# file=open("sub.xml","w+")
# file.write(the_page)
# file.close()

#------------------------importacao das legendas em xml-----------------------------------------
a=[]
tree = ET.parse('sub.xml')
root = tree.getroot()
for child in root:
	a.append(child.attrib)

index = 1
subFile = open("subtitle.srt","w+")
for tempo in range(len(a)):
	#print (a[tempo]["dur"])
	legenda = root[tempo].text
	start = round(float(a[tempo]["start"]),3)
	end =  float(a[tempo]["dur"])+start
	start_mili=round(start-int(start),3)
	start_mili=str(start_mili).replace("0.","")
	end_mili=round(end-int(end),3)
	end_mili=str(end_mili).replace("0.","")
	
	#milliseconds
	if(len(start_mili)==2):
		start_mili=start_mili+'0'
	elif(len(start_mili)==1):
		start_mili=start_mili+'00'

	if(len(end_mili)==2):
		end_mili=end_mili+'0'
	elif(len(end_mili)==1):
		end_mili=end_mili+'00'

	
	if(start<60 and end<60):
		if(start<10):
			start=str(int(start))
			start="0"+start
		if(end<10):
			end=str(int(end))
			end="0"+end
		print ("start: 00:00:%.2s,%s --> end: 00:00:%.2s,%s" %(start,start_mili,end,int(end_mili)))
	elif(start>60 and end>60):
		#minutes and seconds
		if(start%60 >= 1):
			start_min = (start/60)
			start_sec = ((start/60) - int(start_min))*60
		if(end%60 >= 1):
			start_min = (start/60)
			start_sec = ((start/60) - int(start_min))*60
		#print ("start: 00:%.0f:%.0f,%s" %(start_min,start_sec,start_mili))
		print ("start: 00:%.0f:%.0f,%s" %(start_min,start_sec,start_mili))


# 	subFile.write('''%i\n:%.0f,%s --> %.0f,%s\n%s\n\n''' % (index, start,start_mili,float(end),end_mili,legenda.encode('utf-8')))
# 	index+=1

# subFile.close()
