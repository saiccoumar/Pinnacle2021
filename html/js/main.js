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

    // Fetch JSON
    $.getJSON('test.json', function(data) {
        var item = '';

        // Go through JSON
        $.each(data.items, function(key, value) {
            item += '<tr><td>'+value.correlation+'</td><td>'+value.frequency+'</td><td>'+value.productID+'</td>';
        })
        $('#dataResult').append(item)
    })
});