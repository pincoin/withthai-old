/* left side bar for mobile */
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('#mobile-menu');
    var instances = M.Sidenav.init(elems, {});
});

/* right side bar for mobile */
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('#mobile-cart');
    var instances = M.Sidenav.init(elems, {'edge': 'right'});
});
