import os,json, isodate, time, sys
from stat import S_ISREG, ST_CTIME, ST_MODE

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



# # dir_path = path_to_json
# # get all entries in the directory
# entries = (os.path.join(path_to_json, file_name) for file_name in os.listdir(path_to_json))
# # Get their stats
# entries = ((os.stat(path), path) for path in entries)
# # leave only regular files, insert creation date
# entries = ((stat[ST_CTIME], path)
#            for stat, path in entries if S_ISREG(stat[ST_MODE]))
# print(entries)
import glob
import os

files = glob.glob(path_to_json + "*.json")
files.sort(key=os.path.getmtime)
# print(files)


for file_name in files:
	if(file_name.find(".json") == -1):
		continue

	with open(file_name) as json_file:

		data = json.load(json_file)

		rating = "" if data["aggregateRating"] == None else float(data["aggregateRating"]["ratingValue"])

		duration = "" if "totalTime" not in data else isoDurationToString(data["totalTime"])
		# print(rating)
		recipe = {"json": file_name.replace(path_to_json,""),"name":data["name"], "description": data["description"], "author": data["author"]["name"], "image": data["image"], "duration": duration, "servings": data["recipeYield"], "cuisine": data["recipeCuisine"], "categories": data["recipeCategory"].split(", "), "keywords": data["keywords"], "rating": rating }
		# print(file_name)
		out.append(recipe)

with open('data/recipes.js', 'w') as f:
	f.write("recipes=")
	json.dump(out, f)	
