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

    $('.js-edit-button').click(function () {
        $(this).closest(':has(.js-editable-info-area)').find('.js-editable-info-area').addClass('d-none');
        $('#' + $(this).attr('js-edit-area-id')).removeClass('d-none');
    });
    $('.js-editable-stop-edit-button').on('click', function() {
        $(this).closest(':has(.js-editable-info-area)').find('.js-editable-info-area').removeClass('d-none');
        $(this).closest(".js-editable-edit-area").addClass('d-none');
    });
});

