function getExpand() {
	var budget = $("#budget").val();
	var brandTags = $("#brandTags").tagit("assignedTags");
	var colorTags = $("#colorTags").tagit("assignedTags");
	var categoryTags = $("#categoryTags").tagit("assignedTags");
  var url = window.location.origin + "/wowardrobe/get_clothes_by_budget?budget=" + budget;

  if(brandTags.length > 0) {
    url += "&brand=" + brandTags;
  }
  if(colorTags.length > 0) {
    url += "&color=" + colorTags;
  }
  if(categoryTags.length > 0) {
    url += "&category=" + categoryTags;
  }
  $.get(url)
  .done(function(data) {
    var html = '';
    var div = $("#shopstyle-result");
    div.html('');
    data['data'].forEach(function(d){
    	html += '<div class="col-lg-3 col-md-4 col-xs-6"><a href="' + d.clickUrl + '" class="d-block mb-4 h-100"><img class="img-fluid img-thumbnail" src="' + d.imageUrl + '" alt="' + d.name + '"><small>' + d.price + '</small></a></div>'
    });
    div.html(html);
  });
}

function reset() {
    $('#brandTags').tagit('removeAll');return false;
    $('#colorTags').tagit('removeAll');return false;
    $('#categoryTags').tagit('removeAll');return false;
}

function shuffle() {
    $( "#expend-form" ).submit();

}