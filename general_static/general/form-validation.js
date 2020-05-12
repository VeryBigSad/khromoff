$(document).ready(function() {

    window.addEventListener('load', function () {
        const forms = document.getElementsByClassName('novalidate-form');
        const validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');

            }, false);
        });
    }, false);


});


