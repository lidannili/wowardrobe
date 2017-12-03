$(document).ready(function($) {
      $.get(window.location.origin + "/wowardrobe/get_tags")
            .done(function(data) {
                  $('#searchTags').tagit({
                        allowSpaces: true,
                        caseSensitive: false,
                        fieldName: "tags",
                        singleField: true,
                        autocomplete: {delay: 0, minLength: 2},
                        availableTags: data.tags
                  });
            });


});