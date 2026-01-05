const notifice = document.getElementById("message");

if (notifice) {
  setTimeout(() => {
    notifice.style.display = "none";
  }, 6000);
  notifice.addEventListener("click", () => {
    notifice.style.display = "none";
  });
}

// Selecciona todos los alert de sesión
const sessionAlerts = document.querySelectorAll(".alert");

sessionAlerts.forEach((alert) => {
  // Desaparece después de 7 segundos
  setTimeout(() => {
    // Aplicamos animación de Animate.css para fade out hacia arriba
    alert.classList.remove("animate__fadeInDown"); // quitamos la animación de entrada
    alert.classList.add("animate__fadeOutUp"); // agregamos animación de salida

    // Esperamos 1 segundo para que termine la animación antes de remover el alert del DOM
    setTimeout(() => alert.remove(), 1000);
  }, 7000);

  // También permitir cerrar al hacer click en el botón
  alert.addEventListener("click", () => alert.remove());
});

/**********************************************************/

const btn_delete = document.querySelectorAll("#delete");

if (btn_delete) {
  const btnArray = Array.from(btn_delete);
  btnArray.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      if (!confirm("Are you sure, you want to delete it ??"))
        e.preventDefault();
    });
  });
}

console.log("Contact App Loaded Successfully!");
