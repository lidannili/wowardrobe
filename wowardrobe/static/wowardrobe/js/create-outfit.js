  var n = 1;
  // var color = d3.scaleOrdinal()
  //   .domain(d3.range(n))
  //   .range(d3.schemeCategory20c);

  var color = d3.scaleOrdinal(["#fcd2a6", "#ffbe7a", "#fca84e", "#fc890f", "#f96c00", "#f45f40"]);

  var margin = {
      top: 0,
      right: 10,
      bottom: 0,
      left: 10
    },
    width = 614; //+svg.attr("width"),
  height = 426; //+svg.attr("height");

  var x, y, series, g, rect, pie;

  $(document).ready(function($) {
    var count = 0;
    var max_temp_level = 0;

    $(".outfit_top").click(function(e) {
      var temp_level = $(e.currentTarget).data('temp_level');
      var style = $(e.currentTarget).data('style');
      var id = $(e.currentTarget).data('id');
      var event = $(e.currentTarget).data('event');
      $("#outfit-top1").attr('src', this.src);
      $("#outfit-top1").addClass("outfit-remove");
      $("#removelink-top1").show();
      $("#outfit-top1").data('temp_level', temp_level);
      $("#outfit-top1").data('id', id);
      $("#outfit-top1").data('style', style);
      $("#outfit-top1").data('event', event);
      updateValue(getTempLevel());
      updatePieValue(getData("style"), false);
    });

    $(".outfit_outwear").click(function(e) {
      var temp_level = $(e.currentTarget).data('temp_level');
      var style = $(e.currentTarget).data('style');
      var id = $(e.currentTarget).data('id');
      var event = $(e.currentTarget).data('event');
       $("#outfit-top2").attr('src', this.src);
       $("#outfit-top2").addClass("outfit-remove");
       $("#removelink-top2").show();
       $("#outfit-top2").data('temp_level', temp_level);
       $("#outfit-top2").data('id', id);
       $("#outfit-top2").data('style', style);
       $("#outfit-top2").data('event', event);
      updateValue(getTempLevel());
      updatePieValue(getData("style"), false);
    });

    $(".outfit_bottom").click(function(e) {
      var temp_level = $(e.currentTarget).data('temp_level');
      var style = $(e.currentTarget).data('style');
      var id = $(e.currentTarget).data('id');
      var event = $(e.currentTarget).data('event');
      $("#outfit-bottom1").attr('src', this.src);
      $("#outfit-bottom1").addClass("outfit-remove");
      $("#removelink-bottom1").show();
      $("#outfit-bottom1").data('temp_level', temp_level);
      $("#outfit-bottom1").data('id', id);
      $("#outfit-bottom1").data('style', style);
      $("#outfit-bottom1").data('event', event);
      updateValue(getTempLevel());
      updatePieValue(getData("style"), false);
    });
    $(".outfit_shoes").click(function(e) {
      var temp_level = $(e.currentTarget).data('temp_level');
      var style = $(e.currentTarget).data('style');
      var id = $(e.currentTarget).data('id');
      var event = $(e.currentTarget).data('event');
      $("#outfit-bottom2").attr('src', this.src);
      $("#outfit-bottom2").addClass("outfit-remove");
      $("#removelink-bottom2").show();
      $("#outfit-bottom2").data('temp_level', temp_level);
      $("#outfit-bottom2").data('id', id);
      $("#outfit-bottom2").data('style', style);
      $("#outfit-bottom2").data('event', event);
      updateValue(getTempLevel());
      updatePieValue(getData("style"), false);
    });
    $(".outfit_dress").click(function(e) {
      var temp_level = $(e.currentTarget).data('temp_level');
      var style = $(e.currentTarget).data('style');
      var id = $(e.currentTarget).data('id');
      var event = $(e.currentTarget).data('event');
      $("#outfit-dress").attr('src', this.src);
      $("#outfit-dress").addClass("outfit-remove");
      $("#removelink-dress").show();
      $("#outfit-dress").data('temp_level', temp_level);
      $("#outfit-dress").data('id', id);
      $("#outfit-dress").data('style', style);
      $("#outfit-dress").data('event', event);
      updateValue(getTempLevel());
      updatePieValue(getData("style"), false);
    });

    $("#saveoutfit").click(function(e) {
      var top1Id = $("#outfit-top1").data('id');
      var top2Id = $("#outfit-top2").data('id');
      var bottomId = $("#outfit-bottom1").data('id');
      var shoesId = $("#outfit-bottom2").data('id');
      var dressId = $("#outfit-dress").data('id');
      var eventTags = $("#eventTags").tagit("assignedTags");
      var seasonTags = $("#seasonTags").tagit("assignedTags");
      var styleTags = $("#styleTags").tagit("assignedTags");
      var outfit_name = $("#outfit_name").val();
      $.post(window.location.origin + "/wowardrobe/upload_outfit", {
          "temperature_level": getTempLevel(),
          "styles": styleTags.toString(),
          "events": eventTags.toString(),
          "seasons": seasonTags.toString(),
          "top1": top1Id,
          "top2": top2Id,
          "bottom": bottomId,
          "shoes": shoesId,
          "dress": dressId,
          "name": outfit_name
        })
        .done(function(response) {
          $("#outfit-top1").attr('src', "/static/wowardrobe/img/top_holder.svg");
          $("#outfit-top2").attr('src', "/static/wowardrobe/img/coat_holder.svg")
          $("#outfit-bottom1").attr('src', "/static/wowardrobe/img/pants_holder.svg");
          $("#outfit-bottom2").attr('src', "/static/wowardrobe/img/shoes_holder.svg");
          $("#outfit-dress").attr('src', "/static/wowardrobe/img/dress_holder.svg");
          $("#removelink-top1").hide();
          $("#removelink-top2").hide();
          $("#removelink-bottom1").hide();
          $("#removelink-bottom2").hide();
          $("#removelink-dress").hide();
          var pieData = {
            label: "",
            value: 1,
            "color": "#cccccc"
          };
          updatePieValue(pieData, true);
          updateValue(0);
          $("#save_outfit").modal('hide');
        });
    });
    $("#search-btn").click(searchClothes);
 
    // render 
    initTempColumn();
    initPie();

    $("#removelink-top1").click(function(){
      $("#outfit-top1").attr('src', "/static/wowardrobe/img/top_holder.svg");
      $("#outfit-top1").data('temp_level', -1);
      $("#outfit-top1").data('id', '');
      $("#outfit-top1").data('style', '');
      $("#removelink-top1").hide();
        updateValue(getTempLevel());
        updatePieValue(getData("style"), false);
    });
    $("#removelink-top2").click(function(){
      $("#outfit-top2").attr('src', "/static/wowardrobe/img/coat_holder.svg");
      $("#removelink-top2").hide();
      $("#outfit-top2").data('temp_level', -1);
      $("#outfit-top2").data('id', '');
      $("#outfit-top2").data('style', '');
        updateValue(getTempLevel());
        updatePieValue(getData("style"), false);
    });
    $("#removelink-bottom1").click(function(){
      $("#outfit-bottom1").attr('src', "/static/wowardrobe/img/pants_holder.svg");
      $("#removelink-bottom1").hide();
      $("#outfit-bottom1").data('temp_level', -1);
      $("#outfit-bottom1").data('id', '');
      $("#outfit-bottom1").data('style', '');
      updateValue(getTempLevel());
      updatePieValue(getData("style"), false);
    });
    $("#removelink-bottom2").click(function(){
      $("#outfit-bottom2").attr('src', "/static/wowardrobe/img/shoes_holder.svg");
      $("#removelink-bottom2").hide();
      $("#outfit-bottom2").data('temp_level', -1);
      $("#outfit-bottom2").data('id', '');
      $("#outfit-bottom2").data('style', '');
      updateValue(getTempLevel());
      updatePieValue(getData("style"), false);
    });
    $("#removelink-dress").click(function(){
      $("#outfit-dress").attr('src', "/static/wowardrobe/img/dress_holder.svg");
      $("#removelink-dress").hide();
      $("#outfit-dress").data('temp_level', -1);
      $("#outfit-dress").data('id', '');
      $("#outfit-dress").data('style', '');
      updateValue(getTempLevel());
      updatePieValue(getData("style"), false);
    });

  });

  function getData(data) {
    var top1Level = $("#outfit-top1").data(data);
    var top2Level = $("#outfit-top2").data(data);
    var bottomLevel = $("#outfit-bottom1").data(data);
    var shoesLevel = $("#outfit-bottom2").data(data);
    var dressLevel = $("#outfit-dress").data(data);
    var resData = {};
    if (top1Level != null) {
      var resArr = top1Level.split(",");
      resArr.forEach(function(e) {
        if (e != "") {
          if (resData.hasOwnProperty(e)) {
            resData[e]++;
          } else {
            resData[e] = 1;
          }
        }
      });
    }
    if (top2Level != null) {
      var resArr = top2Level.split(",");
      resArr.forEach(function(e) {
        if (e != "") {
          if (resData.hasOwnProperty(e)) {
            resData[e]++;
          } else {
            resData[e] = 1;
          }
        }
      });
    }
    if (bottomLevel != null) {
      var resArr = bottomLevel.split(",");
      resArr.forEach(function(e) {
        if (e != "") {
          if (resData.hasOwnProperty(e)) {
            resData[e]++;
          } else {
            resData[e] = 1;
          }
        }
      });
    }
    if (shoesLevel != null) {
      var resArr = shoesLevel.split(",");
      resArr.forEach(function(e) {
        if (e != "") {
          if (resData.hasOwnProperty(e)) {
            resData[e]++;
          } else {
            resData[e] = 1;
          }
        }
      });
    }
    if (dressLevel != null) {
      var resArr = dressLevel.split(",");
      resArr.forEach(function(e) {
        if (e != "") {
          if (resData.hasOwnProperty(e)) {
            resData[e]++;
          } else {
            resData[e] = 1;
          }
        }
      });
    }
    return resData;
  }

  function getTempLevel() {
    var top1Level = $("#outfit-top1").data("temp_level");
    var top2Level = $("#outfit-top2").data("temp_level");
    var bottomLevel = $("#outfit-bottom1").data("temp_level");
    var shoesLevel = $("#outfit-bottom2").data("temp_level");
    var dressLevel = $("#outfit-dress").data("temp_level");
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

  function initTempColumn() {
    var m = 0; // The number of values per series.

    var xz = d3.range(m),
      yz = [
        [0]
      ]; //d3.range(n).map(function() { return [1]; }),
    y01z = d3.stack().keys(d3.range(n))(d3.transpose(yz)),
      yMax = 1,
      y1Max = 6;

    var svg = d3.select("svg");


    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .attr("clip-path", "url(#myClip)");

    x = d3.scaleBand()
      .domain(xz)
      .rangeRound([0, width])
      .padding(0.08);

    y = d3.scaleLinear()
      .domain([0, y1Max])
      .range([height, 0]);

    series = g.selectAll(".series")
      .data(y01z)
      .enter().append("g")
      .attr("fill", function(d, i) {
        return color(i);
      })
      .attr("transform", "translate(-50, 40)");

    rect = series.selectAll("rect")
      .data(function(d) {
        return d;
      })
      .enter().append("rect")
      .attr("x", function(d, i) {
        return x(i);
      })
      .attr("y", height)
      .attr("width", x.bandwidth())
      .attr("height", 0);

    rect.transition()
      .delay(function(d, i) {
        return i * 100;
      })
      .attr("y", function(d) {
        return y(d[1]);
      })
      .attr("height", function(d) {
        return y(d[0]) - y(d[1]);
      });
  }

  function updateValue(temp_level) {
    var svg = d3.select("svg");
    series.remove();
    var xz = d3.range(temp_level);
    var yz = [];
    for (var i = 0; i < temp_level; i++) {
      yz.push([1]);
    }
    var y01z = d3.stack().keys(d3.range(temp_level))(d3.transpose(yz)),
      yMax = 1,
      y1Max = 6;
    series = g.selectAll(".series")
      .data(y01z)
      .enter().append("g")
      .attr("fill", function(d, i) {
        return color(i);
      })
      .attr("transform", "translate(-50, 40)");

    rect = series.selectAll("rect")
      .data(function(d) {
        return d;
      })
      .enter().append("rect")
      .attr("x", function(d, i) {
        return x(i);
      })
      .attr("y", height)
      .attr("width", x.bandwidth())
      .attr("height", 0);

    rect.transition()
      .delay(function(d, i) {
        return i * 200;
      })
      .attr("y", function(d) {
        return y(d[1]);
      })
      .attr("height", function(d) {
        return y(d[0]) - y(d[1]);
      });
  }


  function initPie() {
    pie = new d3pie("pieChart", {
      header: {
        title: {
          text: "Style"
        }
      },
      size: {
        "canvasWidth": 260,
        "canvasHeight": 250,
        "pieOuterRadius": "70%"
      },
      data: {
        content: [{
          label: "",
          value: 1,
          "color": "#cccccc"
        }]
      },
      labels: {
        "outer": {
          "pieDistance": 5
        },
        "mainLabel": {
          "fontSize": 11
        },
        "lines": {
          "enabled": true
        },
        "truncation": {
          "enabled": false
        }
      },
    });
  }

  function updatePieValue(styleData, isClear) {
    var data = [];
    if(isClear) {
      data.push(styleData);
    } else {
      for (var prop in styleData) {
        data.push({
          label: prop,
          value: styleData[prop]
        });
      }
    }
    if (data.length == 0) {
      data = [{
          label: "",
          value: 1,
          "color": "#cccccc"
        }];    
    }
    pie.updateProp("data.content", data);
  }

  function searchClothes() {
    var tags = $("#searchTags").tagit("assignedTags");
    $.get(window.location.origin + "/wowardrobe/clothes_search?tags=" + tags)
      .done(function(data) {
        var searchDiv = $("#search_results");
        searchDiv.html('');
        data.results.forEach(function(d){
          var div = $("<div></div>").addClass("col-md-4").css("margin-bottom", "10px");
          var thumbnailDiv = $("<div></div>").addClass("thumbnail").attr("id", d.id);
          var imgHTML = "<img  src=/wowardrobe/get_image/" +  d.id + "  class='clothes-img search_results'/>";
          var imgdom = $(imgHTML);
          var category = d.category.toLowerCase();
          if (category.indexOf('top') > -1) {
            category = "top";
          } else if(category.indexOf('outwear') > -1) {
            category = "outwear";
          } else if(category.indexOf('bottom') > -1) {
            category = "bottom";
          } else if(category.indexOf("shoes") > -1) {
            category = "shoes";
          } else if(category.indexOf("dress") > -1) {
            category = "dress";
          }
          imgdom.data("id", d.id);
          imgdom.data("temp_level", d.temperature_level);
          imgdom.data("category", category);
          imgdom.data("style", d.style);
          thumbnailDiv.append(imgdom);
          div.append(thumbnailDiv);
          searchDiv.append(div);
        });
        $('.nav-tabs a[href="#menu5"]').tab('show');
        $(".search_results").click(function(e) {
          var category = $(e.currentTarget).data('category');
          var temp_level = $(e.currentTarget).data('temp_level');
          var style = $(e.currentTarget).data('style');
          var id = $(e.currentTarget).data('id');
          var divId = "#outfit-";

          if(category.indexOf("top") > -1) {
           $("#removelink-top1").show();
           divId = divId + "top1";
          } else if(category.indexOf("outwear") > -1) {
            $("#removelink-top2").show();
            divId = divId + "top2";
          } else if(category.indexOf("bottom") > -1) {
            $("#removelink-bottom1").show();
            divId = divId + "bottom1";
          } else if(category.indexOf("shoes") > -1) {
            $("#removelink-bottom2").show();
            divId = divId + "bottom2";
          } else if (category.indexOf("dress") > -1) {
            $("#removelink-dress").show();
            divId = divId + "dress";
          }
          $(divId).attr('src', this.src);
          $(divId).addClass("outfit-remove");
          $(divId).data('temp_level', temp_level);
          $(divId).data('id', id);
          $(divId).data('style', style);
          updateValue(getTempLevel());
          updatePieValue(getData("style"), false);
        });
      });
  }

  function openModal(){
    var outfitStyle = getData("style");
    var styles = [];
    for(var key in outfitStyle) {
        if (outfitStyle.hasOwnProperty(key)) {
          styles.push([key, outfitStyle[key]]);
        }
    }
    styles.sort(function(a, b){
      return b[1] - a[1];
    });
    $('#styleTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "styles",
       singleField: true
    });
    var len = Math.min(styles.length, 5);
    for(var i = len-1; i >= 0; i--) {
      $("#styleTags").tagit("createTag", styles[i][0]);
    }

    var eventData = getData("event");
    var events = [];
    for(var key in eventData) {
        if (eventData.hasOwnProperty(key)) {
          events.push([key, eventData[key]]);
        }
    }
    events.sort(function(a, b){
      return b[1] - a[1];
    });
    $('#eventTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "events",
       singleField: true
    });
    var len = Math.min(events.length, 5);
    for(var i = len - 1; i >= 0; i--) {
      $("#eventTags").tagit("createTag", events[i][0]);
    }
    $('#seasonTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "seasons",
       singleField: true
    });
    var tempData = getTempLevel();
    var seasons = [];
    if(tempData == 1) {
      seasons.push('Summer');
    } else if(tempData >=2 && tempData <= 3) {
      seasons.push('Spring', 'Summer', 'Fall');
    } else if(tempData >=3 && tempData <=4) {
      seasons.push('Winter', 'Spring', 'Fall');
    } else {
      seasons.push('Winter');
    }
    seasons.forEach(function(e){
      $("#seasonTags").tagit("createTag", e);
    });
    $('#save_outfit').modal("show");
  }


  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });