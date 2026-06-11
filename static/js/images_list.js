document.querySelectorAll('.images-list__button--delete').forEach((button) => {
    button.addEventListener('click', async () => {
        const filename = button.dataset.filename;

        if (!filename) {
            return;
        }

        const confirmed = confirm(`Удалить изображение ${filename}?`);
        if (!confirmed) {
            return;
        }

        button.disabled = true;

        try {
            const response = await fetch(
                `/images-list/${encodeURIComponent(filename)}`,
                { method: 'DELETE' }
            );

            if (!response.ok) {
                throw new Error('Delete failed');
            }

            const row = button.closest('.images-list__row');
            if (row) {
                row.remove();
            }

            const summary = document.querySelector('.images-list__summary p');
            if (summary) {
                const match = summary.textContent.match(/\d+/);
                if (match) {
                    const total = Math.max(Number(match[0]) - 1, 0);
                    summary.textContent = `Всего записей: ${total}`;
                }
            }

            if (!document.querySelector('.images-list__row')) {
                window.location.reload();
            }
        } catch (error) {
            button.disabled = false;
            alert('Не удалось удалить изображение');
        }
    });
});
