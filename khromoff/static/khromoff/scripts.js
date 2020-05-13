let short_code;
$(document).ready( function () {
    $(document.getElementsByClassName('pointer-on-hover')).on('click', function () {
        short_code = $($(this).children()[2]).children()[0].textContent;
        $('#redirect-url').text($(this).children()[0].textContent);
        $('#redirect-count').text($(this).children()[1].textContent);
        $('#short_code_val').attr('value', short_code);

        $('#delete-item-modal').modal('show');
    });

});

$('#delete-shorturl-form').on('submit', function (qualifiedName, value){
    try {
        let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        let url = $(this).attr('action');
        $.ajax(url, {
            method: 'GET',
            xhrFields: {
                withCredentials: true
            },
            data: $(this).serialize(),
            headers: {"Content-Type": "application/json",
                        'X-Requested-With': 'XMLHttpRequest',
                        'Access-Control-Allow-Origin': '*'},
        }
        );
        $('.short-code-' + short_code).remove();
        console.log($('#tbody-shorturls').length);
        if($('#tbody-shorturls').children().length === 0){
            $('#table-shorturls').remove();
            $('#hidden-shorturl-advice').removeAttr('hidden')
        }
        $('#delete-item-modal').modal('hide');

        // TODO: sliding up the thing


        return false;
    }
    catch (e) {
        console.log(e);
        return false;
    }
});

