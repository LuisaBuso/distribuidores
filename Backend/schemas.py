from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional
from pydantic.networks import EmailStr
# from pydantic.types import SecretStr

class Admin(BaseModel):
    nombre: str
    pais: str
    whatsapp: str
    correo_electronico: EmailStr
    password: str
    rol: str  # Puede ser "Distribuidor" o "AdminN"
        
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    rol: str
    nombre: str
    pais: str
    email: str

# Esquema para crear un distribuidor (sin admin_id)    
class DistribuidorCreate(BaseModel):
    nombre: str
    pais: str
    phone: str
    correo_electronico: EmailStr
    password: str

class Distribuidor(BaseModel):
    nombre: str
    pais: str
    phone: str
    correo_electronico: EmailStr
    admin_id: str
    
# CLASE PARA CREAR PRODUCTOS
class ProductCreate(BaseModel):
    nombre: str
    categoria: str
    precio_sin_iva_colombia: float
    precio_con_iva_colombia: float
    precio_internacional: float
    stock: int
    margen_descuento: float = 0.45
    codigo_tipo: Optional[int] = None

    class Config:
        json_encoders = {
            float: lambda v: round(v, 2),
        }

# CLASE PARA ACTUALIZAR PRODUCTOS
class ProductUpdate(BaseModel):
    nombre: str = None
    categoria: str = None
    precio: float = None
    stock: int = None
    
class ProductoPedido(BaseModel):
    id: str = Field(..., description="ID del producto")
    cantidad: int = Field(..., gt=0, description="Cantidad del producto")

class PedidoCreate(BaseModel):
    productos: List[ProductoPedido] = Field(..., min_items=1, description="Lista de productos")
    direccion: str = Field(..., min_length=5, description="Dirección de entrega")
    notas: str = Field("", description="Notas adicionales")

class PedidoResponse(BaseModel):
    id: str
    distribuidor_id: str
    distribuidor_nombre: str
    distribuidor_phone: str
    productos: List[dict]
    direccion: str
    notas: str
    fecha: datetime
    estado: str

# MODELO PARA CREAR USUARIOS CON DIFERENTES ROLES
class UserCreate(BaseModel):
    nombre: str
    pais: str
    correo_electronico: str
    phone: str
    password: str
    rol: str  # "produccion", "facturacion" o "distribuidor"
    tipo_precio: Optional[str] = Field(
        None,
        description="Tipo de precio para distribuidores. Opciones: 'sin_iva', 'con_iva', 'sin_iva_internacional'"
    )
    
# MODELO DE RESPUESTA PARA USUARIOS
class UserResponse(BaseModel):
    id: str
    nombre: str
    correo_electronico: str
    rol: str
    phone: str
    estado: str
    fecha_ultimo_acceso: str
    admin_id: str | None = None  # Puede ser opcional
    tipo_precio: str | None = None  # Puede ser opcional

# modelo para actualizar usuarios
class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    correo_electronico: Optional[str] = None
    rol: Optional[str] = None
    phone: Optional[str] = None
    estado: Optional[str] = None
    tipo_precio: Optional[str] = None
    contrasena: Optional[str] = None

# MODELO PARA RESPUESTA DE DASHBOARD
class EstadisticasGeneralesResponse(BaseModel):
    pedidos_totales: int
    total_productos: int
    total_distribuidores: int
    ventas_mensuales: float 

