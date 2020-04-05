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

$('document').ready(function () {
    $('#navbar-search1').on('click', function () {
        $('#navbar-top-right').hide();
        $('#navbar-search-box1').show();
    });

    $('#navbar-search-close1').on('click', function () {
        $('#navbar-top-right').show();
        $('#navbar-search-box1').hide();
    });

    $('#navbar-search2').on('click', function () {
        $(this).hide();
        $('.brand-logo').hide();
        $('#navbar-search-box2').show();
    });

    $('#navbar-search-close2').on('click', function () {
        $('#navbar-search2').show();
        $('.brand-logo').show();
        $('#navbar-search-box2').hide();
    });

});

$(window).on('load resize', function () {
    if ($(this).width() < 992) {
        var h = $(window).height();

        // 38x7=266, 38x8=304
        $('.submenu-scroll').css({'max-height': h - 228, 'min-height': h - 228});
    }
});