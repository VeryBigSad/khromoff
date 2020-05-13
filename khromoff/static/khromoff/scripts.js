let short_code;
let prefix;
$(document).ready( function () {
    $(document.getElementsByClassName('shorturl-item')).on('click', function () {
        short_code = $($(this).children()[2]).children()[0].textContent;
        $('#redirect-url').text($(this).children()[0].textContent);
        $('#redirect-count').text($(this).children()[1].textContent);
        $('#short_code_val').attr('value', short_code);

        $('#delete-item-modal').modal('show');
    });

    $(document.getElementsByClassName('delete-key-item')).on('click', function () {
        let thing = $(this.parentElement).children();
        prefix = $(thing[1]).text().trim();
        console.log(prefix);
        $('#apikey-name').text(thing[0].textContent);
        $('#apikey-prefix').text(prefix);
        $('#apikey-rights').html($(thing[2]).html());
        $('#apikey-rpm').text(thing[3].textContent);

        $('#prefix_val').attr('value', prefix);
        $('#delete-apikey-modal').modal('show');
    })

});

$('#delete-shorturl-form').on('submit', function (){
    try {
        let url = $(this).attr('action');
        $('.short-code-' + short_code).remove();
        if($('#tbody-shorturls').children().length === 0){
            $('#table-shorturls').remove();
            $('#hidden-shorturl-advice').setAttribute('hidden', '')
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


$('#delete-apikey-form').on('submit', function () {
    try {
        let url = $(this).attr('action');
        $('.prefix-' + prefix).remove();
        let childrens = $('#tbody-apikeys').children().length;
        if(childrens === 0){
            $('#table-apikeys').remove();
            $('#hidden-apikey-advice').removeClass('invisible').addClass('visible');
            document.getElementById('get-apikey-recommendation').hidden = true;
        } else if (0 < childrens < 5) {
            document.getElementById('get-apikey-recommendation').hidden = false;
            document.getElementById('5-keys-limit').hidden = true;

        }
        $('#delete-apikey-modal').modal('hide');

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
