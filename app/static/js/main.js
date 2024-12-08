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

    // Controlador para las notificaciones flash en modal
    const modal = document.getElementById('flash-modal');
    const closeButton = document.querySelector('.modal .delete');
    const okButton = document.querySelector('.modal .button.is-success');

    if (modal && modal.querySelector('.notification')) {
        modal.classList.add('is-active');
    }

    const closeModal = () => {
        modal.classList.remove('is-active');
    }

    closeButton.addEventListener('click', closeModal);
    okButton.addEventListener('click', closeModal);

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

    // Gráfica de histórico de correos
    if (document.getElementById('emailHistoryChart')) {
        const jsonData = JSON.parse(document.getElementById('emailHistoryChart').dataset.json);

        var ctx = document.getElementById('emailHistoryChart').getContext('2d');
        var emailHistoryChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: jsonData.labels,
                datasets: [{
                    label: 'Envíos de Correos',
                    data: jsonData.data,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day'
                        }
                    },
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Sendmode en scheduler
    const sendModeField = document.querySelector('select[name="send_mode"]');
    const individualFields = document.querySelectorAll('.individual');
    const listFields = document.querySelectorAll('.list');

    function updateForm() {
        const sendMode = sendModeField.value;
        if (sendMode === 'individual') {
            individualFields.forEach(field => field.style.display = 'block');
            listFields.forEach(field => field.style.display = 'none');
        } else if (sendMode === 'list') {
            individualFields.forEach(field => field.style.display = 'none');
            listFields.forEach(field => field.style.display = 'block');
        } else if (sendMode === 'all') {
            individualFields.forEach(field => field.style.display = 'none');
            listFields.forEach(field => field.style.display = 'none');
        }
    }

    sendModeField.addEventListener('change', updateForm);
    updateForm();  // Initialize the form
});




