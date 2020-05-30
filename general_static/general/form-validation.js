$(document).ready(function() {

    window.addEventListener('load', function () {
        const forms = document.getElementsByClassName('novalidate-form');
        const validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                } else if ($.contains(form, document.getElementById('captcha'))) {
                    if (hcaptcha.getResponse() === "") {
                        event.preventDefault();
                        event.stopPropagation();
                        if (!$.contains(document.getElementsByClassName('errors')[0], document.getElementById('captcha-error'))) {
                            $('.errors').append('<div id="captcha-error" class="alert alert-danger col">Пожалуйста, введите капчу.</div>')
                        }
                    }
                }

                form.classList.add('was-validated');

            }, false);
        });
    }, false);


});


