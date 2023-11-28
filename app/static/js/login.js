async function loginUser() {

    const url = "http://127.0.0.1:8000/api/v1/auth/login";
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email: email, password: password}),
    }).then(response => {
        if (response.status === 200) {
            window.location.href = "/pages/"
        }
    });
}