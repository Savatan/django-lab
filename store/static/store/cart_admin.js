// Помечает строки неактивных корзин классом cart-inactive.
// Неактивную корзину определяем по зачёркнутому тексту "(неактивна)".
document.addEventListener('DOMContentLoaded', function () {
    var rows = document.querySelectorAll('#result_list tbody tr');
    rows.forEach(function (row) {
        if (row.textContent.indexOf('(неактивна)') !== -1) {
            row.classList.add('cart-inactive');
        }
    });
});
