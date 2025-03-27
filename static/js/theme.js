// Функция для применения темы
function applyTheme(isDark) {
    document.body.classList.toggle('dark-theme', isDark);
    localStorage.setItem('darkTheme', isDark);

    // Обновляем все переключатели на странице
    document.querySelectorAll('.theme-checkbox').forEach(checkbox => {
        checkbox.checked = isDark;
    });
}

// Инициализация темы при загрузке
document.addEventListener('DOMContentLoaded', function () {
    const savedTheme = localStorage.getItem('darkTheme') === 'true';
    applyTheme(savedTheme);

    // Обработчик изменения переключателя
    document.querySelectorAll('.theme-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            applyTheme(this.checked);
        });
    });
});

// Для отладки - проверяем в консоли
console.log('Система темы инициализирована');
console.log('Текущая тема:', localStorage.getItem('darkTheme'));
