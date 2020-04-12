import os,json, isodate, time, sys, glob

out = []

def isoDurationToString(isoDuration):
	try:
		timeDelta = isodate.parse_duration(isoDuration)
	except:
		return isoDuration
	hours, remainder = divmod(timeDelta.total_seconds(), 3600)
	minutes, seconds = divmod(remainder, 60)

	hours = int(hours)
	minutes = int(minutes)

	if(hours == 0):
		suffix = "" if minutes == 1.0 else "s"
		return "%i minute%s"%(minutes, suffix)
	elif(minutes == 0):
		suffix = "" if hours == 1.0 else "s"
		return "%i hour%s"%(hours, suffix)
	else:
		suffixM = "" if minutes == 1.0 else "s"
		suffixH = "" if hours == 1.0 else "s"

		return "%i hour%s and %i minute%s"%(hours, suffixH, minutes, suffixM)


def buildJs(source):
	path_to_json = 'data/schema/%s/'%source
	files = glob.glob(path_to_json + "*.json")
	files.sort(key=os.path.getmtime)

	for file_name in files:

		if(file_name.find(".json") == -1):
			continue

		with open(file_name) as json_file:

			data = json.load(json_file)

			if(source == "nyt"):
				link = "https://cooking.nytimes.com/recipes/" + file_name.replace(path_to_json,"").replace(".json","")
			elif(source == "sk"):
				link = "https://smittenkitchen.com/" + file_name.replace(path_to_json,"").replace("_","/").replace(".json","")
			elif(source == "se"):
				link = data["link"]

			data["link"] = link
			with open(file_name, 'w') as f:
				json.dump(data, f)	


			rating = "" if data["aggregateRating"] == None or data["aggregateRating"] == "" or data["aggregateRating"]["ratingValue"] == "" else float(data["aggregateRating"]["ratingValue"])

			duration = "" if "totalTime" not in data else isoDurationToString(data["totalTime"])
			# print(rating)
			if(source == "se"):
				categories = data["recipeCategory"]
			else:
				categories = data["recipeCategory"].split(", ")
			recipe = {"source": source, "json": file_name.replace(path_to_json,""),"name":data["name"], "description": data["description"], "author": data["author"]["name"], "image": data["image"], "duration": duration, "servings": data["recipeYield"], "cuisine": data["recipeCuisine"], "categories": categories, "keywords": data["keywords"], "rating": rating, "link": link}
			# print(file_name)
			out.append(recipe)




sources = ["nyt","sk","se"]
for source in sources:
	buildJs(source)

with open('data/recipes.js', 'w') as f:
	f.write("recipes=")
	json.dump(out, f)	
