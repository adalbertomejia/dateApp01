# Plan de refactor priorizado (MVP limpio y escalable)

## 1) reservations (máxima prioridad)

### Objetivo
Consolidar reglas de negocio de citas, evitar duplicados de forma segura y reducir lógica repetida en vistas.

### Checklist priorizado
- [x] Centralizar validaciones de cita en el modelo (`clean`) para reutilización desde formularios, vistas o API.
- [x] Endurecer validación de teléfono (10 dígitos numéricos) con errores por campo.
- [x] Evitar falsos duplicados al editar una cita existente (`exclude(pk=self.pk)`).
- [x] Reutilizar contexto de disponibilidad semanal para no duplicar lógica en vistas.
- [x] Agregar ordenamiento por defecto del modelo para consultas consistentes (`Meta.ordering`).
- [x] Agregar restricción de unicidad a nivel base de datos para `date + time`.
- [x] Ajustar manejo de errores en `book_appointment` para mostrar mensajes reales de validación.
- [x] Cubrir reglas críticas con pruebas unitarias del modelo.

### Próximos pasos sugeridos
- [ ] Mover lógica de orquestación de reserva a un servicio dedicado (`reservations/services.py`).
- [ ] Introducir `ModelForm` para validación/limpieza de entrada HTTP y mensajes de error más finos.
- [ ] Agregar endpoint paginado de disponibilidad si se amplía ventana de días.

---

## 2) users (prioridad media)

### Objetivo
Mantener la app enfocada en autenticación/roles y minimizar lógica acoplada a métricas.

### Checklist priorizado
- [x] Limpieza de imports y estructura básica del modelo de usuario.
- [x] Reducir redundancia en consultas que ya heredan orden por defecto del modelo `Appointment`.
- [x] Extraer capacidad diaria a constante para evitar “números mágicos” en métricas.

### Próximos pasos sugeridos
- [ ] Crear permisos/grupos formales para staff nutricionista (más allá de flags booleanos).
- [ ] Separar cálculo de KPIs del dashboard en funciones utilitarias o servicio.

---

## 3) proyecto global (prioridad media-baja)

### Objetivo
Dejar una base preparada para crecer sin sacrificar simplicidad.

### Checklist priorizado
- [x] Documentar el plan técnico y estado de avance por app (este archivo).
- [ ] Configurar entorno local estándar (`requirements.txt`/`pip-tools`) para ejecutar tests en cualquier máquina.
- [ ] Estandarizar idioma y zona horaria del proyecto según negocio (por ejemplo `es-mx` + TZ local).
- [ ] Añadir pipeline CI mínimo (lint + tests) para proteger regresiones.
- [ ] Definir convención de capas: `models` (reglas), `services` (orquestación), `views` (HTTP).

## Resultado esperado tras estas mejoras
- Menos duplicidad de código.
- Reglas críticas protegidas en dos capas (aplicación + base de datos).
- Mayor legibilidad para iterar rápido en fase MVP.
- Menor riesgo de inconsistencias al escalar funcionalidades.
