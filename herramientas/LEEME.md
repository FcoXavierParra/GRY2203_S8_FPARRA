# Herramientas del proyecto

Tres scripts para validar y publicar. Todos se ejecutan desde la raíz del repositorio.

## Desde VS Code

`Ctrl+Shift+P` → **Tasks: Run Task** → elija:

| Tarea | Qué hace |
|---|---|
| **1 · Validar repositorio** | Estructura, `index.html` en la raíz, limpieza, tamaño y estado de Git |
| **2 · Verificar consistencia** | Que los tres artefactos describan el mismo sistema |
| **3 · Validar TODO** | Las dos anteriores en secuencia |
| **4 · Ver el prototipo** | Abre `index.html` en el navegador |
| **5 · Subir a GitHub** | Valida, pide confirmación y sube con historial por fases |

La tarea 1 es la predeterminada: `Ctrl+Shift+P` → **Tasks: Run Test Task**.

## Desde la terminal

```bash
python herramientas/validar_repositorio.py
python herramientas/verificar_consistencia.py
python herramientas/subir_a_github.py
```

## Qué detecta cada uno

**`validar_repositorio.py`** — pensado para evitar el error más común: que `index.html`
no quede en la raíz, con lo cual GitHub Pages responde 404. También avisa de archivos
temporales de Word (`~$`), versiones duplicadas en los nombres, páginas repetidas en los
`.drawio` y cambios sin confirmar en Git.

**`verificar_consistencia.py`** — comprueba que la arquitectura, el prototipo de baja
fidelidad y el de alta fidelidad describan el mismo sistema: las cuatro funcionalidades
presentes en los tres, los estados del dominio coincidentes, los datos de ejemplo iguales,
y sin navegación rota ni dependencias externas en el prototipo.

**`subir_a_github.py`** — valida antes de subir y se detiene si algo falla. Crea cinco
commits, uno por fase del proyecto, en lugar de un único commit con todo.

## Extensiones recomendadas

Al abrir la carpeta, VS Code sugiere instalar:

- **Draw.io Integration** — edita los `.drawio` sin salir del editor
- **Python** — ejecuta los scripts
- **Live Server** — sirve el prototipo con recarga automática
