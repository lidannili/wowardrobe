
function searchClothes() {
    var tags = $('#searchTags').tagit('assignedTags');
    $.get("/wowardrobe/clothes_search?tags="+tags)
      .done(function(data) {
          var div = $("#search_results")
          div.html('')
          var result = data.results.html
          div.append(result)
      });
}



$(document).ready(function () {
  $("#search-btn").click(searchClothes)
  

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