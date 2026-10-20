const formulario = document.getElementById("formulario-juego");
const panelResultado = document.getElementById("panel-resultado");
const resultadoCaja = document.getElementById("resultado-caja");
const btnEnviar = document.getElementById("btn-enviar");

formulario.addEventListener("submit", async (evento) => {
  // 1. Evitamos el comportamiento por defecto de recarga del formulario
  evento.preventDefault();

  // 2. Extraemos los valores y los convertimos al formato que espera Pydantic
  const datosVideojuego = {
    titulo: document.getElementById("titulo").value,
    plataforma: document.getElementById("plataforma").value,
    precio: parseFloat(document.getElementById("precio").value),
    calificacion_edad: parseInt(document.getElementById("edad").value),
    multijugador: document.getElementById("multijugador").checked,
    genero: document.getElementById("genero").value || null
  };

  btnEnviar.disabled = true;
  btnEnviar.textContent = "⏳ Enviando datos a la API...";

  try {
    // 3. Petición POST asíncrona hacia nuestro endpoint de FastAPI
    const respuesta = await fetch("/videojuegos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(datosVideojuego)
    });

    if (!respuesta.ok) {
      const errorData = await respuesta.json();
      throw new Error(JSON.stringify(errorData.detail, null, 2));
    }

    // 4. Parseamos la respuesta JSON del servidor
    const resultado = await respuesta.json();

    // 5. Mostramos el panel de resultados dinámicamente
    panelResultado.classList.remove("hidden");
    
    resultadoCaja.className = "p-6 rounded-xl border border-indigo-500/30 bg-indigo-950/40 text-slate-100";
    resultadoCaja.innerHTML = `
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-bold text-indigo-400">✨ Videojuego Registrado con Éxito</h3>
        <span class="px-3 py-1 bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded-full font-bold text-sm">
          ${resultado.plataforma}
        </span>
      </div>
      <p class="text-sm mb-2"><strong>Título:</strong> ${resultado.titulo}</p>
      <p class="text-sm mb-2"><strong>Precio Final Aplicado:</strong> <span class="text-emerald-400 font-bold text-lg">${resultado.precio_final} €</span></p>
      <p class="text-sm mb-2"><strong>¿Apto para menores de 16?:</strong> ${resultado.apto_menores ? "Sí (Apto)" : "No (Restringido)"}</p>
      <p class="text-sm text-indigo-200 mt-4 p-3 bg-indigo-900/30 rounded-lg border border-indigo-800/50 italic">${resultado.resumen_catalogo}</p>
    `;

  } catch (error) {
    alert("Error de validación en la API:\n" + error.message);
    console.error(error);
  } finally {
    btnEnviar.disabled = false;
    btnEnviar.textContent = "🚀 Registrar y Evaluar con la API";
  }
});