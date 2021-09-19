// Keep searh bar at top
$(window).scroll(function(e){
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

// Update rating number
function updateRateNum(val) {
    $('#ratingNum').html(val);
}

// Dropdown fill search on click
function fillSearch(val) {
    $('#search').val(val);
}

// Window loads
$(function() {
    // DBZ Easter Egg
    $('#easterEgg').on({
        click: function() {
            $('#easterEgg').hide();
            $('#dbz').show();
        }
    });

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
    // $('#searchBtn').on({
    //     click: function() {
    //         $.getJSON('test.json', function(data) {
    //             var item = '';
        
    //             // Go through JSON
    //             $.each(data.items, function(key, value) {
    //                 item += '<tr><td>'+value.correlation+'</td><td>'+value.frequency+'</td><td>'+value.productID+'</td>';
    //             })
    //             $('#dataResult').append(item)
    //         })
    //     }
    // })
    
    // Search autocomplete
    $('#search').on('input', function() {
        if ($('#search').val()) {
            $('.searchDrop').html('<span class="d-block pt-1 pb-1">Searching suggestions...</span>');
            // Prevent empty query to SQLite
            $.get('/autocomplete/' + $('#search').val(), function(data) { // Sends GET request to server returning {'data':[...]}
                var results = '';
                data['data'].forEach((result) => {
                    results += '<span class="d-block pt-1 pb-1 searchDropItem" onclick="fillSearch(\''+result+'\')">'+result+'</span>';
                });

                // Blank if results match to avoid empty dropdown
                if(results === '') {
                    $('.searchDrop').hide();
                } else {
                    $('.searchDrop').html(results);
                    $('.searchDrop').show();
                }
            });
        } else {
            // Empty search
            $('.searchDrop').html('<span class="d-block pt-1 pb-1">Start typing!</span>');
        }
    });

    // Focus dropdown visibility
    $('#search').focusout(function() {
        setTimeout(function() {
            $('.searchDrop').hide();
        }, 250)
    })
    $('#search').focusin(function() {
        $('.searchDrop').show();
    })

    // Search form AJAX submission
    $('#searchForm').submit(function(event) {
        // Prevent normal submission
        event.preventDefault();

        $.get('/query/'+$('#search').val(), function(data) {
            console.log(data);
            var item = '';
        
            // Go through JSON
            $.each(data.items, function(key, value) {
                item += '<tr><td>'+value.productID+'</td><td>'+value.frequency+'</td><td>'+value.correlation+'</td>';
            })
            $('#dataResult').append(item)
        })
    });
});