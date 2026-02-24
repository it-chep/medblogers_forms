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

    $('.input_container textarea').each(function () {
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

    // Обработчик изменения checkbox кнопок для occupation
    $('input[name="checkbox-occupation"]').change(function () {
        const $container = $(this).closest('.field_inline_item_container');

        // Сбрасываем ошибки при любом изменении
        $container.removeClass('invalid')
            .find('.field_item_warning_container').hide();

        const $input = $('#id_occupation');
        if ($(this).val() === 'another') {
            if ($(this).prop('checked')) {
                $input.prop('disabled', false).focus();
            } else {
                $input.val('').prop('disabled', true);
            }
        }
    });

    // Обработчик изменения самого инпута occupation
    $('#id_occupation').on('input change', function () {
        const $container = $(this).closest('.field_inline_item_container');
        const $anotherCheckbox = $('#checkbox_occupation_another');
        if ($(this).val().trim()) {
            $anotherCheckbox.prop('checked', true);
            $container.removeClass('invalid')
                .find('.field_item_warning_container').hide();
        }
    });

    // Обработчик ввода текста в поле "Другое" для чекбоксов
    $('.another-input').on('input', function () {
        const $checkbox = $(this).closest('.many-checkbox-button').find('input[type="checkbox"]');
        const $fieldContainer = $(this).closest('.field_inline_item_container');

        if ($(this).val().trim()) {
            $checkbox.prop('checked', true);
            $fieldContainer.removeClass('invalid')
                .find('.field_item_warning_container').hide();
        }
    });

    $('.submit_button').click(function (e) {
        e.preventDefault();

        const $button = $(this);

        $button.css({'opacity': '0.7', 'pointer-events': 'none'});
        $button.find('.submit_text').text('Отправка...');

        let isValid = true;
        const formData = $('form').serializeArray();
        const formDataObj = {};

        // Обработка чекбоксов skills
        $('.many-checkbox-button').each(function () {
            const $filed = $(this);
            const fieldName = $filed.find('.many-checkbox-button__input').attr('name')
            const $checkbox = $filed.find('input[type="checkbox"]');
            const val = $filed.val().trim();
            if (val === 'on') {
                return
            }
            if ($checkbox.prop('checked') && val) {
                formData.push({name: fieldName, value: val})
            }
        })

        let skills = []
        // Конвертируем formData в объект
        $.each(formData, function (i, field) {
            if (field.name === 'skills') {
                skills.push(field.value)
                return
            }
            formDataObj[field.name] = field.value;
        });

        formDataObj['skills'] = JSON.stringify(skills);

        // Обработка occupation (множественный выбор)
        const selectedOccupations = $('input[name="checkbox-occupation"]:checked');
        let occupationValues = [];
        selectedOccupations.each(function () {
            const val = $(this).val();
            if (val === 'another') {
                const otherText = $('#id_occupation').val().trim();
                if (otherText) {
                    occupationValues.push(otherText);
                }
            } else {
                // Берём текст из label
                const labelText = $(this).closest('.many-checkbox-button').find('.many-checkbox-button__label').text().trim();
                occupationValues.push(labelText);
            }
        });
        formDataObj['occupation'] = occupationValues.join(', ');

        // Проверка обязательных полей
        $('form input[required]').each(function () {
            const $field = $(this);
            const $fieldInputContainer = $field.closest('.field_inline_item_container');
            const $line = $field.closest('.input_container').find('.line');
            const $fieldWarningContainer = $fieldInputContainer.find('.field_item_warning_container');
            if ($field.attr('id') === 'id_occupation') {
                return true
            }
            // Обычная проверка для других полей
            if (!$field.val() && $field.prop('required')) {
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

        $('form textarea[required]').each(function () {
            const $field = $(this);
            const $fieldInputContainer = $field.closest('.field_inline_item_container');
            const $line = $field.closest('.input_container').find('.line');
            const $fieldWarningContainer = $fieldInputContainer.find('.field_item_warning_container');
            if ($field.attr('id') === 'id_occupation') {
                return true
            }
            // Обычная проверка для других полей
            if (!$field.val() && $field.prop('required')) {
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

        // Проверка occupation (хотя бы один чекбокс)
        if (!selectedOccupations.length) {
            const $occupationContainer = $('#field_inline_item_container_occupation');
            const $occupationWarning = $occupationContainer.find('.field_item_warning_container');
            $occupationContainer.addClass('invalid');
            $occupationWarning.css('display', 'block');
            isValid = false;
        } else if (selectedOccupations.length === 1 && selectedOccupations.first().val() === 'another' && !$('#id_occupation').val().trim()) {
            const $occupationContainer = $('#field_inline_item_container_occupation');
            const $occupationWarning = $occupationContainer.find('.field_item_warning_container');
            $occupationContainer.addClass('invalid');
            $occupationWarning.css('display', 'block');
            isValid = false;
        }

        // policy_agreement — необязательное
        const $idPolicyPolicy = $('#id_policy_agreement');
        formDataObj["policy_agreement"] = $idPolicyPolicy.prop('checked');

        if (!isValid) {
            resetButtonState($button);
            return false;
        }

        $.ajax({
            type: 'POST',
            url: $('form').attr('action'),
            data: formDataObj,
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
                        $fieldWarningContainer.html(errors.join('<br>')).css('display', 'block');
                    });

                    if (Object.keys(response.errors).length > 0) {
                        const firstErrorField = Object.keys(response.errors)[0];
                        const $firstErrorElement = $('[name=' + firstErrorField + ']');
                        $('html, body').animate({
                            scrollTop: $firstErrorElement.offset().top - 100
                        }, 500);
                    }
                    resetButtonState($button);
                }
            },
            error: function (xhr, status, error) {
                console.error('Ошибка при отправке формы:', status, error);
                resetButtonState($button);
            }
        });
    });

    // Сброс состояния кнопки
    function resetButtonState($button) {
        $button.css({'opacity': '1', 'pointer-events': 'auto'});
        $button.find('.submit_text').text('Отправить');
    }

    $('.clear_inline_container').click(function () {
        $('form')[0].reset();
        $('.input_container').removeClass('invalid');
        $('input[name="radio-group"]').prop('checked', false);
        $('input[name="checkbox-occupation"]').prop('checked', false);
        $('#id_occupation').prop('disabled', false).val('');
    });

    // Находим все textarea внутри .textarea-with-underline
    const $autoResizeTextareas = $('.auto-resize-textarea');

    // Функция для автоматического изменения высоты
    function autoResize($element) {
        // Сбрасываем высоту на auto для правильного расчета
        $element.css('height', 'auto');

        // Получаем вычисленные стили
        const computedStyle = window.getComputedStyle($element[0]);
        const maxHeight = parseInt(computedStyle.maxHeight) || 200;

        // Рассчитываем новую высоту
        const scrollHeight = $element[0].scrollHeight;
        const newHeight = Math.min(scrollHeight + 2, maxHeight);

        // Устанавливаем новую высоту
        $element.css('height', newHeight + 'px');

        // Показываем/скрываем полосу прокрутки при необходимости
        const showScrollbar = scrollHeight > $element[0].clientHeight;
        $element.css('overflow-y', showScrollbar ? 'auto' : 'hidden');
    }

    // Применяем функцию ко всем найденным textarea
    $autoResizeTextareas.each(function () {
        const $textarea = $(this);

        // Устанавливаем начальную высоту
        autoResize($textarea);

        // Добавляем обработчик на ввод текста
        $textarea.on('input', function () {
            autoResize($(this));
        });
    });

    // Также при изменении размера окна
    $(window).on('resize', function () {
        $autoResizeTextareas.each(function () {
            autoResize($(this));
        });
    });
});
