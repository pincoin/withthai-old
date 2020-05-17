$(window).on('load resize', function () {
    if ($(this).width() < 960) {
        var h = $(window).height();

        // 40x7=280, 40x8=320 + 4(border)
        $('.submenu-scroll').css({'max-height': h - 284 , 'min-height': h - 284});
    }
});

$(document).ready(function () {
    $('#language-selector').on('change', function (e) {
        this.form.submit();
    });

    $(window).on("scroll", function () {
        var wn = $(window).scrollTop();
        if (wn > 20) {
            $(".navbar").css("box-shadow", "0 10px 5px -2px rgba(0,0,0,0.2)").css("transition-duration", "0.1s");
        } else {
            $(".navbar").css("box-shadow", "none");
        }
    });

    $('#icon-burger').on('click', function() {
        $('#left-sidebar').addClass('is-active');
        $('html').addClass('is-clipped');
    });

    $('.modal-background').on('click', function() {
        $('#left-sidebar').removeClass('is-active');
        $('html').removeClass('is-clipped');
    });
});
