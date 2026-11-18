# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto desarrollado para la Fase 4 - Componente Práctico (Programación 213023 - UNAD).

## Integrantes Activos
 Cristóbal Acevedo Correa
 Luis Fernando Benedetti Ospina

## Arquitectura Modular del Proyecto
 `excepciones.py` Jerarquía de excepciones personalizadas del sistema.
 `clientes.py` Clase abstracta `EntidadBase` y clase `Cliente` con encapsulación y validaciones estrictas.
 `servicios.py` Clase abstracta `Servicio` y subclases (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) aplicando polimorfismo y sobrecarga.
 `reservas.py` Gestión de estados, confirmación (`tryexceptelsefinally`), encadenamiento de errores y cancelación.
 `main.py` Punto de entrada con configuración de `logging` y ejecución de 10 simulaciones válidas e inválidas.

## Ejecución
Ejecutar el archivo principal desde terminal
```bash
python main.py