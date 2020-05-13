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

$('#delete-shorturl-form').on('submit', function (){
    try {
        let url = $(this).attr('action');
        $('.short-code-' + short_code).remove();
        if($('#tbody-shorturls').children().length === 0){
            $('#table-shorturls').remove();
            $('#hidden-shorturl-advice').removeClass('invisible').addClass('visible')
        }
        $('#delete-item-modal').modal('hide');

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

        return false;
    }
    catch (e) {
        console.log(e);
        return false;
    }
});

