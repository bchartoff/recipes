function getQueryString(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}
var iso8601DurationRegex = /(-)?P(?:([.,\d]+)Y)?(?:([.,\d]+)M)?(?:([.,\d]+)W)?(?:([.,\d]+)D)?T(?:([.,\d]+)H)?(?:([.,\d]+)M)?(?:([.,\d]+)S)?/;

function parseISO8601Duration(iso8601Duration) {
    var matches = iso8601Duration.match(iso8601DurationRegex);

    return {
        sign: matches[1] === undefined ? '+' : '-',
        years: matches[2] === undefined ? 0 : matches[2],
        months: matches[3] === undefined ? 0 : matches[3],
        weeks: matches[4] === undefined ? 0 : matches[4],
        days: matches[5] === undefined ? 0 : matches[5],
        hours: matches[6] === undefined ? 0 : matches[6],
        minutes: matches[7] === undefined ? 0 : matches[7],
        seconds: matches[8] === undefined ? 0 : matches[8]
    };
};


d3.json("data/schema/" + getQueryString("recipe")).then(function(data){
	console.log(data)

	var tags = data.recipeCategory.split(", ")
		.concat(
			data.keywords.split(", ")
		)
		.sort(function(a,b){
			var tagA = a.toUpperCase(); // ignore upper and lowercase
			var tagB = b.toUpperCase(); // ignore upper and lowercase
			if (tagA < tagB) {
				return -1;
			}
			if (tagA > tagB) {
				return 1;
			}

			// tags must be equal
			return 0;

		})

	var timeObj = parseISO8601Duration(data.totalTime),
		hours = timeObj.hours,
		minutes = timeObj.minutes,
		timeString,
		suffix;
	// if(timeObj.hours == 0)
	// console.log(timeObj.minutes, timeObj.hours)
	if(hours == 0){
		suffix = (minutes == "1") ? "" : "s"
		timeString = minutes + " minute" + suffix
	}
	else if(minutes == 0){
		suffix = (hours == "1") ? "" : "s"
		timeString = hours + " hour" + suffix
	}else{
		suffixM = (minutes == "1") ? "" : "s"
		suffixH = (minutes == "1") ? "" : "s"

		timeString = hours +" hour" + suffixH + " and " + minutes + " minute" + suffixM
	}

	d3.select("#recipeTitle").html(data.name)
	d3.select("#recipeAuthor").html(data.author.name)

	d3.select("#summaryYield").html("<span class=\"smallLabel\">Yield</span>" + data.recipeYield)
	d3.select("#summaryTime").html("<span class=\"smallLabel\">Time</span>" + timeString)
	

	d3.select("#recipeDescription").html(data.description)
	d3.select("#recipeImage")
		.append("img")
		.attr("src", data.image)

	var tag = d3.select("#tags").selectAll(".tag")
		.data(tags)
		.enter()
		.append("div")
		.attr("class","tag")
	tag.append("a")
		.attr("href", function(d){ return "index.html?search=" + d })
		.attr("target", "_blank")
		.text(function(d){ return d })


	var ingredients = data.recipeIngredient
	var steps = data.recipeInstructions.map(function(o){ return o.text })

	d3.select("#ingredients")
		.selectAll(".ingredient")
		.data(ingredients)
		.enter()
		.append("li")
		.attr("class","ingredient")
		.html(function(d){ return d.replace("http://cooking.nytimes.com/recipes/","recipe.html?recipe=") + ".json" })

	var step = d3.select("#steps")
		.selectAll(".step")
		.data(steps)
		.enter()
		.append("li")
		.attr("class","step")
		
	step.append("div")
		.attr("class", "stepHead")
		.text(function(d,i){ return "Step " + (i+1)})
	step.append("div")
		.attr("class","stepText")
		.html(function(d){ return d })



})