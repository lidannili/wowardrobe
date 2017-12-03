    // Load the Visualization API and the piechart package.
    google.charts.load('current', {
    	'packages': ['corechart']
    });

    // Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
    	$.get("/wowardrobe/get_category_count")
    		.done(function(jsonData) {
    			if (jsonData != null && jsonData.length > 0) {
    				var arrData = [];
    				var count = 0;
    				var categoryHTML = "<div>You have ";
    				jsonData.forEach(function(e) {
    					if (e.category != "") {
    						arrData.push([e.category, e.count]);
    						count = count + e.count;
    						var link = "#" + e.category.toLowerCase() + "-overview";
    						if (e.category == "Dress") {
    							categoryHTML += e.category + ": &nbsp;" + e.count + ", &nbsp; &nbsp;";
    						} else {
    							categoryHTML += "<a href=" + link + " class='link'>" + e.category + "</a>: &nbsp;" + e.count + ", &nbsp; &nbsp;";
    						}
    					}
    				});
    				categoryHTML += "<a href='#category-text' class='link'>Total:</a> &nbsp;" + count + "</div>";
    				$("#category-text").html(categoryHTML);
    				var data = new google.visualization.arrayToDataTable(arrData, true);
    				var chart = new google.visualization.PieChart(document.getElementById('category-pie-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
    					colors: ['#d67c98','#ed769c', '#e05e87', '#ce1c54', '#b70b41', '#f6c7b6'],
    					pieHole: 0.4
    				});
    				// draw column chart
    				data = new google.visualization.arrayToDataTable(arrData.slice(0, 5), true);
    				var chart2 = new google.visualization.ColumnChart(document.getElementById('category-column-chart'));
    				chart2.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
    					animation: {
    						duration: 500,
    						easing: 'out',
    						startup: true
    					},
                        colors: ['#d67c98'],
                        legend:{position:'none'}
    				});
    			}
    		});

    	$.get("/wowardrobe/get_top_count")
    		.done(function(jsonData) {
    			if (jsonData != null && jsonData.length > 0) {
    				var arrData = [];
    				jsonData.forEach(function(e) {
    					arrData.push([e.tagname, e.count]);
    				});
    				// draw pie chart
    				var data = new google.visualization.arrayToDataTable(arrData, true);
    				var chart = new google.visualization.PieChart(document.getElementById('top-pie-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
                        colors: ['#865df7','#7c50f4', '#5e35ce', '#4b2ba5', '#371f7a'],
    					pieHole: 0.4
    				});
    				// draw column chart
    				data = new google.visualization.arrayToDataTable(arrData.slice(0, 5), true);
    				chart = new google.visualization.ColumnChart(document.getElementById('top-column-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
    					animation: {
    						duration: 500,
    						easing: 'out',
    						startup: true
    					},
                        colors: ['#865df7'],
                        legend:{position:'none'}
    				});
    			}
    		});

    	$.get("/wowardrobe/get_bottom_count")
    		.done(function(jsonData) {
    			if (jsonData != null && jsonData.length > 0) {
    				var arrData = [];
    				jsonData.forEach(function(e) {
    					arrData.push([e.tagname, e.count]);
    				});
    				var data = new google.visualization.arrayToDataTable(arrData, true);
    				var chart = new google.visualization.PieChart(document.getElementById('bottom-pie-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
                        colors: ['#8afc96', '#7ae285', '#6ecc78', '#539b5b', '#3c7042'],
    					pieHole: 0.4
    				});
    				// draw column chart
    				data = new google.visualization.arrayToDataTable(arrData.slice(0, 5), true);
    				chart = new google.visualization.ColumnChart(document.getElementById('bottom-column-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
    					animation: {
    						duration: 500,
    						easing: 'out',
    						startup: true
    					},
                        colors: ['#8afc96'],
                        legend:{position:'none'}
    				});
    			}
    		});

    	$.get("/wowardrobe/get_shoes_count")
    		.done(function(jsonData) {
    			if (jsonData != null && jsonData.length > 0) {
    				var arrData = [];
    				jsonData.forEach(function(e) {
    					arrData.push([e.tagname, e.count]);
    				});
    				var data = new google.visualization.arrayToDataTable(arrData, true);
    				var chart = new google.visualization.PieChart(document.getElementById('shoes-pie-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
                        colors: ['#85f3f7', '#74dce0', '#62bec1', '#53a0a3', '#3f7a7c'],
    					pieHole: 0.4
    				});
    				// draw column chart
    				data = new google.visualization.arrayToDataTable(arrData.slice(0, 5), true);
    				chart = new google.visualization.ColumnChart(document.getElementById('shoes-column-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
    					animation: {
    						duration: 500,
    						easing: 'out',
    						startup: true
    					},
                        colors: ['#8afc96'],
                        legend:{position:'none'}
    				});
    			}
    		});

    	$.get("/wowardrobe/get_color_count")
    		.done(function(jsonData) {
    			if (jsonData != null && jsonData.length > 0) {
    				var arrData = [];
    				var favColor = "";
    				jsonData.forEach(function(e) {
    					if(e.count == jsonData[0].count) {
    						favColor += e.tagname + ", ";
    					}
    					arrData.push([e.tagname, e.count]);
    				});
    				favColor = favColor.substring(0,favColor.length-2);
    				var colorHTML = "Your favorite <a href='#color-overview' class='link'>Color</a> is <span class='bold-font'>" + favColor + "</span>";
    				$("#color-text").html(colorHTML);
    				var data = new google.visualization.arrayToDataTable(arrData, true);
    				var chart = new google.visualization.PieChart(document.getElementById('color-pie-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
                        colors: ['#7984fc', '#6972db', '#585fb7', '#43488e', '#313468'],
    					pieHole: 0.4
    				});
    				// draw column chart
    				data = new google.visualization.arrayToDataTable(arrData.slice(0, 5), true);
    				chart = new google.visualization.ColumnChart(document.getElementById('color-column-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
    					animation: {
    						duration: 500,
    						easing: 'out',
    						startup: true
    					},
                        colors: ['#7984fc'],
                        legend:{position:'none'}
    				});
    			}
    		});

    	$.get("/wowardrobe/get_brand_count")
    		.done(function(jsonData) {
    			if (jsonData != null && jsonData.length > 0) {
    				var arrData = [];
    				var favBrand = "";
    				jsonData.forEach(function(e) {
    					if(e.count == jsonData[0].count) {
    						favBrand += e.tagname + ", ";
    					}
    					arrData.push([e.tagname, e.count]);
    				});
    				favBrand = favBrand.substring(0, favBrand.length-2);
    				var brandHTML = "Your favorite <a href='#brand-overview' class='link'>Brand</a> is <span class='bold-font'>" + favBrand + "</span>";
    				$("#brand-text").html(brandHTML);
    				var data = new google.visualization.arrayToDataTable(arrData, true);
    				var chart = new google.visualization.PieChart(document.getElementById('brand-pie-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
                        colors: ['#c3f29d', '#b1f27d', '#a1ef62', '#79cc37', '#5caa1e'],
    					pieHole: 0.4
    				});
    				// draw column chart
    				data = new google.visualization.arrayToDataTable(arrData.slice(0, 5), true);
    				chart = new google.visualization.ColumnChart(document.getElementById('brand-column-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
    					animation: {
    						duration: 500,
    						easing: 'out',
    						startup: true
    					},
                        colors: ['#c3f29d'],
                        legend:{position:'none'}
    				});
    			}
    		});

    	$.get("/wowardrobe/get_style_count")
    		.done(function(jsonData) {
    			if (jsonData != null && jsonData.length > 0) {
    				var arrData = [];
    				var favStyle = "";
    				jsonData.forEach(function(e) {
    					if(e.count == jsonData[0].count) {
    						favStyle += e.tagname + ", ";
    					}
    					arrData.push([e.tagname, e.count]);
    				});
    				favStyle = favStyle.substring(0,favStyle.length-2);
    				var styleHTML = "Your favorite <a href='#style-overview' class='link'>Style</a> is <span class='bold-font'>" + favStyle + "</span>";
    				$("#style-text").html(styleHTML);
    				var data = new google.visualization.arrayToDataTable(arrData, true);
    				var chart = new google.visualization.PieChart(document.getElementById('style-pie-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
                        colors: ['#f9c2f5', '#f4abef', '#f791f0', '#f271e9', '#ef28e1'],
    					pieHole: 0.4
    				});
    				// draw column chart
    				data = new google.visualization.arrayToDataTable(arrData.slice(0, 5), true);
    				chart = new google.visualization.ColumnChart(document.getElementById('style-column-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
    					animation: {
    						duration: 500,
    						easing: 'out',
    						startup: true
    					},
                        colors: ['#f9c2f5'],
                        legend:{position:'none'}
    				});
    			}
    		});

    	$.get("/wowardrobe/get_event_count")
    		.done(function(jsonData) {
    			if (jsonData != null && jsonData.length > 0) {
    				var arrData = [];
    				var fav = "";
    				jsonData.forEach(function(e) {
    					if(e.count == jsonData[0].count) {
    						fav += e.tagname + ", ";
    					}
    					arrData.push([e.tagname, e.count]);
    				});
    				fav = fav.substring(0,fav.length-2);
    				var eventHTML = "You have most clothes for <a href='#event-overview' class='link'>Event</a>: <span class='bold-font'>" + fav + "</span>";
    				$("#event-text").html(eventHTML);
    				var data = new google.visualization.arrayToDataTable(arrData, true);
    				var chart = new google.visualization.PieChart(document.getElementById('event-pie-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
                        colors: ['#e0440e', '#e6693e', '#ec8f6e', '#f3b49f', '#f6c7b6'],
    					pieHole: 0.4
    				});
    				// draw column chart
    				data = new google.visualization.arrayToDataTable(arrData.slice(0, 5), true);
    				chart = new google.visualization.ColumnChart(document.getElementById('event-column-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
    					animation: {
    						duration: 500,
    						easing: 'out',
    						startup: true
    					},
                        colors: ['#e0440e'],
                        legend:{position:'none'}
    				});
    			}
    		});

    	$.get("/wowardrobe/get_season_count")
    		.done(function(jsonData) {
    			if (jsonData != null && jsonData.length > 0) {
    				var arrData = [];
    				var fav = "";
    				jsonData.forEach(function(e) {
    					if(e.count == jsonData[0].count) {
    						fav += e.tagname + ", ";
    					}
    					arrData.push([e.tagname, e.count]);
    				});
    				fav = fav.substring(0,fav.length-2);
    				var seasonHTML = "You have most clothes for <a href='#season-overview' class='link'>Season</a>: <span class='bold-font'>" + fav + "</span>";
    				$("#season-text").html(seasonHTML);
    				var data = new google.visualization.arrayToDataTable(arrData, true);
    				var chart = new google.visualization.PieChart(document.getElementById('season-pie-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
                        colors: ['#efea86', '#e8e053', '#f7ed3b', '#f9ed09'],
    					pieHole: 0.4
    				});
    				// draw column chart
    				data = new google.visualization.arrayToDataTable(arrData.slice(0, 5), true);
    				chart = new google.visualization.ColumnChart(document.getElementById('season-column-chart'));
    				chart.draw(data, {
    					width: 400,
    					height: 240,
    					backgroundColor: "transparent",
    					animation: {
    						duration: 500,
    						easing: 'out',
    						startup: true
    					},
                        colors: ['#efea86'],
                        legend:{position:'none'}
    				});
    			}
    		});

    }