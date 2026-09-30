#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sube el repositorio a GitHub con un historial de commits por fase.

Uso:   python herramientas/subir_a_github.py

Valida primero y se detiene si algo esta mal. Pide confirmacion antes de
sobrescribir lo que haya en GitHub.
"""
import os, sys, subprocess

REMOTO = 'https://github.com/FcoXavierParra/GRY2203_S8_FPARRA.git'
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
V, R, A, F = '\033[92m', '\033[91m', '\033[93m', '\033[0m'

FASES = [
    (['arquitectura'],                    'Modelado arquitectonico bajo el marco 4+1'),
    (['prototipos/baja-fidelidad'],       'Ideacion y prototipo de baja fidelidad'),
    (['prototipos/alta-fidelidad', 'index.html'],
                                          'Prototipo interactivo de alta fidelidad'),
    (['documentacion'],                   'Documentacion de cierre: DAS, lecciones aprendidas y acta'),
    (['herramientas', 'README.md', '.gitignore', 'PUBLICAR.md', '.vscode'],
                                          'Herramientas de validacion y documentacion del repositorio'),
]

def corre(*args, check=True):
    print('   $ %s' % ' '.join(args))
    r = subprocess.run(args, capture_output=True, text=True)
    if r.stdout.strip(): print('     %s' % r.stdout.strip()[:300])
    if r.returncode and check:
        print('   %sError:%s %s' % (R, F, r.stderr.strip()[:300]))
        sys.exit(1)
    return r

print('\nSUBIR A GITHUB')
print('=' * 68)

# 1. validar primero
print('\n1. Validando el repositorio...')
r = subprocess.run([sys.executable, 'herramientas/validar_repositorio.py'],
                   capture_output=True, text=True)
if r.returncode:
    print('%s   La validacion fallo. Corrija los problemas antes de subir.%s' % (R, F))
    print(r.stdout[-1500:])
    sys.exit(1)
print('   %sValidacion correcta.%s' % (V, F))

# 2. confirmar
print('\n2. Esta operacion SOBRESCRIBE el contenido actual de:')
print('   %s' % REMOTO)
if input('\n   Escriba "si" para continuar: ').strip().lower() not in ('si', 'sí'):
    print('   Cancelado.')
    sys.exit(0)

# 3. inicializar
print('\n3. Preparando el repositorio local...')
if not os.path.isdir('.git'):
    corre('git', 'init')
corre('git', 'branch', '-M', 'main', check=False)

# 4. commits por fase
print('\n4. Creando el historial por fases...')
for rutas, mensaje in FASES:
    existentes = [r_ for r_ in rutas if os.path.exists(r_)]
    if not existentes:
        continue
    corre('git', 'add', *existentes)
    r = subprocess.run(['git', 'diff', '--cached', '--quiet'])
    if r.returncode:                      # hay algo que confirmar
        corre('git', 'commit', '-m', mensaje)
    else:
        print('   (sin cambios) %s' % mensaje)

# 5. remoto y push
print('\n5. Subiendo...')
r = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
if r.returncode:
    corre('git', 'remote', 'add', 'origin', REMOTO)
else:
    corre('git', 'remote', 'set-url', 'origin', REMOTO)

print('\n   Si pide credenciales: el usuario es su nombre de GitHub y la')
print('   contrasena es un token personal (Settings > Developer settings >')
print('   Personal access tokens > Tokens classic, con permiso "repo").\n')
corre('git', 'push', '-u', 'origin', 'main', '--force')

print('\n' + '=' * 68)
print('%sListo.%s' % (V, F))
print('\n   Repositorio: https://github.com/FcoXavierParra/GRY2203_S8_FPARRA')
print('   Prototipo  : https://fcoxavierparra.github.io/GRY2203_S8_FPARRA/')
print('\n   Revise Settings > Pages: rama "main", carpeta "/ (root)".')
print('   El sitio tarda uno o dos minutos en actualizarse.\n')
