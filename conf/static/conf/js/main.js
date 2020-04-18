$('document').ready(function () {
});

$(window).on('load resize', function () {
    if ($(this).width() < 960) {
        var h = $(window).height();

        // 38x7=266, 38x8=304
        $('.submenu-scroll').css({'max-height': h - 228, 'min-height': h - 228});
    }
});
