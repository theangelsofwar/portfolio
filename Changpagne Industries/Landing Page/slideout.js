$(document).ready(function () {
    $('.sldm-toggle, .sldm-overlay').on("click", function (e) {
        e.preventDefault();
        $('.sldm').toggleClass('sldm-active');
        $('.sldm-bg-image').toggleClass('active');
    });

    $('.sldm-submenu > a').on("click", function (e) {
        e.preventDefault();
        $(this).toggleClass('sldm-open');
        $(this).parent().find('>ul').slideToggle(450);
    });

    $('.sldm-widget-toggle').on("click", function (e) {
        e.preventDefault();
        $($(this).data('target')).slideToggle(300);
    });
});