import os,json, isodate

path_to_json = 'data/schema/'

out = []

def isoDurationToString(isoDuration):
	timeDelta = isodate.parse_duration(isoDuration)
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

for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
	with open(path_to_json + file_name) as json_file:
		data = json.load(json_file)

		rating = "" if data["aggregateRating"] == None else float(data["aggregateRating"]["ratingValue"])
		duration = "" if "totalTime" not in data else isoDurationToString(data["totalTime"])

		recipe = {"json": file_name,"name":data["name"], "description": data["description"], "author": data["author"]["name"], "image": data["image"], "duration": duration, "servings": data["recipeYield"], "cuisine": data["recipeCuisine"], "categories": data["recipeCategory"].split(", "), "keywords": data["keywords"], "rating": rating }

		out.append(recipe)


with open('data/streaming_recipes.json', 'w') as f:
	json.dump(out, f)
with open('data/recipes.js', 'w') as f:
	f.write("recipes=")
	json.dump(out, f)
