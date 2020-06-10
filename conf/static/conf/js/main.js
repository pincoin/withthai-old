$(window).on('load resize', function () {
    if ($(this).width() < 960) {
        var h = $(window).height();

        // 40x7=280, 40x8=320 + 4(border)
        // 40+56+40+44 = 180
        $('.submenu-scroll').css({'max-height': h - 180 , 'min-height': h - 180});
    }
});

$(document).ready(function () {
    $('#language-selector, #language-selector-mobile').on('change', function (e) {
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
        $('#left-sidebar').addClass('is-active').animate({"left":"0%"}, 3000);
        $('html').addClass('is-clipped');
    });

    $('#icon-search').on('click', function() {
        $('#right-sidebar').addClass('is-active').animate({"left":"0%"}, 3000);
        $('html').addClass('is-clipped');
    });

    $('.modal-background, #left-sidebar-close, #right-sidebar-close').on('click', function() {
        $('#left-sidebar').animate({"left":"-100%"}, 3000, function(){ $(this).removeClass('is-active')  });
        $('#right-sidebar').animate({"left":"-100%"}, 3000,function(){ $(this).removeClass('is-active')  });
        $('html').removeClass('is-clipped');
    });
});
