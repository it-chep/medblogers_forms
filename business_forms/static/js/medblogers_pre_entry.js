$(document).ready(function () {
    $('.input_container input').each(function () {
        const $fieldInputContainer = $(this).closest('.field_inline_item_container');
        const $line = $(this).closest('.input_container').find('.line')
        if ($(this).length) {
            if ($(this).attr('type') === 'checkbox') {
                $(this).addClass('checkbox');
                $line.remove()
            }
        }
        const $fieldWarningContainer = $fieldInputContainer.find('.field_item_warning_container');
        $(this).on('blur', function () {

            if (!$(this).val() && $(this).prop('required')) {
                $fieldInputContainer.addClass('invalid');
                $line.addClass('invalid');
                $fieldWarningContainer.css('display', 'block');
            } else {
                $fieldInputContainer.removeClass('invalid')
                $line.removeClass('invalid');
                $fieldWarningContainer.css('display', 'none');
            }
        });

        $(this).on('input change', function () {
            $fieldInputContainer.removeClass('invalid')
            $line.removeClass('invalid');
            $fieldWarningContainer.css('display', 'none');
        });
    });

    $('#radio').click(function () {
        const $idPolicyAgreement = $('#id_policy_agreement');
        $idPolicyAgreement.prop('checked', true);

        const $fieldInputContainer = $(this).closest('.field_inline_item_container');
        const $fieldWarningContainer = $fieldInputContainer.find('.field_item_warning_container');
        $fieldInputContainer.removeClass('invalid');
        $fieldWarningContainer.css('display', 'none');
    });

    $('.submit_button').click(function () {

        let isValid = true;
        const formData = $('form').serialize();

        $('form input[required]').each(function () {
            const $fieldInputContainer = $(this).closest('.field_inline_item_container');
            const $line = $(this).closest('.input_container').find('.line');
            const $fieldWarningContainer = $fieldInputContainer.find('.field_item_warning_container');
            if (!$(this).val() && $(this).prop('required')) {
                $fieldInputContainer.addClass('invalid');
                $line.addClass('invalid');
                $fieldWarningContainer.css('display', 'block');
                isValid = false;
            } else {
                $fieldInputContainer.removeClass('invalid');
                $line.removeClass('invalid');
                $fieldWarningContainer.css('display', 'none');
            }
        });
        const $idPolicyPolicy = $('#id_policy_agreement')

        if ($idPolicyPolicy.prop('checked') !== true) {
            const $fieldInputContainer = $idPolicyPolicy.closest('.field_inline_item_container');
            const $fieldWarningContainer = $fieldInputContainer.find('.field_item_warning_container');
            $fieldInputContainer.addClass('invalid');
            $fieldWarningContainer.css('display', 'block');
            isValid = false;
        }

        formData["privacy_policy"] = $idPolicyPolicy.prop('checked')

        if (!isValid) {
            return
        }
        if (isValid) {
            $.ajax({
                type: 'POST',
                url: $('form').attr('action'),
                data: formData,
                dataType: 'json',
                success: function (response) {
                    if (response.success) {
                        window.location.href = response.redirect_url;
                    } else {
                        $.each(response.errors, function (field, errors) {
                            const $field = $('[name=' + field + ']');
                            const $fieldInputContainer = $field.closest('.field_inline_item_container');
                            const $fieldWarningContainer = $fieldInputContainer.find('.field_item_warning_container');
                            $fieldInputContainer.addClass('invalid');
                            $fieldWarningContainer.html('');
                            $fieldWarningContainer.html(errors.join('<br>')).css('display', 'block');
                        });
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Ошибка при отправке формы:', status, error);
                }
            });
        }
    });

    $('.clear_inline_container').click(function () {
        $('form')[0].reset();
        $('.input_container').removeClass('invalid');
    });
});