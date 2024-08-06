
    document.addEventListener("DOMContentLoaded", function() {
        // Получаем все чекбоксы на странице
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');

        checkboxes.forEach(checkbox => {
            // Добавляем обработчик события 'change' для каждого чекбокса
            checkbox.addEventListener('change', function() {
                // Получаем имя текущего чекбокса
                const inputName = this.getAttribute('value');
                // Находим соответствующий скрытый input по имени
                const hiddenInput = document.querySelector(`input[name=${inputName}]`);

                // Обновляем значение скрытого input в зависимости от состояния чекбокса
                hiddenInput.value = this.checked ? '1' : '0';
            });
        });
    });

