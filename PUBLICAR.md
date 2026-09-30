# Publicar este repositorio en GitHub

Repositorio: `https://github.com/FcoXavierParra/GRY2203_S8_FPARRA`
Prototipo publicado: `https://fcoxavierparra.github.io/GRY2203_S8_FPARRA/`

El repositorio ya tiene una versión anterior. Estas instrucciones la reemplazan por completo.

---

## Opción A — Desde el navegador, sin instalar nada

**Recomendada si no tienes Git configurado.**

### 1. Borrar el contenido actual

1. Entra al repositorio → pestaña **Code**.
2. Por cada archivo o carpeta que aparezca: haz clic en él → botón **⋯** (arriba a la derecha) → **Delete file** o **Delete directory** → **Commit changes**.
3. Repite hasta que el repositorio quede vacío.

> Si aparece un aviso de que no puedes borrar el último archivo, deja el `README.md` y sobrescríbelo en el paso siguiente.

### 2. Subir la versión nueva

1. **Add file → Upload files**.
2. Abre la carpeta `repo_v2` en el explorador de Windows.
3. Selecciona **todo su contenido** (Ctrl+A) y arrástralo a la ventana del navegador.
   GitHub conserva las subcarpetas automáticamente.
4. En *Commit changes* escribe: `Estructura final del proyecto SGGC`.
5. **Commit changes**.

### 3. Confirmar que quedó bien

El repositorio debe mostrar exactamente esto:

```
arquitectura/        documentacion/       herramientas/
prototipos/          index.html           README.md
.gitignore           PUBLICAR.md
```

---

## Opción B — Desde la terminal, con historial por fases

**Recomendada si quieres que el repositorio refleje la evolución del proyecto.**
Esto es pertinente en esta unidad, que trata precisamente de control de versiones.

```bash
cd "C:\Users\fparraa\Documents\ESTUDIO\GRY2203 ING SOFTWARE 2\S8_Sumativa_3\repo_v2"

git init
git branch -M main

git add arquitectura/
git commit -m "Modelado arquitectonico bajo el marco 4+1"

git add prototipos/baja-fidelidad/
git commit -m "Ideacion y prototipo de baja fidelidad"

git add prototipos/alta-fidelidad/ index.html
git commit -m "Prototipo interactivo de alta fidelidad"

git add documentacion/
git commit -m "Documentacion de cierre: DAS, lecciones aprendidas y acta"

git add herramientas/ README.md .gitignore PUBLICAR.md
git commit -m "Herramienta de verificacion y documentacion del repositorio"

git remote add origin https://github.com/FcoXavierParra/GRY2203_S8_FPARRA.git
git push -u origin main --force
```

El `--force` sobrescribe lo que haya en GitHub. Es lo que buscamos aquí.

Si pide credenciales: usuario es tu nombre de GitHub, y la contraseña es un
**token personal** (Settings → Developer settings → Personal access tokens →
Tokens (classic) → Generate new token, con permiso `repo`).

---

## Verificar GitHub Pages

1. **Settings → Pages**
2. Source: *Deploy from a branch* · Branch: **main** · carpeta **/ (root)** · **Save**
3. Espera uno o dos minutos y abre la URL.

Como `index.html` está en la raíz, la publicación no se rompe al reemplazar el contenido.

Si sale 404: recarga con `Ctrl+F5`, y si persiste revisa la pestaña **Actions**
del repositorio para ver si el despliegue falló.

---

## Antes de dar por cerrado

```bash
python herramientas/verificar_consistencia.py
```

Debe terminar con *«Todas las verificaciones pasaron»*.
