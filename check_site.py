import http.client
import filecmp
import os

sites = [] #tumblr blog sites (ex: 'name.tumblr.com')

for url in sites: #iterate all blogs
	filename = url[0:url.find('.')]+'.txt' #file names (blog name + txt)

	site = http.client.HTTPConnection(url) #open http connection with blog

	site.request('GET', '/api/read/json') #GETs the blog content from the old tumblr api in JSON format
	response = site.getresponse() #receives response
	
	htmlcode = str(response.read()) #JSON response

	try:
		f = open('temp_'+filename, 'w+') #tries to open new temporary file
		f.write(htmlcode) #puts response in temp file
		f.close() #closes file

		if not filecmp.cmp(filename, 'temp_'+filename): #compares old file with new temp file
			print('website '+filename[0:filename.find('.')]+' changed') #returns if file was changed

	except:
		pass

	f = open(filename, 'w') #opens old file
	f.write(htmlcode) #writes new content
	f.close() #closes file
	os.remove('temp_'+filename) #deletes temporary file