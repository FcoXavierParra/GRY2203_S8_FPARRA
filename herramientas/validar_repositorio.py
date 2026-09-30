#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Valida que el repositorio este listo para subir a GitHub.

Uso:   python herramientas/validar_repositorio.py

Comprueba la estructura de carpetas, que index.html este en la raiz (sin el
cual GitHub Pages devuelve 404), que no queden archivos temporales ni
versiones duplicadas, y que los artefactos tengan el numero de paginas
esperado.
"""
import os, re, sys, subprocess
import xml.dom.minidom as minidom

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)

V, R, A, F = '\033[92m', '\033[91m', '\033[93m', '\033[0m'
errores, avisos = [], []

def ok(cond, texto, detalle='', critico=True):
    if cond:
        print('   [%sOK%s] %s' % (V, F, texto))
    else:
        etiqueta = '%s--%s' % (R, F) if critico else '%s!!%s' % (A, F)
        print('   [%s] %s' % (etiqueta, texto))
        (errores if critico else avisos).append(texto)
    if detalle:
        print('        %s' % detalle)

def titulo(t):
    print('\n%s\n%s' % (t, '=' * 68))

print('\nVALIDACION DEL REPOSITORIO')
print('Carpeta: %s' % RAIZ)

# ------------------------------------------------ estructura obligatoria
titulo('1. ARCHIVOS Y CARPETAS OBLIGATORIOS')
requeridos = [
    ('index.html',                                             'archivo'),
    ('README.md',                                              'archivo'),
    ('.gitignore',                                             'archivo'),
    ('arquitectura/modelo-4mas1.drawio',                       'archivo'),
    ('prototipos/baja-fidelidad/ideacion-y-wireframes.drawio', 'archivo'),
    ('prototipos/alta-fidelidad/prototipo-interactivo.html',   'archivo'),
    ('documentacion',                                          'carpeta'),
    ('herramientas',                                           'carpeta'),
]
for ruta, tipo in requeridos:
    existe = os.path.isdir(ruta) if tipo == 'carpeta' else os.path.isfile(ruta)
    ok(existe, '%s %s' % (tipo.capitalize(), ruta))

# ------------------------------------------------ GitHub Pages
titulo('2. GITHUB PAGES')
en_raiz = os.path.isfile('index.html')
ok(en_raiz, 'index.html esta en la raiz del repositorio',
   'Sin este archivo en la raiz, Pages responde 404.' if not en_raiz else '')

if en_raiz:
    h = open('index.html', encoding='utf-8').read()
    ext = re.findall(r'(?:src|href)="(https?://[^"]+)"', h)
    ok(not ext, 'index.html no depende de recursos externos',
       ', '.join(ext) if ext else 'autocontenido', critico=False)
    ok('<!DOCTYPE html>' in h[:200], 'index.html declara DOCTYPE')
    d = (len(re.findall(r'<div[ >]', h)), len(re.findall(r'</div>', h)))
    ok(d[0] == d[1], 'HTML balanceado', '%d aperturas / %d cierres' % d)

# ------------------------------------------------ limpieza
titulo('3. LIMPIEZA')
temporales, duplicados, ocultos = [], [], []
for base, dirs, files in os.walk('.'):
    if '.git' in base:
        continue
    for f in files:
        p = os.path.join(base, f).replace('.' + os.sep, '')
        if f.startswith('~$'):
            temporales.append(p)
        if re.search(r'_v\d+\.|_FINAL|_copia|\bcopy\b| \(\d\)', f, re.I):
            duplicados.append(p)
        if f.endswith(('.bkp', '.dtmp', '.tmp')):
            temporales.append(p)

ok(not temporales, 'Sin archivos temporales', '\n        '.join(temporales))
ok(not duplicados, 'Sin versiones duplicadas en los nombres',
   '\n        '.join(duplicados), critico=False)

# ------------------------------------------------ artefactos
titulo('4. ARTEFACTOS')
esperado = {
    'arquitectura/modelo-4mas1.drawio': 11,
    'prototipos/baja-fidelidad/ideacion-y-wireframes.drawio': 9,
}
for ruta, n in esperado.items():
    if not os.path.isfile(ruta):
        continue
    try:
        d = minidom.parse(ruta)
        pgs = [x.getAttribute('name') for x in d.getElementsByTagName('diagram')]
        dup = len(pgs) != len(set(pgs))
        ok(len(pgs) == n and not dup,
           '%s: %d paginas' % (os.path.basename(ruta), len(pgs)),
           'se esperaban %d%s' % (n, ' · hay nombres repetidos' if dup else '')
           if (len(pgs) != n or dup) else '')
    except Exception as e:
        ok(False, 'XML valido: %s' % ruta, str(e)[:60])

# ------------------------------------------------ tamano
titulo('5. TAMANO')
total = 0
grandes = []
for base, dirs, files in os.walk('.'):
    if '.git' in base:
        continue
    for f in files:
        p = os.path.join(base, f)
        s = os.path.getsize(p)
        total += s
        if s > 25 * 1024 * 1024:
            grandes.append('%s (%.1f MB)' % (p, s / 1024 / 1024))
ok(not grandes, 'Ningun archivo supera los 25 MB',
   '\n        '.join(grandes) if grandes else '')
ok(total < 100 * 1024 * 1024, 'Repositorio bajo 100 MB',
   'total: %.1f MB' % (total / 1024 / 1024))

# ------------------------------------------------ estado de git
titulo('6. ESTADO DE GIT')
def git(*args):
    try:
        return subprocess.run(['git'] + list(args), capture_output=True,
                              text=True, timeout=10).stdout.strip()
    except Exception:
        return None

if os.path.isdir('.git'):
    rama = git('rev-parse', '--abbrev-ref', 'HEAD')
    ok(rama == 'main', 'Rama actual: %s' % (rama or 'desconocida'),
       'GitHub Pages espera "main"' if rama != 'main' else '', critico=False)
    pend = git('status', '--porcelain')
    ok(not pend, 'Sin cambios sin confirmar',
       '%d archivo(s) pendiente(s)' % len(pend.splitlines()) if pend else '',
       critico=False)
    rem = git('remote', 'get-url', 'origin')
    ok(bool(rem), 'Remoto configurado', rem or 'falta: git remote add origin ...',
       critico=False)
    n = git('rev-list', '--count', 'HEAD')
    if n:
        print('        %s commit(s) en el historial' % n)
else:
    print('   [%s!!%s] Aun no es un repositorio Git' % (A, F))
    print('        Ejecute: git init && git branch -M main')
    avisos.append('sin repositorio git')

# ------------------------------------------------ resumen
titulo('RESUMEN')
if errores:
    print('   %s%d problema(s) que impiden subir:%s' % (R, len(errores), F))
    for e in errores:
        print('     - %s' % e)
if avisos:
    print('   %s%d aviso(s):%s' % (A, len(avisos), F))
    for a in avisos:
        print('     - %s' % a)
if not errores:
    print('\n   %sEl repositorio esta listo para subir.%s' % (V, F))
    print('   Siguiente paso: consulte PUBLICAR.md')
print()
sys.exit(1 if errores else 0)
