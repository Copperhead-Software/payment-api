# import urllib library
from urllib.request import urlopen
import json
url = "http://localhost:5000/"
  
# store the response of URL
response = urlopen(url)
  
# storing the JSON response 
# from url in data
data_json = json.loads(response.read())
  
# print the json response
print(data_json)