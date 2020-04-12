import requests
import json
import re
import urllib

shortUrl="https://www.seriouseats.com/topics?index=recipes&count=1"
shortRequest=requests.get(shortUrl)
shortJson=json.loads(shortRequest.content)

total_entries = shortJson["total_entries"]
# total_entries = 100

url="https://www.seriouseats.com/topics?index=recipes&count=%i"%total_entries

request=requests.get(url)
entries=json.loads(request.content)["entries"]

for entry in entries:
	outRecipe = {}

	outRecipe["@context"] = "http://schema.org"
	outRecipe["@type"] = "Recipe"
	outRecipe["nutrition"] = {}

	tags = []
	for tag in entry["tags"]:
		if(tag[0] != "_"):
			tags.append(tag)

	categories = []
	cuisine = ""
	for category in entry["categories"]:
		if(category["url"].find("cuisine") != -1):
			cuisine = category["name"]
		categories.append(category["name"])

	aggregateRating = {"@type": "AggregateRating"}
	aggregateRating["ratingValue"] = entry["rating"]
	aggregateRating["ratingCount"] = entry["rating_count"]

	recipeInstructions = []
	for procedure in entry["procedures"]:
		recipeInstruction = {"@context": "http://schema.org","@type": "HowToStep"}
		recipeInstruction["text"] = procedure["text"]
		recipeInstructions.append(recipeInstruction)

	try:
		outRecipe["image"] = entry["assets"][0]["url"]
	except:
		outRecipe["image"] = ""
	# try:
	# 	assets = entry["assets"][0]
	# 	if("medium" in assets):
	# 		outRecipe["image"] = entry["assets"][0]["sizes"]["medium"]["url"]
	# 	elif("small" in assets):
	# 		outRecipe["image"] = entry["assets"][0]["sizes"]["small"]["url"]
	# 	else:
	# 		outRecipe["image"] = ""
	# except:
	# 	outRecipe["image"] = ""
	outRecipe["author"] = {'@type': "Person", "name": entry["author_name"]}
	outRecipe["recipeCuisine"] = cuisine
	outRecipe["keywords"] = tags
	outRecipe["aggregateRating"] = aggregateRating
	outRecipe["name"] =  entry["title"]
	outRecipe["link"] = entry["permalink"]
	outRecipe["description"] = entry["excerpt"]
	outRecipe["totalTime"] = entry["total_time"]
	outRecipe["recipeYield"] = entry["number_serves"]
	outRecipe["recipeCategory"] = categories
	outRecipe["recipeIngredient"] = entry["ingredients"]
	outRecipe["recipeInstructions"] = recipeInstructions

	recipeUrl = entry["permalink"]
	recipeSlug = recipeUrl.replace("https://www.seriouseats.com/recipes/","").replace(".html","").replace("/","_")

	with open("data/schema/se/%s.json"%recipeSlug,"w") as f:
		json.dump(outRecipe, f)
