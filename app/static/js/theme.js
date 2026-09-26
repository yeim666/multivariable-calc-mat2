// controla el boton de alternar tema. la aplicacion INICIAL del tema ya
// ocurrio en un script inline dentro de <head> (para evitar parpadeo);
// aqui solo manejamos el click para cambiarlo despues.

const themeToggle = document.getElementById("theme-toggle");


themeToggle.addEventListener("click", () => {

    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";

    document.documentElement.setAttribute("data-theme", next);

    // guardamos la preferencia para que persista entre visitas
    localStorage.setItem("theme", next);

});
