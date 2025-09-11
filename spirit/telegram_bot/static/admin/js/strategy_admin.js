document.addEventListener('DOMContentLoaded', function() {
    const strategyTypeSelect = document.querySelector('#id_strategy_type');

    if (strategyTypeSelect) {
        // Обновляем поля при изменении типа стратегии
        strategyTypeSelect.addEventListener('change', updateStrategyFields);

        function updateStrategyFields() {
            const selectedType = strategyTypeSelect.value;
            const paramFields = document.querySelector('.strategy-params');

            // Скрываем все параметры
            paramFields.querySelectorAll('div').forEach(field => {
                field.style.display = 'none';
            });

            // Показываем нужные поля
            if (selectedType === 'keyword') {
                document.querySelector('#keyword_fields').style.display = 'block';
            } else if (selectedType === 'regex') {
                document.querySelector('#regex_fields').style.display = 'block';
            }
        }

        // Инициализация при загрузке
        updateStrategyFields();
    }
});
