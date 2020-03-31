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

$('document').ready(function() {
   $('#navbar-search1').on('click', function() {
       $('#navbar-top-right').hide();
       $('#navbar-search-box').show();
   });

   $('#search-close').on('click', function() {
       $('#navbar-top-right').show();
       $('#navbar-search-box').hide();
   });
});