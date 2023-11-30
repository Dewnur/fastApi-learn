const register_form = document.getElementById('register-form');

register_form.addEventListener('submit', function (event) {
    // Останавливаем стандартное поведение формы (перезагрузка страницы)
    event.preventDefault();
    const url = "http://127.0.0.1:8000/api/v1/auth/register";
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            email: email,
            password: password,
            username: username
        }),
    })
        .then(response => {
            if (response.status === 201) {
                window.location.href = "/pages/login"
            }
            return response.json()
        })
        .then(data => {
            const register_alert = document.getElementById("register-alert")
            const register_alert_text = document.getElementById("register-alert-text")
            register_alert.style.display = "block";
            register_alert_text.textContent = data.detail
        })
        .catch(error => console.error('Error:', error));
});

