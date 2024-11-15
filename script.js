// Inicializa la fecha de la entrada del usuario
const startDate = new Date(); // Tomamos la fecha y hora actuales cuando el usuario entra a la página

// Configura la fecha de destino (28 años después de la fecha de inicio)
const targetDate = new Date(startDate);
targetDate.setFullYear(startDate.getFullYear() + 28); // Agregar 28 años a la fecha de inicio

// Función para actualizar la cuenta regresiva
function countdownTimer() {
    const now = new Date();
    const difference = targetDate - now;

    if (difference <= 0) {
        document.getElementById("countdown").innerHTML = "<h2>El Apocalipsis ha comenzado...</h2>";
        return;
    }

    // Calcular los años, días, horas, minutos, segundos y milisegundos restantes
    const years = Math.floor(difference / (1000 * 60 * 60 * 24 * 365));
    const days = Math.floor((difference % (1000 * 60 * 60 * 24 * 365)) / (1000 * 60 * 60 * 24));
    const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((difference % (1000 * 60)) / 1000);
    const milliseconds = Math.floor((difference % 1000) / 10);

    // Actualizar el contenido de la cuenta regresiva
    document.getElementById("years").textContent = String(years).padStart(2, "0");
    document.getElementById("days").textContent = String(days).padStart(3, "0");
    document.getElementById("hours").textContent = String(hours).padStart(2, "0");
    document.getElementById("minutes").textContent = String(minutes).padStart(2, "0");
    document.getElementById("seconds").textContent = String(seconds).padStart(2, "0");
    document.getElementById("milliseconds").textContent = String(milliseconds).padStart(3, "0");
}

// Actualiza la cuenta regresiva cada 10 milisegundos
setInterval(countdownTimer, 10);

// Reproducir y pausar música de fondo
const music = document.getElementById("backgroundMusic");
const toggleButton = document.getElementById("toggleMusic");

toggleButton.addEventListener("click", () => {
    if (music.paused) {
        music.play();
        toggleButton.textContent = "⏸ Pausar Música";
    } else {
        music.pause();
        toggleButton.textContent = "▶ Reanudar Música";
    }
});

// Funciones para compartir en redes sociales
function shareOnFacebook() {
    const url = encodeURIComponent(window.location.href);
    const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
    window.open(shareUrl, '_blank');
}

function shareOnTwitter() {
    const url = encodeURIComponent(window.location.href);
    const text = encodeURIComponent("¡Mira la cuenta regresiva hacia el fin del mundo!");
    const shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${text}`;
    window.open(shareUrl, '_blank');
}

function shareOnWhatsApp() {
    const url = encodeURIComponent(window.location.href);
    const text = encodeURIComponent("¡Mira la cuenta regresiva hacia el fin del mundo!");
    const shareUrl = `https://wa.me/?text=${text}%20${url}`;
    window.open(shareUrl, '_blank');
}
