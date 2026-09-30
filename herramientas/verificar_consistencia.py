#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica la consistencia entre los tres artefactos del proyecto SGGC.

Uso:   python herramientas/verificar_consistencia.py

Comprueba que la arquitectura, el prototipo de baja fidelidad y el de alta
fidelidad describan el mismo sistema: mismas funcionalidades, mismos estados
de dominio y mismos datos de ejemplo.
"""
import os, re, sys
import xml.dom.minidom as minidom

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ  = os.path.join(RAIZ, 'arquitectura', 'modelo-4mas1.drawio')
BAJA = os.path.join(RAIZ, 'prototipos', 'baja-fidelidad', 'ideacion-y-wireframes.drawio')
ALTA = os.path.join(RAIZ, 'prototipos', 'alta-fidelidad', 'prototipo-interactivo.html')

VERDE, ROJO, AMAR, FIN = '\033[92m', '\033[91m', '\033[93m', '\033[0m'
fallos = []

def leer(p):
    return open(p, encoding='utf-8').read()

def paginas(p):
    d = minidom.parse(p)
    return [x.getAttribute('name') for x in d.getElementsByTagName('diagram')]

def marca(ok, texto, detalle=''):
    simbolo = VERDE + 'OK' + FIN if ok else ROJO + '--' + FIN
    print('   [%s] %s' % (simbolo, texto))
    if detalle:
        print('        %s' % detalle)
    if not ok:
        fallos.append(texto)

def titulo(t):
    print('\n' + t)
    print('=' * 68)

# ---------------------------------------------------------------- existencia
titulo('1. ARTEFACTOS PRESENTES')
for nombre, ruta in [('Arquitectura 4+1', ARQ),
                     ('Prototipo baja fidelidad', BAJA),
                     ('Prototipo alta fidelidad', ALTA)]:
    marca(os.path.exists(ruta), nombre,
          '' if os.path.exists(ruta) else 'no se encuentra: %s' % ruta)
if fallos:
    print('\nFaltan artefactos. Se interrumpe la verificacion.')
    sys.exit(1)

# ---------------------------------------------------- contenido de cada archivo
titulo('2. CONTENIDO ESPERADO DE CADA ARCHIVO')
pa, pb = paginas(ARQ), paginas(BAJA)

vistas = ['Contexto', 'Escenarios', 'Lógica', 'Proceso', 'Desarrollo', 'Física']
faltan = [v for v in vistas if not any(v.lower() in p.lower() for p in pa)]
marca(not faltan, 'La arquitectura cubre las 5 vistas del modelo 4+1',
      'faltan: %s' % ', '.join(faltan) if faltan else '%d paginas' % len(pa))

ideacion = [p for p in pb if p.startswith('I')]
pantallas = [p for p in pb if p.startswith('P')]
marca(len(ideacion) >= 3, 'El prototipo incluye las tecnicas de ideacion',
      '%d paginas de ideacion' % len(ideacion))
marca(len(pantallas) >= 5, 'El prototipo incluye las pantallas de baja fidelidad',
      '%d paginas de pantallas' % len(pantallas))

marca(not any('Persona' in p or 'Storytelling' in p for p in pa),
      'La arquitectura no contiene material de ideacion (no se solapan)')
marca(not any('Clase' in p or 'Despliegue' in p for p in pb),
      'El prototipo no contiene diagramas de arquitectura (no se solapan)')

# ------------------------------------------------- funcionalidades exigidas
titulo('3. LAS CUATRO FUNCIONALIDADES EN LOS TRES ARTEFACTOS')
ta, tb, tc = leer(ARQ), leer(BAJA), leer(ALTA)
funcs = {
    'Inicio de sesion':        ['sesión', 'sesión', 'Contraseña'],
    'Registro de residentes':  ['residente', 'residente', 'Nuevo residente'],
    'Cuotas y pagos':          ['cuota', 'cuota', 'Historial de cuotas'],
    'Recordatorios/morosidad': ['morosidad', 'morosidad', 'Cuota vencida'],
}
for nombre, (ka, kb, kc) in funcs.items():
    r = [ka.lower() in ta.lower(), kb.lower() in tb.lower(), kc.lower() in tc.lower()]
    marca(all(r), nombre,
          'arquitectura:%s  baja:%s  alta:%s' % tuple('si' if x else 'NO' for x in r))

# ------------------------------------------------- estados del dominio
titulo('4. ESTADOS DE LA CUOTA (modelo de dominio)')
estados = ['Emitida', 'Notificada', 'Pagada', 'Vencida', 'morosidad', 'Regularizada']
for e in estados:
    en_arq = e.lower() in ta.lower()
    en_alta = e.lower() in tc.lower()
    marca(en_arq and en_alta, 'Estado "%s"' % e,
          'arquitectura:%s  alta fidelidad:%s' % ('si' if en_arq else 'NO',
                                                  'si' if en_alta else 'NO'))

# ------------------------------------------------- datos de ejemplo
titulo('5. COHERENCIA DE LOS DATOS DE EJEMPLO')
datos = {
    'Unidad de ejemplo 1204':   ('1204', tb, tc),
    'Saldo adeudado $100.470':  ('100.470', tb, tc),
    'Cuota base $98.500':       ('98.500', tb, tc),
    'Residente Ana Rojas':      ('Ana Rojas', tb, tc),
    'Total de 160 unidades':    ('160', ta, tc),
}
for nombre, (valor, f1, f2) in datos.items():
    r1, r2 = valor in f1, valor in f2
    marca(r1 and r2, nombre,
          'presente en ambos' if r1 and r2 else 'falta en %s' %
          ('el primero' if not r1 else 'el segundo'))

viejo = '148.500'
marca(viejo not in tb and viejo not in tc,
      'Sin rastros del monto antiguo ($148.500)')

# ------------------------------------------------- integridad tecnica
titulo('6. INTEGRIDAD TECNICA')
for nombre, ruta in [('modelo-4mas1.drawio', ARQ),
                     ('ideacion-y-wireframes.drawio', BAJA)]:
    try:
        minidom.parse(ruta); ok = True; det = '%d paginas' % len(paginas(ruta))
    except Exception as e:
        ok = False; det = str(e)[:60]
    marca(ok, 'XML valido: %s' % nombre, det)

divs = (len(re.findall(r'<div[ >]', tc)), len(re.findall(r'</div>', tc)))
marca(divs[0] == divs[1], 'HTML balanceado', '%d aperturas / %d cierres' % divs)

defs = set(re.findall(r'function\s+(\w+)\s*\(', tc))
llam = set(re.findall(r'onclick="(\w+)\(', tc))
marca(not (llam - defs), 'Sin funciones invocadas y no definidas',
      ', '.join(llam - defs) if (llam - defs) else '%d funciones' % len(defs))

ids  = set(re.findall(r'\bid="([^"]+)"', tc))
refs = set(re.findall(r"[md]Go\('([^']+)'\)", tc))
rotas = [r for r in refs if r not in ids]
marca(not rotas, 'Sin navegacion rota en el prototipo',
      ', '.join(rotas) if rotas else '%d destinos' % len(refs))

ext = re.findall(r'(?:src|href)="(https?://[^"]+)"', tc)
marca(not ext, 'Prototipo autocontenido, sin dependencias externas',
      ', '.join(ext) if ext else 'ningun recurso externo')

# ------------------------------------------------- resumen
titulo('RESUMEN')
if fallos:
    print('   %s%d verificacion(es) fallida(s)%s' % (ROJO, len(fallos), FIN))
    for f in fallos:
        print('     - %s' % f)
    sys.exit(1)
print('   %sTodas las verificaciones pasaron.%s' % (VERDE, FIN))
print('   Los tres artefactos describen el mismo sistema de forma consistente.')
