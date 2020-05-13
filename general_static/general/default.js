let do_open = true;

$('#bug-report').on('click', (function () {
    if (do_open) {
        $('#report-modal').modal();
    }
}));

$('#bug-report-form').on('submit', function(){

    $("<input />").attr("type", "hidden")
        .attr("name", "location")
        .attr("value", window.location.href)
        .appendTo("#bug-report-form");

    $.post($(this).attr('action'), $(this).serialize(), function(response){
    },'json');

    do_open = false;
    $('#report-modal').modal('hide');
    $('#bug-report-flag').addClass('fas').removeClass('far');
    $('#bug-report-text').html('Спасибо за помощь!').parent().attr('id', 'thanks-for-help');
    return false;
});
