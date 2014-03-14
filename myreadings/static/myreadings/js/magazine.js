function Magazine() {
		
	this.deleteMagazine = function(magazine_id) {
		var token = $("input[name=csrfmiddlewaretoken]").val();
		if ( confirm("Are you sure you want to delete this magazine?") ) {
			$.post("/myreadings/magazine/"+magazine_id+"/delete/", {'csrfmiddlewaretoken': token}, function(retData){location.reload(1);});
		}
	}
	
	this.searchNext = function() {
		var page = parseInt($("#page").val());
		var totPage = parseInt($("#total-page").val());
		if (page < totPage) {
			$("#page").val(page+1);
			$("#magazine-search").submit();
		}
	}
	this.searchPrev = function() {
		var page = parseInt($("#page").val());
		if (page > 1) {
			$("#page").val(page-1);
			$("#magazine-search").submit();
		}
	}
	// Resetting page (page=1) when clicking Search Button
	this.search = function() {
		$("#page").val(1);
		$("#magazine-search").submit();
	}
}

var m = new Magazine();

$(document).ready(function(){
	$("#magazine-form").validate({
		'rules': {
			'title': 'required',
			'page-count': 'number',
			'number': 'number',
			'published-date': 'number',
			'month': 'number',
		}, 
		'messages': {
			'title': '',
			'page-count': '',
			'number': '',
			'published-date': '',
			'month': '',
		}
	});
	$("#title").change(function(evt){
		$("#summary-title").text(evt.target.value);
	});
	$("#thumbnail").change(function(evt){
		$("#summary-thumbnail").attr("src", evt.target.value);
	});

});