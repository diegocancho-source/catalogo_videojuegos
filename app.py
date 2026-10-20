from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datos import VideojuegoEntrada, VideojuegoRespuesta
 
# defino el título, la descripción y versión para la documentación automática.
app = FastAPI(
    title="API de Catálogo de Videojuegos",
    description="Servicio backend para gestionar y evaluar videojuegos usando FastAPI y Pydantic.",
    version="1.0.0"
)

# Configuro los permisos de CORS para permitir que cualquier 
# cliente frontend se comunique conmigo sin bloqueos de origen cruzado.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Preparo mi directorio para servir archivos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Defino mi ruta raiz: cuando me visiten en la URL principal, 
# yo me encargare de devolver directamente el archivo index.html.
@app.get("/", response_class=FileResponse)
def inicio():
    return FileResponse("index.html")

# Defino el endpoint POST para registrar y evaluar videojuegos, 
# asegurándome de que la respuesta cumpla con mi modelo VideojuegoRespuesta.
@app.post("/videojuegos", response_model=VideojuegoRespuesta)
def registrar_videojuego(juego: VideojuegoEntrada):
    """
    Recibe los datos de un videojuego, los valida mediante Pydantic
    y calcula el precio final aplicando reglas de negocio.
    """
    # Inicializo el descuento en cero y evalúo mi regla de negocio:
    # si el precio original supera los 60.0, decido aplicar un 15% de descuento.
    descuento = 0.0
    if juego.precio > 60.0:
        descuento = 0.15  
    
    # Calculo el precio final y lo redondeo a dos decimales.
    precio_final = round(juego.precio * (1 - descuento), 2)
    
    # Determino si el juego es apto para menores de 16 años.
    apto_menores = juego.calificacion_edad < 16
    
    # Construyo dinamicamente un resumen textual combinando el genero y la plataforma.
    resumen = f"Juego de {juego.genero or 'General'} para {juego.plataforma}. "
    if descuento > 0:
        resumen += "Incluye oferta promocional del 15%."
    else:
        resumen += "Precio estándar aplicado."

    # Empaqueto y devuelvo el resultado estructurado de mi modelo de respuesta.
    return {
        "titulo": juego.titulo,
        "plataforma": juego.plataforma,
        "precio_final": precio_final,
        "apto_menores": apto_menores,
        "resumen_catalogo": resumen
    }