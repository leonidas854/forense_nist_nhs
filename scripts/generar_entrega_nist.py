#!/usr/bin/env python3
"""Compone la entrega académica sin abrir muestras ni modificar evidencia."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import re
import subprocess
import textwrap
from datetime import datetime, timezone
from html import escape
from pathlib import Path

import markdown
from bs4 import BeautifulSoup, NavigableString
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT, WD_SECTION_START
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageBreak, PageTemplate, NextPageTemplate, Paragraph, Spacer, Table,
    TableStyle, XPreformatted, KeepTogether,
)
from reportlab.platypus.tableofcontents import TableOfContents
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'entrega_nist'
AUTHORS = json.loads((OUT / 'autores.json').read_text())
WIDTH = 508
FONTDIR = Path(subprocess.run(
    ['fc-match', '-f', '%{file}', 'DejaVu Sans'],
    check=True, capture_output=True, text=True).stdout).parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


GRAPHS = {
    'osi_red_host': '''
    a [label="Proceso y APIs de Windows\\nDos vistas del trabajo solicitado"];
    subgraph cluster_red {
      label="COMUNICACIÓN: siete capas OSI"; fontname="DejaVu Sans";
      osi7 [label="7 Aplicación\\nHTTP / SMB"];
      osi6 [label="6 Presentación\\nNo aislada en estas funciones"];
      osi5 [label="5 Sesión\\nNo reconstruida aquí"];
      osi4 [label="4 Transporte\\nTCP / puerto 445 (indicio)"];
      osi3 [label="3 Red\\nIP: sin captura local"];
      osi2 [label="2 Enlace\\nNIC / tecnología no identificada"];
      osi1 [label="1 Física\\nMedio no identificado"];
      osi7 -> osi6 -> osi5 -> osi4 -> osi3 -> osi2 -> osi1;
    }
    subgraph cluster_local {
      label="HOST: operaciones de Windows, fuera de OSI"; fontname="DejaVu Sans";
      h1 [label="Recursos PE y memoria\\nLocalizar e interpretar datos"];
      h2 [label="Archivos y servicios\\nSolicitar cambios"];
      h3 [label="Procesos y token\\nCondiciones y ejecución solicitada"];
      h1 -> h2 -> h3 [style=dashed, label="Dependencia según función"];
    }
    a -> osi7; a -> h1;
    ''',
    'metodo': '''
    a [label="Pregunta y alcance"];
    b [label="Recolección y preservación\nOrigen, identidad y registro"];
    c [label="Examen\nBytes, recursos, Listing y C"];
    d [label="Análisis\nCondiciones y fuentes"];
    e [shape=diamond, label="¿Soporte\nsuficiente?"];
    f [label="Informe: conclusión\ny límites"];
    g [label="Hipótesis y prueba\npendiente"];
    h [label="Mapeo retrospectivo CSF\ny revisión colectiva"];
    a -> b -> c -> d -> e;
    e -> f [label="Sí, para esa afirmación"];
    e -> g [label="No"];
    f -> h; g -> h;
    ''',
    'historia': '''
    a [label="Marzo–abril de 2017\nCorrecciones y avisos disponibles"];
    b [label="Persisten equipos expuestos\nVerificación de avisos insuficiente"];
    c [label="12 de mayo\nBrote y propagación documentada"];
    d [label="Infecciones y perturbaciones\nImpacto asistencial"];
    e [label="Kill switch\nLimita impacto posterior"];
    f [label="Respuesta institucional\nCoordinación y desconexiones"];
    g [label="Recuperación progresiva\nReinstalación y parcheo documentados"];
    h [label="Revisiones 2017–2018\nLecciones y seguimiento"];
    a -> b -> c; c -> d -> f -> g -> h; c -> e;
    ''',
    'componentes': '''
    a [label="24d004…\nPE32 x86"];
    b [label="ed01…\nPE32 x86"];
    z [label="ZIP: 36 miembros"];
    u [label="u.wnry"];
    t [label="t.wnry y otros\ncomponentes"];
    d [label="ec1383…\nDLL x64"];
    w [label="W/101\nLongitud + datos"];
    p [label="PE 93db4b26…\nDistinto de 24d004…"];
    a -> b [label="R/1831: identidad"];
    b -> z [label="XIA/2058"];
    z -> u; z -> t;
    d -> w [label="Contiene recurso"];
    w -> p [label="Tramo desde +4"];
    {rank=same; a; d;}
    ''',
    '24d004': '''
    a [label="00408140\nInternetOpenUrlA"];
    b [shape=diamond, label="¿Handle\nNULL?"];
    c [label="Llamar 00408090\nDistribuir por argumentos"];
    d [label="Evitar esa llamada"];
    e [label="Retorno 0"];
    a -> b; b -> c [label="Sí"]; b -> d [label="No"];
    c -> e; d -> e;
    ''',
    'ed01': '''
    a [label="00401fe7\nRuta y argumentos"];
    b [shape=diamond, label="¿Se cumple toda la\nrama de salida inicial?"];
    c [label="Directorio y paquete\nSolicitudes de atributos/permisos"];
    d [shape=diamond, label="¿Condiciones previas\nsuperadas?"];
    e [label="Leer y procesar t.wnry\nBuscar destino TaskStart"];
    q [shape=diamond, label="¿Lectura, procesamiento\ny destino válidos?"];
    call [label="CALL EAX\nSolicitud de ejecución indirecta"];
    f [label="Salida / limpieza según rama\nRetorno 0"];
    a -> b; b -> f [label="Sí"]; b -> c [label="No"];
    c -> d; d -> e [label="Sí"]; d -> f [label="No"];
    e -> q; q -> call [label="Sí"]; q -> f [label="No"]; call -> f;
    ''',
    'u_wnry': '''
    a [label="Dato 00420fd8\nReferencia y copia en Listing"];
    b [label="CALL 00401bb0\nConsulta de SID/token"];
    c [shape=diamond, label="¿Retorno\nno cero?"];
    d [label="00401a90\nSolicitud CreateProcessA"];
    e [label="00401b50\nShellExecuteExA, verbo runas"];
    f [label="Efecto externo no observado\nRequiere evidencia adicional"];
    a -> b -> c; c -> d [label="Sí"]; c -> e [label="No"];
    d -> f; e -> f;
    ''',
    'ec1383': '''
    a [label="180001014\nFind / Load / Lock / SizeofResource"];
    b [shape=diamond, label="¿Controles iniciales\nsuperados?"];
    c [label="Leer longitud inicial\nSolicitar CreateFileA"];
    d [shape=diamond, label="¿Handle de archivo\nválido?"];
    e [label="WriteFile desde recurso +4\nNo comprobar resultado; cerrar"];
    f [label="Retorno 1"];
    g [label="Retorno 0"];
    a -> b; b -> g [label="No"]; b -> c [label="Sí"];
    c -> d; d -> f [label="No"]; d -> e [label="Sí"]; e -> f;
    ''',
}


def render_graphs():
    folder = OUT / 'figuras'
    folder.mkdir(exist_ok=True)
    # Negro sobre blanco: luminancias 0 y 1; (1 + .05) / (0 + .05) = 21.
    assert (1 + .05) / .05 >= 4.5
    authored_bpmn = {'24d004', 'ed01', 'u_wnry', 'ec1383'}
    for name, body in GRAPHS.items():
        dot = folder / f'{name}.dot'
        if name in authored_bpmn and dot.exists():
            for fmt in ('svg', 'png'):
                subprocess.run(['dot', f'-T{fmt}', '-Gdpi=180', str(dot),
                                '-o', str(folder / f'{name}.{fmt}')], check=True)
            continue
        dot.write_text('digraph G {\n'
                       'graph [rankdir=TB,bgcolor="white",pad=.15,nodesep=.3,ranksep=.32];\n'
                       'node [shape=box,fontname="DejaVu Sans",fontsize=12,color="black",'
                       'fontcolor="black",style="filled",fillcolor="white",margin=".14,.10"];\n'
                       'edge [fontname="DejaVu Sans",fontsize=10,color="black",fontcolor="black"];\n'
                       + body.strip() + '\n}\n')
        for fmt in ('svg', 'png'):
            subprocess.run(['dot', f'-T{fmt}', '-Gdpi=160', str(dot),
                            '-o', str(folder / f'{name}.{fmt}')], check=True)


def transcripts():
    index = json.loads((ROOT / 'equipo/indice.json').read_text())
    sections, manifest = [], []
    for item, title in zip(index['participantes'], ['24d004…', 'ed01…', 'u.wnry', 'ec1383…']):
        src = ROOT / 'equipo' / item['carpeta'] / 'codigo.md'
        blocks = re.findall(r'```c\n(.*?)```', src.read_text(), re.S)
        assert len(blocks) == len(item['funciones'])
        for fn, code in zip(item['funciones'], blocks):
            sha = hashlib.sha256(code.encode()).hexdigest()
            assert sha == fn['bloque_publicado_sha256'], (title, fn['direccion'])
            sections.append(f"### {title} · {fn['direccion']}\n\n"
                            f"Nombre en exportación: {fn['nombre']}.\n\n"
                            f"```c\n{code}```\n")
            manifest.append({'componente': title, 'direccion': fn['direccion'],
                             'sha256_texto': sha, 'fuente': str(src.relative_to(ROOT)),
                             'consulta_utc': item['consulta_utc']})
    return '\n'.join(sections), manifest


def composed(source, code):
    txt = source.read_text()
    txt = re.sub(r'\{\{INCLUIR:([^}]+)\}\}',
                 lambda m: (OUT / m[1]).read_text().replace('(../figuras/', '(figuras/'), txt)
    txt = txt.replace('{{TRANSCRIPCIONES}}', code)
    assert '{{' not in txt
    return txt


def pdf_inline(node):
    if isinstance(node, NavigableString):
        return escape(str(node))
    inner = ''.join(pdf_inline(x) for x in node.children)
    if node.name in ('strong', 'b'):
        return f'<b>{inner}</b>'
    if node.name in ('em', 'i'):
        return f'<i>{inner}</i>'
    if node.name == 'code':
        return f'<font name="DVMono" size="8">{inner}</font>'
    if node.name == 'a' and node.get('href', '').startswith('https://'):
        return f'<link href="{escape(node["href"], quote=True)}"><u>{inner}</u></link>'
    if node.name == 'br':
        return '<br/>'
    return inner


class Report(BaseDocTemplate):
    def __init__(self, filename, short_title, title):
        super().__init__(str(filename), pagesize=letter, leftMargin=52,
                         rightMargin=52, topMargin=50, bottomMargin=50,
                         title=title, author='; '.join(AUTHORS['autores']))
        self.short_title = short_title
        normal = PageTemplate(id='normal', pagesize=letter,
            frames=Frame(52, 50, WIDTH, 692, leftPadding=0, rightPadding=0,
                         topPadding=0, bottomPadding=0), onPage=self.page_decoration)
        figure = PageTemplate(id='figure', pagesize=landscape(letter),
            frames=Frame(36, 36, 720, 540, leftPadding=0, rightPadding=0,
                         topPadding=0, bottomPadding=0), onPage=self.figure_decoration)
        self.addPageTemplates([normal, figure])

    def page_decoration(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.black)
        if doc.page > 1:
            canvas.setFont('DV', 8)
            canvas.drawString(52, 764, self.short_title)
            canvas.drawRightString(560, 764, 'Informática Forense · 2026')
            canvas.setLineWidth(.4)
            canvas.line(52, 754, 560, 754)
        canvas.setFont('DV', 8)
        canvas.drawString(52, 28, 'Estudio documental y estático · Aplicación retrospectiva de NIST')
        canvas.drawRightString(560, 28, str(doc.page))
        canvas.restoreState()

    def figure_decoration(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.black)
        canvas.setFont('DV', 8)
        canvas.drawString(36, 586, self.short_title + ' · diagrama BPMN')
        canvas.drawRightString(756, 586, 'Informática Forense · 2026')
        canvas.setLineWidth(.4)
        canvas.line(36, 578, 756, 578)
        canvas.drawString(36, 20, 'Flujo estático reconstruido · no representa ejecución observada')
        canvas.drawRightString(756, 20, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if hasattr(flowable, 'toc_key'):
            text = flowable.getPlainText()
            self.canv.bookmarkPage(flowable.toc_key)
            self.canv.addOutlineEntry(text, flowable.toc_key, level=0)
            self.notify('TOCEntry', (0, text, self.page, flowable.toc_key))


def styles():
    for name, file in [('DV', 'DejaVuSans.ttf'), ('DV-Bold', 'DejaVuSans-Bold.ttf'),
                       ('DV-Italic', 'DejaVuSans-Oblique.ttf'),
                       ('DV-BoldItalic', 'DejaVuSans-BoldOblique.ttf'),
                       ('DVMono', 'DejaVuSansMono.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(FONTDIR / file)))
    pdfmetrics.registerFontFamily('DV', normal='DV', bold='DV-Bold',
                                 italic='DV-Italic', boldItalic='DV-BoldItalic')
    s = getSampleStyleSheet()
    s.add(ParagraphStyle('Body', fontName='DV', fontSize=10, leading=15,
                         spaceAfter=8, textColor=colors.black, splitLongWords=True))
    s.add(ParagraphStyle('Chapter', parent=s['Body'], fontName='DV-Bold',
                         fontSize=16, leading=21, spaceAfter=16, keepWithNext=True))
    s.add(ParagraphStyle('Section', parent=s['Body'], fontName='DV-Bold',
                         fontSize=11.5, leading=16, spaceBefore=10, keepWithNext=True))
    s.add(ParagraphStyle('Cell', parent=s['Body'], fontSize=8, leading=11,
                         spaceAfter=2, wordWrap='CJK'))
    s.add(ParagraphStyle('Caption', parent=s['Body'], fontSize=8.5, leading=12,
                         spaceBefore=6, spaceAfter=12))
    s.add(ParagraphStyle('CodeBlock', fontName='DVMono', fontSize=7,
                         leading=9.2, spaceAfter=10))
    s.add(ParagraphStyle('Cover', parent=s['Body'], alignment=TA_CENTER,
                         fontSize=10, leading=15))
    s.add(ParagraphStyle('CoverTitle', parent=s['Cover'], fontName='DV-Bold',
                         fontSize=19, leading=26, spaceAfter=18))
    return s


def make_pdf(soup, target, title, short, s):
    story = [Spacer(1, 38)]
    for line in [AUTHORS['institucion'], '“' + AUTHORS['denominacion'] + '”',
                 'BOLIVIA', 'PROYECTO FINAL · INFORMÁTICA FORENSE']:
        story.append(Paragraph(escape(line), s['Cover']))
    story.extend([Spacer(1, 35), Paragraph(escape(title), s['CoverTitle']),
                  Paragraph('NIST SP 800-86 · NIST CSF 2.0', s['Cover']),
                  Spacer(1, 28), Paragraph('<b>Autores</b>', s['Cover'])])
    for author in AUTHORS['autores']:
        story.append(Paragraph(escape(author), s['Cover']))
    story.extend([Spacer(1, 26), Paragraph(AUTHORS['lugar'], s['Cover']),
                  Paragraph(AUTHORS['fecha_edicion'], s['Cover']),
                  PageBreak(), Paragraph('Índice de contenido', s['Chapter'])])
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle('TOCline', parent=s['Body'], fontSize=9,
                                     leading=13, spaceBefore=6)]
    story.append(toc)
    for node in soup.children:
        tag = getattr(node, 'name', None)
        if not tag or tag == 'h1':
            continue
        if tag == 'h2':
            story.append(PageBreak())
            p = Paragraph(pdf_inline(node), s['Chapter'])
            p.toc_key = f'chapter-{len(story)}'
            story.append(p)
        elif tag in ('h3', 'h4'):
            story.append(Paragraph(pdf_inline(node), s['Section']))
        elif tag == 'p' and node.find('img'):
            img = node.find('img')
            drawing = svg2rlg(str((OUT / img['src']).with_suffix('.svg')))
            caption = Paragraph(escape(img.get('alt', '')), s['Caption'])
            if 'BPMN' in img.get('alt', ''):
                story.extend([NextPageTemplate('figure'), PageBreak()])
                factor = min(720 / drawing.width, 480 / drawing.height, 1)
                drawing.scale(factor, factor)
                drawing.width *= factor
                drawing.height *= factor
                story.append(KeepTogether([drawing, caption]))
                story.extend([NextPageTemplate('normal'), PageBreak()])
            else:
                factor = min(WIDTH / drawing.width, 470 / drawing.height, 1)
                drawing.scale(factor, factor)
                drawing.width *= factor
                drawing.height *= factor
                story.append(KeepTogether([drawing, caption]))
        elif tag == 'p':
            story.append(Paragraph(pdf_inline(node), s['Body']))
        elif tag in ('ul', 'ol'):
            for n, item in enumerate(node.find_all('li', recursive=False), 1):
                prefix = f'{n}. ' if tag == 'ol' else '• '
                story.append(Paragraph(prefix + pdf_inline(item), s['Body']))
        elif tag == 'pre':
            raw = node.get_text().rstrip('\n')
            lines = []
            for line in raw.splitlines():
                lines.extend(textwrap.wrap(line, width=112, replace_whitespace=False,
                             drop_whitespace=False, break_long_words=True,
                             break_on_hyphens=False) or [''])
            story.append(XPreformatted(escape('\n'.join(lines)), s['CodeBlock']))
        elif tag == 'table':
            rows = []
            for tr in node.find_all('tr'):
                rows.append([Paragraph(pdf_inline(cell), s['Cell'])
                             for cell in tr.find_all(['td', 'th'])])
            count = len(rows[0])
            widths = [WIDTH / count] * count
            if count == 2 and 'SHA-256' in node.get_text():
                widths = [135, WIDTH - 135]
            t = Table(rows, colWidths=widths, repeatRows=1, hAlign='LEFT')
            t.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LINEABOVE', (0, 0), (-1, 0), .8, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), .8, colors.black),
                ('LINEBELOW', (0, -1), (-1, -1), .5, colors.black),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.extend([t, Spacer(1, 12)])
    Report(target, short, title).multiBuild(story)


def word_inline(paragraph, node, bold=False, italic=False, mono=False):
    if isinstance(node, NavigableString):
        run = paragraph.add_run(str(node))
        run.bold, run.italic = bold, italic
        if mono:
            run.font.name, run.font.size = 'DejaVu Sans Mono', Pt(8)
        return
    if node.name == 'a' and node.get('href', '').startswith('https://'):
        rel = paragraph.part.relate_to(node['href'],
            'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
        link = OxmlElement('w:hyperlink'); link.set(qn('r:id'), rel)
        run = OxmlElement('w:r'); prop = OxmlElement('w:rPr')
        under = OxmlElement('w:u'); under.set(qn('w:val'), 'single'); prop.append(under)
        text = OxmlElement('w:t'); text.text = node.get_text()
        run.append(prop); run.append(text); link.append(run); paragraph._p.append(link)
        return
    for child in node.children:
        word_inline(paragraph, child, bold or node.name in ('b', 'strong'),
                    italic or node.name in ('i', 'em'), mono or node.name == 'code')


def make_docx(soup, target, title, short):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.top_margin = sec.bottom_margin = Inches(.7)
    sec.left_margin = sec.right_margin = Inches(.72)
    normal = doc.styles['Normal']
    normal.font.name, normal.font.size = 'DejaVu Sans', Pt(10)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.space_after = Pt(7)
    normal.paragraph_format.line_spacing = 1.15
    for name in ['Title', 'Heading 1', 'Heading 2', 'Heading 3']:
        doc.styles[name].font.name = 'DejaVu Sans'
        doc.styles[name].font.color.rgb = RGBColor(0, 0, 0)
    doc.styles['Caption'].font.name = 'DejaVu Sans'
    doc.styles['Caption'].font.color.rgb = RGBColor(0, 0, 0)
    doc.core_properties.title = title
    doc.core_properties.author = '; '.join(AUTHORS['autores'])
    for line in [AUTHORS['institucion'], '“' + AUTHORS['denominacion'] + '”',
                 'BOLIVIA', '', 'PROYECTO FINAL · INFORMÁTICA FORENSE', '']:
        p = doc.add_paragraph(line); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph(title, 'Title'); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph('NIST SP 800-86 · NIST CSF 2.0'); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()
    for author in AUTHORS['autores']:
        p = doc.add_paragraph(author); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
    for line in ['', AUTHORS['lugar'], AUTHORS['fecha_edicion']]:
        p = doc.add_paragraph(line); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()
    doc.add_heading('Índice de contenido', 1)
    for heading in soup.find_all('h2'):
        doc.add_paragraph(heading.get_text())
    header = sec.header.paragraphs[0]
    header.text = short + ' · Informática Forense'
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    field = OxmlElement('w:fldSimple'); field.set(qn('w:instr'), 'PAGE'); footer._p.append(field)
    for node in soup.children:
        tag = getattr(node, 'name', None)
        if not tag or tag == 'h1':
            continue
        if tag == 'h2':
            doc.add_page_break(); doc.add_heading(node.get_text(), 1)
        elif tag in ('h3', 'h4'):
            doc.add_heading(node.get_text(), 2)
        elif tag == 'p' and node.find('img'):
            img = node.find('img')
            path = OUT / img['src']
            if 'BPMN' in img.get('alt', ''):
                section = doc.add_section(WD_SECTION_START.NEW_PAGE)
                section.orientation = WD_ORIENT.LANDSCAPE
                section.page_width, section.page_height = Inches(11), Inches(8.5)
                section.top_margin = section.bottom_margin = Inches(.45)
                section.left_margin = section.right_margin = Inches(.55)
                doc.add_picture(str(path), width=Inches(9.8))
                doc.add_paragraph(img.get('alt', ''), 'Caption')
                section = doc.add_section(WD_SECTION_START.NEW_PAGE)
                section.orientation = WD_ORIENT.PORTRAIT
                section.page_width, section.page_height = Inches(8.5), Inches(11)
                section.top_margin = section.bottom_margin = Inches(.7)
                section.left_margin = section.right_margin = Inches(.72)
            else:
                from PIL import Image
                with Image.open(path) as im:
                    width = min(6.5, 6.5 * im.width / im.height)
                doc.add_picture(str(path), width=Inches(width))
                doc.add_paragraph(img.get('alt', ''), 'Caption')
        elif tag == 'p':
            word_inline(doc.add_paragraph(), node)
        elif tag in ('ul', 'ol'):
            for item in node.find_all('li', recursive=False):
                word_inline(doc.add_paragraph(style='List Number' if tag == 'ol' else 'List Bullet'), item)
        elif tag == 'pre':
            for line in node.get_text().rstrip('\n').splitlines():
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1
                r = p.add_run(line); r.font.name = 'DejaVu Sans Mono'; r.font.size = Pt(7)
        elif tag == 'table':
            rows = node.find_all('tr')
            table = doc.add_table(rows=0, cols=len(rows[0].find_all(['td', 'th'])))
            table.style = 'Table Grid'
            for number, row in enumerate(rows):
                cells = table.add_row().cells
                for cell, src in zip(cells, row.find_all(['td', 'th'])):
                    p = cell.paragraphs[0]; word_inline(p, src)
                    for run in p.runs:
                        run.font.size = Pt(8)
                        if number == 0:
                            run.bold = True
                if number == 0:
                    repeat = OxmlElement('w:tblHeader')
                    table.rows[0]._tr.get_or_add_trPr().append(repeat)
            doc.add_paragraph()
    doc.save(target)


def main():
    render_graphs()
    code, code_manifest = transcripts()
    style = styles()
    composed_dir = OUT / 'lectura_completa'
    composed_dir.mkdir(exist_ok=True)
    jobs = [('informe_general.md', 'INFORME_GENERAL_NIST_NHS', 'Informe general'),
            ('parte_practica.md', 'PARTE_PRACTICA_NIST_GHIDRA', 'Parte práctica')]
    for source, name, short in jobs:
        text = composed(OUT / source, code)
        (composed_dir / source).write_text(text.replace('(figuras/', '(../figuras/').rstrip() + '\n')
        soup = BeautifulSoup(markdown.markdown(text, extensions=['tables', 'fenced_code']), 'html.parser')
        title = soup.h1.get_text()
        make_pdf(soup, OUT / (name + '.pdf'), title, short, style)
        make_docx(soup, OUT / (name + '.docx'), title, short)
        print('Generado:', name)
    metadata = {
        'generado_utc': datetime.now(timezone.utc).isoformat(),
        'fecha_editorial': '2026-11-21',
        'contraste_figuras': 'Negro/blanco 21:1; etiquetas y formas, no solo color',
        'dependencias': {p: importlib.metadata.version(p) for p in
                        ['reportlab', 'python-docx', 'Markdown', 'beautifulsoup4', 'svglib']},
        'graphviz': subprocess.run(['dot', '-V'], capture_output=True, text=True).stderr.strip(),
        'transcripciones': code_manifest,
    }
    (OUT / 'construccion.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
    files = sorted(p for p in OUT.rglob('*') if p.is_file() and p.name != 'SHA256SUMS')
    (OUT / 'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.relative_to(OUT)}\n' for p in files))


if __name__ == '__main__':
    main()
