$(document).ready(function() {
	   $('#colorTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "color"
     });
	   $('#categoryTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "category",
       tagLimit: 1
     });
     $('#brandTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "brand",
       tagLimit: 1
     });
     $('#eventTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "event"
     });
     $('#styleTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "style"
     });
     $('#seasonTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "season"
     });
     $('#weatherTags').tagit({
       allowSpaces: true,
       caseSensitive: false,
       fieldName: "weather"
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
       }
     });
});