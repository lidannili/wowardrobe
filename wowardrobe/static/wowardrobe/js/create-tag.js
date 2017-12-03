   $(document).ready(function() {
     $('.addColorTag button').click(function() {
       var inp = $(this).val();
       $('#colorTags').tagit('createTag', inp);
       return false;
     });
     $('.addCategoryTag button').click(function() {
       var inp = $(this).val();
       $('#categoryTags').tagit('createTag', inp);
       return false;
     });
     $('.addSeasonTag button').click(function() {
       var inp = $(this).val();
       $('#seasonTags').tagit('createTag', inp);
       return false;
     });
     $('.addEventTag button').click(function() {
       var inp = $(this).val();
       $('#eventTags').tagit('createTag', inp);
       return false;
     });
     $('.addBrandTag button').click(function() {
       var inp = $(this).val();
       $('#brandTags').tagit('createTag', inp);
       return false;
     });
     $('.addTempTag button').click(function() {
       var inp = $(this).val();
       $('#tempTags').tagit('createTag', inp);
       return false;
     });
     $('.addWeatherTag button').click(function() {
       var inp = $(this).val();
       $('#weatherTags').tagit('createTag', inp);
       return false;
     });
     $('.addStyleTag button').click(function() {
       var inp = $(this).val();
       $('#styleTags').tagit('createTag', inp);
       return false;
     });
     $('#reset-form').click(function() {
       $('#tempTags').tagit('removeAll');
       $('#brandTags').tagit('removeAll');
       $('#eventTags').tagit('removeAll');
       $('#seasonTags').tagit('removeAll');
       $('#colorTags').tagit('removeAll');
       $('#categoryTags').tagit('removeAll');
       $('#weatherTags').tagit('removeAll');
       $('#styleTags').tagit('removeAll');
     });
     $('#colorTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "color",
       afterTagAdded: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).addClass("disabled");
         }
       },
       afterTagRemoved: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).removeClass("disabled");
         }
       }
     });
     $('#categoryTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "category",
       tagLimit: 1,
       readOnly: true,
       afterTagAdded: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).addClass("disabled");
         }
       },
       afterTagRemoved: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).removeClass("disabled");
         }
       }
     });
     $('#eventTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "event",
       afterTagAdded: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).addClass("disabled");
         }
       },
       afterTagRemoved: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).removeClass("disabled");
         }
       }
     });
     $('#seasonTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "season",
       afterTagAdded: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).addClass("disabled");
         }
       },
       afterTagRemoved: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).removeClass("disabled");
         }
       }
     });
     $('#brandTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "brand",
       tagLimit: 1,
       afterTagAdded: function(event, ui) {
         var id = "#" + ui.tagLabel.replace(/[&]+/g, "-").toLowerCase() + "-tag";
         if ($(id).length > 0 && $(id).val().toLowerCase() == ui.tagLabel.toLowerCase()) {
           $(id).addClass("disabled");
         }
       },
       afterTagRemoved: function(event, ui) {
         var id = "#" + ui.tagLabel.replace(/[&]+/g, "-").toLowerCase() + "-tag";
         if ($(id).length > 0 && $(id).val().toLowerCase() == ui.tagLabel.toLowerCase()) {
           $(id).removeClass("disabled");
         }
       }
     });
     $('#tempTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "temp",
       tagLimit: 1,
      beforeTagAdded: function(event, ui){
        if(ui.tag > 6 || ui.tag < 1) {
          alert("Invalid temperature level. Enter number from 1 to 6.");
          return false;
        }
      },
       afterTagAdded: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).addClass("disabled");
         }
       },
       afterTagRemoved: function(event, ui) {
         var id = "#" + ui.tagLabel + "-tag";
         if ($(id).length > 0) {
           $(id).removeClass("disabled");
         }
       }
     });

     $('#weatherTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "weather",
       afterTagAdded: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).addClass("disabled");
         }
       },
       afterTagRemoved: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).removeClass("disabled");
         }
       }
     });
     $('#styleTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "style",
       afterTagAdded: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).addClass("disabled");
         }
       },
       afterTagRemoved: function(event, ui) {
         var id = "#" + ui.tagLabel.toLowerCase() + "-tag";
         if ($(id).length > 0) {
           $(id).removeClass("disabled");
         }
       }
     });

        $('#reset-form').click(function(){
        $('#tempTags').tagit('removeAll');
        $('#brandTags').tagit('removeAll');
        $('#eventTags').tagit('removeAll');
        $('#seasonTags').tagit('removeAll');
        $('#colorTags').tagit('removeAll');
        $('#categoryTags').tagit('removeAll');
        $('#weatherTags').tagit('removeAll');
        $('#styleTags').tagit('removeAll');
       });

     $("#add-tag-form").submit(function(eventObj) {
       $('<input />').attr('type', 'hidden')
         .attr('name', "clothes_name")
         .attr('value', $("#image-name").val())
         .appendTo('#add-tag-form');
      $('<input />').attr('type', 'hidden')
         .attr('name', "clothes_id")
         .attr('value', $("#upload-widget").data().clothes_id)
         .appendTo('#add-tag-form');
       return true;
     });

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
   });