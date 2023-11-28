async function logoutUser() {
    const url = "http://127.0.0.1:8000/api/v1/auth/logout";

    await fetch(url, {
        method: 'POST',
    }).then(response => {
        if (response.status === 200) {
            window.location.href = "/pages/"
        }
    });
}