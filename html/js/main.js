$(window).scroll(function(e){
    // Keep searh bar at top
    var isPositionFixed = ($('.search').css('position') == 'fixed');
    var triggerHeight = $('.landing').height();
    var paddingHeight = $('.search').height();

    if ($(this).scrollTop() > triggerHeight && !isPositionFixed){ 
        $('.search').css({'position': 'fixed', 'top': '0px'});
        $('.stickyAdjust').css({'padding-top': paddingHeight});
    }
    if ($(this).scrollTop() < triggerHeight && isPositionFixed){
        $('.search').css({'position': 'static', 'top': '0px'}); 
        $('.stickyAdjust').css({'padding-top': '0px'});
    } 
});

function updateRateNum(val) {
    $('#ratingNum').html(val);
}

$(function() {

    // Add data entry modal
    var addModal = new bootstrap.Modal($('#addModal'));
    $('#addBtn').on({
        click: function() {
            addModal.show();
        }
    });

    // Rating range update
    $('#rating').on('input', function() {
        val = 
        $('#ratingNum').html($('#rating').val());
    })

    // Fetch JSON
    $('#searchBtn').on({
        click: function() {
            $.getJSON('test.json', function(data) {
                var item = '';
        
                // Go through JSON
                $.each(data.items, function(key, value) {
                    item += '<tr><td>'+value.correlation+'</td><td>'+value.frequency+'</td><td>'+value.productID+'</td>';
                })
                $('#dataResult').append(item)
            })
        }
    })
    
    /*
    $('#guess').on('input', function() {
        if ($('#guess').val()) {
            //prevents empty query to sqlite
            $.get("/autocomplete/" + $('#guess').val(), function(data) { //sends GET request to server returning {'data':[...]}
                var results = "";
                data['data'].forEach((result) => { results += <div class="result">
            <p>${result}</p></div>; }); //inserts div for each matching anime from database
                $('.search-results').html(results); //updates html
                $('.search-results').show(); //shows if it is hidden
            });
        } else {
            $('.search-results').hide(); //if empty query, hide search results just in case
        }
    }); */
});