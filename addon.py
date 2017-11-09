# -*- coding: utf-8 -*
#url Base para legendas http://video.google.com/timedtext?lang={LANG}&v={VIDEOID}
#Base url to subtitles http://video.google.com/timedtext?lang={LANG}&v={VIDEOID}

#-----------------------------------------Inicio/Start--------------------------------------------
import urllib2
import xml.etree.ElementTree as ET
import json
from datetime import time
import sys
# import xbmcaddon
# import xbmcgui

# addon = xbmcaddon.Addon()
# addonname = addon.getAddonInfo('name')

# xbmcgui.Dialog().ok(addonname)

#http://kodi.wiki/view/HOW-TO:Add_a_new_window_or_dialog_via_skinning referencia para popups

# evento para ativar a busca de legendas ActivateWindow(subtitlesearch)

# lista as lengendas disponiveis no video http://video.google.com/timedtext?type=list&v=zzfCVBSsvqA

# print '''
# Os códigos de idiomas são: \n 
# pt-BR       Portuguese (Brazil) \n 
# pt-PT       Portuguese (Portugal) \n
# pa          Punjabi \n
# qu          Quechua \n
# ro          Romanian \n
# rm          Romansh \n
# nyn         Runyakitara \n
# ru          Russian \n
# gd          Scots Gaelic \n
# sr          Serbian \n
# '''

videoID = 'XdMCyi_Avzc'


req = urllib2.Request('http://video.google.com/timedtext?type=list&v=%s' %(videoID))
response = urllib2.urlopen(req)
sub_list = response.read()

b=[]
list_root = ET.fromstring(sub_list)
for list_child in list_root:
	b.append(list_child.attrib)

code=[]
for list_code in range(len(b)):
	code.append(b[list_code]["lang_code"])
print "idiomas disponíveis:"
for p in code: print p+"\n"

lang = raw_input("selecione um idioma para as legendas:")

req = urllib2.Request('http://video.google.com/timedtext?lang=%s&v=%s' %(lang,videoID))
response = urllib2.urlopen(req)
the_page = response.read()
file=open("sub.xml","w+")
file.write(the_page)
file.close()

status=False
for list_check in range(len(code)):
	if(code[list_check]==lang):
		status=True
		print "Idioma",code[list_check],"Selecionado"
		break
	elif(code[list_check]!=lang):
		continue
#------------------------importacao das legendas em xml-----------------------------------------

if(status!=True):
	exit()
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


	#only seconds
	if(start<60 and end<60):
		if(start<10):
			start=str(int(start))
			start="0"+start
		if(end<10):
			end=str(int(end))
			end="0"+end
		print ("00:00:%.2s,%s --> 00:00:%.2s,%s" %(start,start_mili,end,int(end_mili)))
		subFile.write('''%i\n00:00:%.2s,%s --> 00:00:%.2s,%s\n%s\n\n''' % (index,start,start_mili,end,int(end_mili),legenda.encode('utf-8')))
	elif(start>60 and end>60):
		#minutes and seconds
		if(start/60 >= 1):
			start_min = (start/60)
			start_sec = int(((start/60) - int(start_min))*60)
			if(start_sec<10):
				start_sec=str(start_sec)
				start_sec="0"+start_sec
			if(start_min<10):
				start_min=str(start_min)
				start_min="0"+start_min
		if(end%60 >= 1):
			end_min = (end/60)
			end_sec = ((end/60) - int(end_min))*60
			if(end_sec<10):
				end_sec=str(end_sec)
				end_sec="0"+end_sec
			if(end_min<10):
				end_min=str(end_min)
				end_min="0"+end_min
		#print ("end: 00:%.2s:%.2s,%s" %(end_min,end_sec,end_mili))
		print ("00:%.2s:%.2s,%s --> 00:%.2s:%.2s,%s" %(start_min,start_sec,start_mili,end_min,end_sec,end_mili))
		subFile.write('''%i\n00:%.2s:%.2s,%s --> 00:%.2s:%.2s,%s \n%s\n\n''' % (index,start_min,start_sec,start_mili,end_min,end_sec,end_mili,legenda.encode('utf-8')))
 	#subFile.write('''%i\n:%.0f,%s --> %.0f,%s\n%s\n\n''' % (index, start,start_mili,float(end),end_mili,legenda.encode('utf-8')))
 	index+=1

subFile.close()
