// Función para la cuenta regresiva
function countdownTimer() {
    const now = new Date();
    const utcNow = new Date(
        now.getUTCFullYear(),
        now.getUTCMonth(),
        now.getUTCDate(),
        now.getUTCHours(),
        now.getUTCMinutes(),
        now.getUTCSeconds(),
        now.getUTCMilliseconds()
    );

    // Establecer la fecha objetivo (28 años a partir del día actual)
    const targetDate = new Date(utcNow);
    targetDate.setUTCFullYear(targetDate.getUTCFullYear() + 28); // 28 años de cuenta regresiva
    targetDate.setUTCHours(0, 0, 0, 0); // Al inicio del día (00:00:00)

    const difference = targetDate - utcNow;

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

    // Mostrar los resultados de la cuenta regresiva en la página
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
