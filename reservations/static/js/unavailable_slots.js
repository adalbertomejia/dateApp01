document.addEventListener('DOMContentLoaded', () => {
    fetch('/get-unavailable-slots/')
        .then(response => response.json())
        .then(data => {
            const unavailableSlots = data;
            const dateInput = document.getElementById('date');
            const timeSelect = document.getElementById('time');

            if (!dateInput || !timeSelect) {
                return;
            }

            dateInput.addEventListener('change', (e) => {
                const selectedDate = e.target.value;

                Array.from(timeSelect.options).forEach(option => {
                    option.disabled = false;
                });

                unavailableSlots.forEach(slot => {
                    if (slot.date === selectedDate) {
                        const slotHour = slot.time.slice(0, 5);
                        const option = timeSelect.querySelector(`option[value="${slotHour}"]`);
                        if (option) {
                            option.disabled = true;
                        }
                    }
                });
            });
        });
});
