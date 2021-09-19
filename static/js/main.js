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
    $('#searchFormPearson').submit()
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

    // Slider to toggle between modes
    $('#toggleSVDTxt').css('opacity', 0.6);
    $('#toggler').click(function() {
        if($(this).prop('checked') == true) {
            $('#togglePearsonTxt').css('opacity', 0.6);
            $('#toggleSVDTxt').css('opacity', 1.0);
            $('.landing').css('background-color', '#FFAD9B');
            $('a').css('color', '#ff0000');
            $('.search').css('background-color', '#6F1400');
            $('.svd').show();
            $('.pearson').hide();
        } else if($(this).prop('checked') == false) {
            $('#toggleSVDTxt').css('opacity', 0.6);
            $('#togglePearsonTxt').css('opacity', 1.0);
            $('.landing').css('background-color', '#ffbd95');
            $('a').css('color', '#ff8040');
            $('.search').css('background-color', '#623100');
            $('.pearson').show();
            $('.svd').hide();
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
                    $('.searchDrop').fadeOut();
                } else {
                    $('.searchDrop').html(results);
                    $('.searchDrop').fadeIn();
                }
            });
        } else {
            // Empty search
            $('.searchDrop').html('<span class="d-block pt-1 pb-1">Must enter exact search query!</span>');
        }
    });

    // Focus dropdown visibility
    $('#search').focusout(function() {
        setTimeout(function() {
            $('.searchDrop').fadeOut();
        }, 250)
    })
    $('#search').focusin(function() {
        $('.searchDrop').fadeIn();
    })

    // Search Pearson form AJAX submission
    $('#enterDataSVD').submit(function(event) {
        // Prevent normal submission
        event.preventDefault();

        $.get('/querySVD/'+$('#search').val(), function(data) {
            $('#dataResult').html('');
            console.log(data);
            var item = '';
        
            // Go through JSON
            $.each(data.items, function(key, value) {
                item += '<div class="col text-center"><p>User ID: '+value.userID+'</p><h1>'+value.affinity+'</h1><p class="opacity-50">Affinity Score</p></div>';
            })
            $('#svdResults').append(item)
        })
    });

    // SVD enter data AJAX submission

});