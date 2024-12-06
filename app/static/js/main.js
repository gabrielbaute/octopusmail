document.addEventListener('DOMContentLoaded', () => {
    // Cerrar notificaciones flash
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        var $notification = $delete.parentNode;

        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
        });
    });

    // Controlar visibilidad de los campos en el formulario de envío de correos
    const sendModeSelect = document.getElementById('send_mode');
    if (sendModeSelect) {
        const individualFields = document.querySelectorAll('.individual-field');
        const listField = document.querySelector('.list-field');

        sendModeSelect.addEventListener('change', function() {
            const mode = sendModeSelect.value;
            individualFields.forEach(field => {
                field.style.display = mode === 'individual' ? 'block' : 'none';
            });
            listField.style.display = mode === 'list' ? 'block' : 'none';
        });

        // Initialize visibility based on current selection
        sendModeSelect.dispatchEvent(new Event('change'));
    }

    // Manejar el cambio de tema
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;
    const currentTheme = localStorage.getItem('theme') || 'light';

    if (currentTheme === 'dark') {
        htmlElement.setAttribute('data-theme', 'dark');
    }

    themeToggle.addEventListener('click', () => {
        const theme = localStorage.getItem('theme');
        if (theme === 'light') {
            htmlElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            htmlElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });
});
