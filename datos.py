from pydantic import BaseModel, Field

# Datos 
class VideojuegoEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=100, description="Título del videojuego")
    plataforma: str = Field(min_length=2, max_length=50, description="Plataforma pricipal")
    precio : float = Field(gt=0.0, le=150.0, description="Precio base en euros")    
    calificacion_edad: int = Field(ge=3, le= 18, description="Edad minima recomendada")
    multijugador: bool = Field(default=False, description="¿Dispone de multijugador?")
    genero: str | None = Field(default="Aventura", description="Genero del videojuego")

class VideojuegoRespuesta(BaseModel):
    titulo: str
    plataforma: str
    precio_final: float
    apto_menores: bool
    resumen_catalogo: str
    