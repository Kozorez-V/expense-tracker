let field = document.querySelector('#date')

if (field) {
    date.addEventListener('input', function () {
        let date = new Date(field.value);
        console.log(date);
    });
};