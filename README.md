# Sistema de Gestión de Pagos de Gastos Comunes (SGGC)

Diseño y documentación de arquitectura para el edificio residencial **“Nuevos Horizontes”**.

**Asignatura:** GRY2203 Ingeniería de Software II · Duoc UC
**Carrera:** Analista Programador
**Equipo:** Marcelo Bernabé Díaz Canales · Francisco Javier Parra Andía
**Profesor:** José Luis Martínez Opazo

---

## Prototipo en línea

👉 **[Abrir el prototipo interactivo](https://fcoxavierparra.github.io/GRY2203_S8_FPARRA/)**

| Prueba | Cómo |
|---|---|
| Manejo de errores | Borre la contraseña y pulse **Ingresar** |
| Flujo de pago | Estado de cuenta → **Pagar ahora** → medio de pago → **Confirmar** |
| Alerta accionable | Pestaña **Alertas** → toque la alerta de cuota vencida |
| Envío de avisos | Escritorio → **Recordatorios** → seleccione unidades → **Enviar ahora** |
| Vista ampliada | Botón **⛶ Pantalla completa** |

---

## El problema

El edificio administra 160 departamentos —100 de propietarios y 60 en arriendo— con procesos manuales, lo que produce morosidad no detectada a tiempo, errores en el cálculo del prorrateo, lentitud en la cobranza y desconfianza por falta de transparencia.

## La solución

Aplicación web responsiva con dos perfiles:

- **Residente (móvil):** consulta su saldo, entiende el desglose de su cuota, paga en línea y recibe alertas antes del vencimiento.
- **Administrador (escritorio):** registra residentes y gastos, calcula el prorrateo, controla la morosidad y envía recordatorios.

---

## Estructura del repositorio

```
.
├── index.html                          Prototipo publicado en GitHub Pages
│
├── arquitectura/
│   └── modelo-4mas1.drawio             CÓMO ESTÁ CONSTRUIDO EL SISTEMA
│                                       11 páginas · las 5 vistas del modelo 4+1
├── prototipos/
│   ├── baja-fidelidad/
│   │   └── ideacion-y-wireframes.drawio   QUÉ VE EL USUARIO Y POR QUÉ
│   │                                      9 páginas · 4 de ideación + 5 de pantallas
│   └── alta-fidelidad/
│       └── prototipo-interactivo.html     CÓMO SE SIENTE USARLO
│                                          15 vistas navegables · 196 controles
├── documentacion/
│   ├── DAS-documento-arquitectura-software.docx
│   ├── lecciones-aprendidas.docx
│   └── acta-cierre-proyecto.docx
│
└── herramientas/
    └── verificar_consistencia.py       Comprueba que los 3 artefactos coincidan
```

Los archivos `.drawio` se abren en [app.diagrams.net](https://app.diagrams.net) sin instalar nada.

### Qué contiene cada artefacto

Los dos archivos `.drawio` responden preguntas distintas y **no se solapan**:

| | `arquitectura/` | `prototipos/baja-fidelidad/` |
|---|---|---|
| Responde | ¿Cómo está construido el sistema? | ¿Qué ve el usuario y por qué? |
| Contiene | Contexto, casos de uso, clases, actividad, estados, componentes, paquetes, despliegue | Personas, mapa de empatía, brainwriting, mapa de ofertas, storyboard, wireframes |
| Audiencia | Equipo técnico | Usuarios y contraparte del negocio |
| Fase | Semanas 3 a 5 | Semana 6 |

---

## Arquitectura

Monolito modular en capas, documentado bajo el modelo **4+1** de Kruchten (1995):

| Vista | Páginas | Contenido |
|---|---|---|
| Contexto | 0 | Frontera del sistema y entidades externas |
| Escenarios (+1) | 1 – 4 | Casos de uso nivel 1 y nivel 2 |
| Lógica | 5 | Diagrama de clases con cardinalidades y restricciones |
| Procesos | 6 – 7 | Actividad del ciclo mensual y máquina de estados de Cuota |
| Desarrollo | 8 – 9 | Componentes y paquetes |
| Física | 10 | Despliegue con nodos y protocolos |

**Stack propuesto:** Java 17 · Spring Boot 3 · PostgreSQL 15 · Thymeleaf · Bootstrap 5

---

## Accesibilidad

Verificada contra [WCAG 2.1](https://www.w3.org/TR/WCAG21/):

| Elemento | Contraste | Nivel |
|---|---|---|
| Texto principal | 15,78:1 | AAA |
| Texto secundario | 6,00:1 | AA |
| Botón primario | 8,50:1 | AAA |
| Estados de error | 6,54:1 | AA |

Además: foco visible de 3 px, áreas táctiles de 44 × 44 px, estados comunicados con texto e ícono además de color, y etiquetas asociadas en todos los campos.

---

## Verificar la consistencia

```bash
python herramientas/verificar_consistencia.py
```

Comprueba que los tres artefactos describan el mismo sistema: que las cuatro funcionalidades clave estén en los tres, que los estados del dominio coincidan, que los datos de ejemplo sean los mismos y que no haya navegación rota ni dependencias externas.

---

## Alcance

Este proyecto llega hasta el **diseño validado mediante prototipo interactivo**. No incluye código de producción, base de datos poblada ni integración efectiva con pasarelas de pago.

---

*Proyecto académico. Los datos mostrados son ficticios.*
