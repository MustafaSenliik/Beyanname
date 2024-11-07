document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            fetch('/auth/login', { method: 'POST', body: new FormData(loginForm) })
                .then(response => {
                    if (response.ok) {
                        sessionStorage.setItem('isLoggedIn', 'true');
                        window.location.href = '/file/upload';
                    } else {
                        alert('Giriş bilgileri hatalı!');
                    }
                })
                .catch(error => console.error('Login error:', error));
        });
    }

    // Sekme kapatıldığında logout isteği gönder
    window.addEventListener('unload', function() {
        sessionStorage.removeItem('isLoggedIn');
        navigator.sendBeacon('/auth/logout'); // Sekme kapanınca sunucuya logout isteği gönder
    });

    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            sessionStorage.removeItem('isLoggedIn');
            window.location.href = '/auth/login';
        });
    }
});

function clearSessionData() {
    sessionStorage.removeItem('isLoggedIn');
}


function checkSessionValidity() {
    fetch('/check_session')
        .then(response => {
            if (!response.ok) {
                throw new Error('Sunucuya bağlanırken bir hata oluştu');
            }
            return response.json();
        })
        .then(data => {
            if (!data.isValid) {
                window.location.href = '/auth/login';
            }
        })
        .catch(error => {
            console.error('Oturum geçerliliği kontrolünde hata:', error);
        });
}
