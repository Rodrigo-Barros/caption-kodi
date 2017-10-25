#url Base para legendas http://video.google.com/timedtext?lang={LANG}&v={VIDEOID}
#Base url to subtitles http://video.google.com/timedtext?lang={LANG}&v={VIDEOID}

#-----------------------------------------Inicio/Start--------------------------------------------
import urllib2
import xml.etree.ElementTree as ET
import json

print '''
Os codigos de idiomas sao: \n 
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

lang = raw_input("selecione um idioma para as legendas:")
videoID = 'Z4Kz50LFiZk'

req = urllib2.Request('http://video.google.com/timedtext?lang=%s&v=%s' %(lang,videoID))
response = urllib2.urlopen(req)
the_page = response.read()
print the_page
file=open("sub.xml","w+")
file.write(the_page)
file.close()

#------------------------importacao das legendas em xml-----------------------------------------
a=[]
tree = ET.parse('sub.xml')
root = tree.getroot()
for child in root:
	a.append(child.attrib)

#print a[0]["start"]
index = 1
sub = open("subtitle.srt","w+")
for tempo in range(len(a)):
	#print (a[tempo]["start"])
	start = float(a[tempo]["start"])
	end =  float(a[tempo]["dur"])+start
	sub.write('''
	%i
	%f --> %f
	''' % (index,start,end))
	index+=1

sub.close()
print 'soma'
