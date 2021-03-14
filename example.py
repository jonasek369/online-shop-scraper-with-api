import requests
 
 
 # you can change the usd to eur or czk
out = requests.get("http://localhost:5000/msi-geforce-gtx-1650-ventus-xs-d6-4g-4gb-gddr6/311812/usd").text
print(out)
