function Book() {
    this.getBookInfo = function() {
        var url = "https://www.googleapis.com/books/v1/volumes";
        var isbn = $("#isbn").val();
        var query = "isbn:"+isbn;
        if ( !isNaN(isbn) && isbn.length == 13) {
            // Loading Page
            // First Request, get a Google Books ID
            $.get(url, {'q': query}, function(retData){
                var rd = retData;
                if (rd.totalItems != 1) {
                    alert('An error occured parsing data.\n Please try later or insert manually.');
                } else {
                    gid = rd.items[0].id;
                    // Second Request, get all info
                    var url2 = url+"/"+gid;
                    $.get(url2, {}, function(retData){
                        var book = retData;
                        $("#google-id").val(book.id);
                        $("#isbn-id").val(isbn);
                        $("#title").val(book.volumeInfo.title);
                        $("#author").val(book.volumeInfo.authors.join(", "));
                        $("#publisher").val(book.volumeInfo.publisher);
                        $("#published-date").val(book.volumeInfo.publishedDate);
                        $("#description").val(book.volumeInfo.description)
                        $("#page-count").val(book.volumeInfo.pageCount);
                        if ('imageLinks' in book.volumeInfo) $("#thumbnail").val(book.volumeInfo.imageLinks.thumbnail);
                        $("#book-form input.update").each(function(ind, el){$(el).change();})
                    });
                }
            })
        } else {
            alert("Please insert a valid ISBN number.")
        }
    }
    
    this.deleteBook = function(book_id) {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        if ( confirm("Are you sure you want to delete this book?") ) {
            $.post("/myreadings/book/"+book_id+"/delete/", {'csrfmiddlewaretoken': token}, function(retData){location.reload(1);});
        }
    }
    
    this.searchNext = function() {
        var page = parseInt($("#page").val());
        var totPage = parseInt($("#total-pages").val());
        if (page < totPage) {
            $("#page").val(page+1);
            $("#book-search").submit();
        }
    }
    this.searchPrev = function() {
        var page = parseInt($("#page").val());
        if (page > 1) {
            $("#page").val(page-1);
            $("#book-search").submit();
        }
    }
    // Resetting page (page=1) when clicking Search Button
    this.search = function() {
        $("#page").val(1);
        $("#book-search").submit();
    }
    this.filter = function() {
        $("#page").val(1);
        var year = $("#rr-year").val();
        var month = $("#rr-month").val();
        var url = "/myreadings/book/read/";
        if (year != "all") {
            url += year+"/";
            if (month != "all")
                url += month+"/";
        }
        location.href=url;
    }
    this.filterNext = function() {
        var page = parseInt($("#page").val());
        var totPage = parseInt($("#total-pages").val());
        if (page < totPage) {
            location.href = location.href.split("?")[0] + "?page="+(page+1); 
        }
    }
    this.filterPrev = function() {
        var page = parseInt($("#page").val());
        if (page > 1) {
            location.href = location.href.split("?")[0] +  "?page="+(page-1);
        }
    }
    
    /* AJAX Functions */    
    this.showReadRateBook = function(book_id, el) {
        $('tr.readrate').removeClass("readrate");
        $(el).parents('tr').addClass("readrate");
        $("#read-rate-table").html("");
        var token = $("input[name=csrfmiddlewaretoken]").val();
        data = { 'csrfmiddlewaretoken': token, 'book_id': book_id };
        $.post('/myreadings/book/ajax/getreadrate/', data, function(responseData){
            var rd = JSON.parse(responseData);
            if (rd.status == 0) {
                $("#book-id").val(book_id);
                $("#read-rate-book-panel").slideDown();
                $("#search-book-panel").slideUp();
                for (ii=0; ii<rd.rr_list.length; ii++){
                    var rr = rd.rr_list[ii];
                    var rate = '';
                    var del = '<a onclick="javascript:b.deleteReadRateBook('+rr.id+', this)"><span class="glyphicon glyphicon-remove"></span></a>'; 
                    for (jj=0; jj<rr.rate; jj++)
                        rate += '<span class="glyphicon glyphicon-star"></span> '
                    var row = '<tr><td class="datetime">'+rr.year+'/'+rr.month+'</td><td class="rate">'+rate+'</td><td class="delete">'+del+'</td></tr>';
                    $("#read-rate-table").append(row);
                }
            }
        });
    }
    
    this.hideReadRateBook = function() {
        $('tr.readrate').removeClass("readrate");
        $("#read-rate-book-panel").slideUp();
        $("#search-book-panel").slideDown();
    }
    
    this.readRateBook = function() {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        data = {
            'csrfmiddlewaretoken': token,
            'book_id': $("#book-id").val(),
            'year': $("#rr-year").val(),
            'month': $("#rr-month").val(),
            'rate': $("#rr-rate").val(),
        }
        $.post('/myreadings/book/ajax/readrate/', data, function(responseData){
            var rd = JSON.parse(responseData);
            if (rd.status == 0) {
                // Change R&R star
                $("tr.readrate .read-rate span").removeClass("glyphicon-star-empty").addClass("glyphicon-star");
                b.hideReadRateBook();
            }
            else
                alert(rd.message);
        });
    }
    this.deleteReadRateBook = function(readRateId, el) {
        var token = $("input[name=csrfmiddlewaretoken]").val();
        data = {
            'csrfmiddlewaretoken': token,
            'readrate_id': readRateId,
        }
        $.post('/myreadings/book/ajax/readrate/delete/', data, function(responseData){
            var rd = JSON.parse(responseData);
            if (rd.status == 0) {
                $(el).parents('tr').remove();
                // Change R&R star
                if ($("#read-rate-table tr").length == 0)
                    $("tr.readrate .read-rate span").removeClass("glyphicon-star").addClass("glyphicon-star-empty");
            }
            else
                alert(rd.message);
        });
    }
    
}

var b = new Book();

$(document).ready(function(){
    $("#book-form").validate({
        'rules': {
            'title': 'required',
            'page-count': 'number',
        }, 
        'messages': {
            'title': '',
            'page-count': '',
        }
    });
    $("#book-info-btn").click(b.getBookInfo);
    $("#book-info-help").popover({
        placement: 'bottom',
        trigger: 'hover',
        content: 'Insert ISBN number and contact Google Books API to complete Books Information. Please consider that if a match is find all your compiled data will be overwritten',
    });
    $("#title").change(function(evt){
        $("#summary-title").text(evt.target.value);
    });
    $("#author").change(function(evt){
        $("#summary-author").text(evt.target.value);
    });
    $("#thumbnail").change(function(evt){
        $("#summary-thumbnail").attr("src", evt.target.value);
    });

});
