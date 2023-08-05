$(document).ready(function() {
    $('.js-edit-button').click(function () {
        $(this).closest(':has(.js-editable-info-area)').find('.js-editable-info-area').addClass('d-none');
        $('#' + $(this).attr('js-edit-area-id')).removeClass('d-none');
    });
    $('.js-editable-stop-edit-button').on('click', function() {
        $(this).closest(':has(.js-editable-info-area)').find('.js-editable-info-area').removeClass('d-none');
        $(this).closest(".js-editable-edit-area").addClass('d-none');
    });
});

