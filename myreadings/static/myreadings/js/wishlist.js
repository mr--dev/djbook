function Wishlist() {
	
	this.deleteWish = function(wish_id) {
		var token = $("input[name=csrfmiddlewaretoken]").val();
		if ( confirm("Are you sure you want to delete this wish?") ) {
			$.post("/myreadings/wish/"+wish_id+"/delete/", {'csrfmiddlewaretoken': token}, function(retData){location.reload(1);});
		}
	}
	
}

var w = new Wishlist();

$(document).ready(function(){
	$("#wish-form").validate({
		'rules': {
			'title': 'required',
		}, 
		'messages': {
			'title': '',
		}
	});
});