function get_recommendation() {
	var day = $('input[name="day"]:checked').val();
	var event = $("#queryEventTags").tagit("assignedTags");
	var style = $("#queryStyleTags").tagit("assignedTags");
	var weatherCode = "";
	var weatherURL = "";
	if (day == 'today') {
		weatherCode = $('input[name="weatherCode1"]').val();
		weatherURL = "weatherCode1=" + weatherCode;
	} else {
		weatherCode = $('input[name="weatherCode2"]').val();
		weatherURL = "weatherCode2=" + weatherCode;
	}
	var url = window.location.origin + "/wowardrobe/get_recommendation_by_params?day=" + day+"&"+weatherURL;
	if(event.length > 0) {
		url += "&event=" + event;
	}
	if(style.length > 0) {
		url += "&style=" + style;
	}
  $.get(url)
  .done(function(data) {
    var html = '';
    var div = $("#search_result");
    div.html('');
    div.html(data.html);
  });
}



function getTempLevel() {
    var top1Level = $("[id^=clothes-top1-]")[0].data("temp_level");
    var top2Level = $("[id^=clothes-top2-]")[0].data("temp_level");
    var bottomLevel = $("[id^=clothes-bottom-]")[0].data("temp_level");
    var shoesLevel = $("[id^=clothes-shoes-]")[0].data("temp_level");
    var dressLevel = $("[id^=clothes-dress-]")[0].data("temp_level");
    var max_temp_level = 0;
    if (top1Level != null && top1Level > max_temp_level) {
      max_temp_level = top1Level;
    }
    if (top2Level != null && top2Level > max_temp_level) {
      max_temp_level = top2Level;
    }
    if (bottomLevel != null && bottomLevel > max_temp_level) {
      max_temp_level = bottomLevel;
    }
    if (shoesLevel != null && shoesLevel > max_temp_level) {
      max_temp_level = shoesLevel;
    }
    if (dressLevel != null && dressLevel > max_temp_level) {
      max_temp_level = dressLevel;
    }
    var max_count = 0;
    if (top1Level != null && top1Level == max_temp_level) {
      max_count++;
    }
    if (top2Level != null && top2Level == max_temp_level) {
      max_count++;
    }
    if (bottomLevel != null && bottomLevel == max_temp_level) {
      max_count++;
    }
    if (shoesLevel != null && shoesLevel == max_temp_level) {
      max_count++;
    }
    if (dressLevel != null && dressLevel == max_temp_level) {
      max_count++;
    }
    if (max_count > 1) {
      max_temp_level++;
    }
    return max_temp_level;
  }


$(document).ready(function($) {

	$.get("http://ip-api.com/json").done(function(response){
		$.get("http://api.openweathermap.org/data/2.5/forecast/daily?lat=" + response["lat"] + "&lon=" + response["lon"] + "&cnt=2&units=metric&appid=ea574594b9d36ab688642d5fbeab847e")
		.done(function(response) {
			if (response.list.length > 0) {
				var today = response.list[0];
				var tomorrow = response.list[1];
				var todayContext = today.weather[0].id + "," + today.temp.min + "," + today.temp.max;
				var tomorrowContext = tomorrow.weather[0].id + "," + tomorrow.temp.min + "," + tomorrow.temp.max;
				$("#weather-code1").val(todayContext);
				$("#weather-code2").val(tomorrowContext);
			}
			window.myWidgetParam ? window.myWidgetParam : window.myWidgetParam = [];
			window.myWidgetParam.push({
				id: 11,
				cityid: '5206379',
				appid: 'ea574594b9d36ab688642d5fbeab847e',
				units: 'metric',
				containerid: 'openweathermap-widget-11',
			});
			 (function() {var script = document.createElement('script');script.async = true;script.charset = "utf-8";script.src = "https://openweathermap.org/themes/openweathermap/assets/vendor/owm/js/weather-widget-generator.js";var s = document.getElementsByTagName('script')[0];s.parentNode.insertBefore(script, s);  })();
		});

});
	
	$.get(window.location.origin + "/wowardrobe/get_event_tags")
		.done(function(data) {
			$('#queryEventTags').tagit({
				allowSpaces: true,
				caseSensitive: false,
				fieldName: "event",
				singleField: true,
				autocomplete: {
					delay: 0,
					minLength: 2
				},
				availableTags: data
			});
		});

	$.get(window.location.origin + "/wowardrobe/get_style_tags")
		.done(function(data) {
			$('#queryStyleTags').tagit({
				allowSpaces: true,
				caseSensitive: false,
				fieldName: "style",
				singleField: true,
				autocomplete: {
					delay: 0,
					minLength: 2
				},
				availableTags: data
			});
		});
});