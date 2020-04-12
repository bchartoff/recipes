import json
import sys
import os.path
import re
from os import path
import requests
from bs4 import BeautifulSoup



invalidUrls= ["https://smittenkitchen.com/2018/03/1940-2018/","https://smittenkitchen.com/2017/09/smitten-kitchen-every-day-trailer-book-tour/","https://smittenkitchen.com/2017/01/an-easier-way-to-make-cookies/","https://smittenkitchen.com/2017/01/the-smitten-kitchen-series-on-food-network/","https://smittenkitchen.com/2016/08/how-to-julienne/","https://smittenkitchen.com/2016/08/even-more-perfect-blueberry-muffins/","https://smittenkitchen.com/2016/07/welcome-to-the-shiny-new-smitten-kitchen-2-0/","https://smittenkitchen.com/2016/05/failproof-crepes-a-crepe-party/"]
recipePaths = []


def scrapeNewSk(soup):
	name = soup.find("", class_="jetpack-recipe-title").text
	description = "" if soup.find("", class_="jetpack-recipe-notes") == None else soup.find("", class_="jetpack-recipe-notes").text
	
	totalTime = None if soup.find("",{"itemprop" : "totalTime"}) == None else soup.find("",{"itemprop" : "totalTime"})["datetime"]
	recipeYield = soup.find("", class_="jetpack-recipe-servings").text.replace("Servings: ","")
	

	ingredientsSoup = soup.find_all("li", class_="jetpack-recipe-ingredient")
	author = soup.find("",class_="jetpack-recipe-source").text

	ingredients = []
	for ing in ingredientsSoup:
		ingredients.append(ing.text)

	stepDiv = soup.find("div", class_="jetpack-recipe-directions")
	stepFirst = stepDiv.previous
	
	recipeInstructions = []
	if(stepFirst.name != None):
	
		recipeInstructions.append({"@context": "http://schema.org", "@type": "HowToStep", "text": stepFirst.text })

		nextTest = stepDiv.next
		while True:
			# print(nextTest)
			if nextTest.name != "div":
				if nextTest.name == "p" and nextTest.text != "":
					recipeInstructions.append({"@context": "http://schema.org", "@type": "HowToStep", "text": nextTest.text })
				nextTest = nextTest.next
			else:
				break
	else:
		raise ValueError("Can't find first step in new scraper")

	scraped = {}
	scraped["name"] = name
	scraped["description"] = description
	scraped["totalTime"] = totalTime
	scraped["recipeYield"] = recipeYield
	scraped["ingredients"] = ingredients
	scraped["recipeInstructions"] = recipeInstructions
	scraped["author"] = {'@type': "Person", "name": author}

	return scraped

def scrapeOldSk(soup):
	printHide = soup.find("div",class_="smittenkitchen-print-hide")
	titleContainer = printHide.next_sibling.next_sibling
	if(titleContainer.name != "p"):
		raise ValueError('Title container not p tag')
	if(titleContainer.find("b") != None):
		name = titleContainer.find("b").text
	elif(titleContainer.find("strong") != None):
		name = titleContainer.find("b").text
	else:
		raise ValueError('Title container does not contain bold text')
	authorName = "Smitten Kitchen" if titleContainer.text.replace(name,"") == "" else titleContainer.text.replace(name,"")
	author = {'@type': "Organization", "name": authorName}

	desc = ""
	recipeYield = ""
	el = titleContainer
	while True:
		tmp = el.next_sibling.next_sibling

		if(tmp.find("br")):
			ingredientContainer = tmp
			break

		if(tmp.text.upper().find("YIELD") != -1 or tmp.text.upper().find("MAKES") != -1 or tmp.text.upper().find("SERV") != -1):
			recipeYield = tmp.text.replace("Yield:","").strip()
		else:
			desc += "<p>" + tmp.text + "</p>"
		el = tmp


	subHeadCount = 0
	ingredients = []
	el = ingredientContainer
	while True:
		ingredList = el.contents
		for i in ingredList:
			i = str(i)
			if(i.find("<u") != -1):
				subHeadCount += 1
				ingredients.append("RECIPE_SUBHED__%i%s"%(subHeadCount, i))
			elif(i.find("<br") == -1):
				ingredients.append(i.replace("\n",""))
		tmp = el.next_sibling.next_sibling
		if(tmp.find("br")):
			el = tmp
		else:
			break

	recipeInstructions = []
	while True:
		tmp = el.next_sibling.next_sibling
		if(el.name == "p"):
			recipeInstruction = {"@context": "http://schema.org","@type": "HowToStep","text":str(el)}
			recipeInstructions.append(recipeInstruction)
		else:
			break
		el = tmp


	scraped = {}
	scraped["name"] = name
	scraped["description"] = desc
	scraped["totalTime"] = ""
	scraped["recipeYield"] = recipeYield
	scraped["ingredients"] = ingredients
	scraped["recipeInstructions"] = recipeInstructions
	scraped["author"] = author

	return scraped


def getRecipeData(recipeUrl, recipeSlug, recipeThumb):
	if(recipeUrl in invalidUrls):
		return False
	print(recipeUrl)

	outRecipe = {}
	outRecipe["@context"] = "http://schema.org"
	outRecipe["@type"] = "Recipe"
	outRecipe["image"] = recipeThumb
	outRecipe["nutrition"] = {}

	url = recipeUrl
	parser = "html.parser"
	req = requests.get(url)
	soup = BeautifulSoup(req.text, parser)
	r = soup.find("div", class_="hrecipe")


	recipeCuisine = ""
	keywords = ""
	aggregateRating = ""

	recipeCategoryRaw = soup.find("article",class_="post")["class"]
	recipeCategories = []
	recipeCategory = ""
	for rc in recipeCategoryRaw:
		if rc.find("category-") != -1:
			recipeCategories.append(rc.replace("category-","").replace("-"," "))
	
	for i in range(0, len(recipeCategories)):
		sep = "" if i == len(recipeCategories) - 1 else ", "
		recipeCategory += recipeCategories[i] + sep

	if(soup.find("", class_="jetpack-recipe-title")	== None):
		try:
			scraped = scrapeOldSk(soup)
		except:
			invalidUrls.append(recipeUrl)
			return False
		# raise ValueError('Custom exit')
	else:
		try:
			scraped = scrapeNewSk(soup)
		except:
			invalidUrls.append(recipeUrl)
			return False



	outRecipe["recipeCuisine"] = recipeCuisine
	outRecipe["keywords"] = keywords
	outRecipe["aggregateRating"] = aggregateRating
	outRecipe["recipeCategory"] = recipeCategory
	

	outRecipe["name"] = scraped["name"]
	outRecipe["author"] = scraped["author"]
	outRecipe["description"] = scraped["description"]
	outRecipe["totalTime"] = scraped["totalTime"]
	outRecipe["recipeYield"] = scraped["recipeYield"]
	outRecipe["recipeIngredient"] = scraped["ingredients"]
	outRecipe["recipeInstructions"] = scraped["recipeInstructions"]

	with open("data/schema/sk/%s.json"%recipeSlug,"w") as f:
		json.dump(outRecipe, f)

def getrecipePathsFromPage(num):
	url = "https://smittenkitchen.com/page/%i/?s"%num
	parser = "html.parser"
	req = requests.get(url)
	soup = BeautifulSoup(req.text, parser)

	cards = soup.find_all("a", class_="smittenkitchen-thumbnail")
	# print(cards)
	if(cards == []):
		print("Page %i has no search results"%num)
		return None
	else:
		print("getting SK recipe recipePaths for search result page %i"%num)
	
	for card in cards:
		# print(card)	
		thumbnail = card.find("img")
		imgSrc = "" if thumbnail == None else thumbnail["src"]
		recipePaths.append( [card["href"], imgSrc])
	return True

if("--full" in sys.argv):
	num = 1
	while True:
		tester = getrecipePathsFromPage(num)
		num += 1
		if tester == None:
			break

	with open('data/build_script_output/sk/allRecipes.json', 'w') as f:
		json.dump(recipePaths, f)
	
else:
	with open('data/build_script_output/sk/allRecipes.json') as f:
		recipePaths = json.load(f)
	

# article = re.sub(r'(?is)</html>.+', '</html>', article)


recipeCount = 0
for recipePair in recipePaths:
	recipeUrl = recipePair[0]
	recipeSlug = re.sub(r'(\d\d\d\d)\/(\d\d)\/(.*)\/','\g<1>_\g<2>-\g<3>',recipeUrl.replace("https://smittenkitchen.com/",""))
	recipeThumb = recipePair[1]
	recipeCount += 1

	if(path.exists("data/schema/sk/%s.json"%recipeSlug)):
		continue
	else:
		print("getting SK ld+json for recipe number %i"%recipeCount)
		getRecipeData(recipeUrl, recipeSlug, recipeThumb)


with open('data/build_script_output/sk/invalidUrls.json', 'w') as f:
	json.dump(invalidUrls, f)




