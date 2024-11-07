// login.js

document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById('login-form');

    // Form gönderme olayını dinle
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Varsayılan form gönderimini engelle

        // Form verilerini al
        const formData = new FormData(loginForm);
        const email = formData.get('email');
        const password = formData.get('password');

        // Giriş isteğini gönder
        fetch('/auth/login', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Giriş başarısız');
            }
            return response.json();
        })
        .then(data => {
            // Token'ı sessionStorage'a kaydet
            if (data.token) {
                sessionStorage.setItem('jwt_token', data.token);
                // Başarılı girişte yönlendirme
                window.location.href = '/upload_file'; // İstediğin sayfaya yönlendir
            } else {
                alert(data.message || 'Giriş başarısız!');
            }
        })
        .catch(error => {
            alert(error.message);
        });
    });
});
