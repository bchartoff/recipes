import json
import sys
import os.path
from os import path
import requests
from bs4 import BeautifulSoup

recipePaths = []
invalidUrls = []

def get_ld_json(recipePath):
	filename = recipePath.replace("/recipes/","")
	url = "https://cooking.nytimes.com" + recipePath
	parser = "html.parser"
	req = requests.get(url)
	soup = BeautifulSoup(req.text, parser)
	ldJson = soup.find("script", {"type":"application/ld+json"})
	if(ldJson == None):
		print("No ld+json recipe data found for %s"%url)
		invalidUrls.append(url)
	else:
		recipe = json.loads("".join(ldJson.contents))

		with open("data/schema/nyt/%s.json"%filename,"w") as f:
			json.dump(recipe, f)

def getrecipePathsFromPage(num):
	print("getting recipe recipePaths for search result page %i"%num)
	url = "https://cooking.nytimes.com/search?q=&page=%i"%num
	parser = "html.parser"
	req = requests.get(url)
	soup = BeautifulSoup(req.text, parser)

	cards = soup.find_all("article", class_="recipe-card")
	for card in cards:
		recipePaths.append(card["data-url"])

if("--full" in sys.argv):
	for num in range(1,423):
		getrecipePathsFromPage(num)
	with open('data/allRecipes.json', 'w') as f:
		json.dump(recipePaths, f)
	
else:
	with open('data/allRecipes.json') as f:
		recipePaths = json.load(f)
	

recipeCount = 0
for recipePath in recipePaths:
	recipeCount += 1

	if(path.exists("data/schema/nyt/%s.json"%(recipePath.replace("/recipes/","")))):
		continue
	else:
		print("getting ld+json for recipe number %i"%recipeCount)
		get_ld_json(recipePath)


with open('data/invalidUrls.json', 'w') as f:
	json.dump(invalidUrls, f)




