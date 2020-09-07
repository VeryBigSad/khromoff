btn = document.getElementById('shorturl-copy');

new ClipboardJS('.btn-success');

$(function () {
    $('[data-toggle="tooltip"]').tooltip({title: 'Скопировать'})
});


$('#shorturl-copy').click(function () {
    $('#shorturl-copy').tooltip('dispose').tooltip({title: 'Успешно скопированно!'}).tooltip('show');
    setTimeout(function () {
        $('#shorturl-copy').tooltip('dispose').tooltip({title: 'Скопировать'}).tooltip('show');
    }, 5000);
});






