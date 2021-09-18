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