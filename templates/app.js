// Atrapamos el formulario cuando el usuario le da a "Ingresar"
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Evita que la página parpadee o se recargue

    // Obtenemos lo que el usuario escribió
    const usuario = document.getElementById('usuario').value;
    const password = document.getElementById('password').value;
    const mensaje = document.getElementById('mensaje');

    // Validación de prueba
    if(usuario === "admin" && password === "1234") {
        window.location.href = "exito.html";
        // Aquí luego pondremos el código para redirigir a la página del modelo predictivo
    } else {
        mensaje.style.color = "red";
        mensaje.textContent = "Usuario o contraseña incorrectos.";
    }
});