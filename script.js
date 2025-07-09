document.addEventListener('DOMContentLoaded', () => {
    const explorarBtn = document.getElementById('explorarBtn');
    if (explorarBtn) {
        explorarBtn.addEventListener('click', () => {
            alert('¡Has hecho clic en Explorar Datos! Aquí iría la lógica para cargar información.');
        });
    }
    console.log('UrbanBeat script.js cargado correctamente.');
});