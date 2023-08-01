$(document).ready(function() {
    $('.sub-nav-activator').hover(function() {
        $(this).find('.sub-nav').first().slideDown("easeOutBounce");
    }).mouseleave(function() {
        if ($(this).find('.sub-nav').first().is(':hover')) {
            $(this).find('.sub-nav').first().mouseleave(function() {
                $(this).slideUp(500);
            });
        } else {
            $(this).find('.sub-nav').first().slideUp(500);
        }
    });
});
