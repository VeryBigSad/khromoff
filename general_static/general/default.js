let do_open = true;

$('#bug-report').on('click', (function () {
    if (do_open) {
        $('#report-modal').modal();
    }
}));

$('#report-modal').on('hidden.bs.modal', function (e) {
    $('#bug-report-flag').addClass('fas').removeClass('far');
    $('#bug-report-text').html('Спасибо за помощь!').parent().attr('id', 'thanks-for-help');
});

$('#bug-report-form').on('submit', function(){

    $("<input />").attr("type", "hidden")
        .attr("name", "location")
        .attr("value", window.location.href)
        .appendTo("#bug-report-form");
    $.post($(this).attr('action'), $(this).serialize(), function(response){
    },'json');
    $('#report-modal').modal('hide');
    do_open = false;
    return false;
});
