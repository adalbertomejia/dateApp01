document.addEventListener('DOMContentLoaded', () => {
    fetch('/get-unavailable-slots/')
        .then(response => response.json())
        .then(data => {
            const unavailableSlots = data;

            // Deshabilitar fechas ocupadas
            const dateInput = document.querySelector('input[type="date"]');
            dateInput.addEventListener('change', (e) => {
                const selectedDate = e.target.value;
                const timeInput = document.querySelector('input[type="time"]');
                timeInput.disabled = false;

                // Deshabilitar horas ocupadas para la fecha seleccionada
                unavailableSlots.forEach(slot => {
                    if (slot.date === selectedDate) {
                        const option = document.querySelector(`option[value="${slot.time}"]`);
                        if (option) {
                            option.disabled = true;
                        }
                    }
                });
            });
        });
});