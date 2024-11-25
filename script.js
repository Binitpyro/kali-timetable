
const backendBaseUrl = "https://timetable-backend.onrender.com";

document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('file');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch(`${backendBaseUrl}/upload`, {
        method: 'POST',
        body: formData,
    });

    const result = await response.json();
    document.getElementById('upload-result').textContent = result.message || result.error;
});

document.getElementById('free-now').addEventListener('click', async () => {
    const response = await fetch(`${backendBaseUrl}/free-now`);
    const result = await response.json();
    document.getElementById('availability-result').textContent = JSON.stringify(result);
});

document.getElementById('free-next').addEventListener('click', async () => {
    const response = await fetch(`${backendBaseUrl}/free-next`);
    const result = await response.json();
    document.getElementById('availability-result').textContent = JSON.stringify(result);
});
