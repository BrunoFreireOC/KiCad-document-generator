# Bruno 'Jesus' Claudino
# Formula E-Motion UFPB
# 0.4.0


import os
import subprocess
import csv
from PyPDF2 import PdfMerger
from PIL import Image
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from extra_functions import *

# Caminhos
project_path = "/media/bruno-claudino/Dados/Google_DRIVE/DRIVE_Cear/KiCad/Sensor temp/mux_teste"
project_name = "mux_teste"
kicad_cli_path = r"/bin/kicad-cli"

# Projetos
schematic_file = os.path.join(project_path, f"{project_name}.kicad_sch")
board_file = os.path.join(project_path, f"{project_name}.kicad_pcb")
output_dir = os.path.join(project_path, "exportados")
os.makedirs(output_dir, exist_ok=True)

# Tamanho A4
A4_width = "854"
A4_height = "604"



# 1. Exportar PDF do esquemático
schematic_pdf = os.path.join(output_dir, "esquematico.pdf")
if os.path.exists(schematic_pdf):
    print("Removendo PDF esquema anterior...")
    os.remove(schematic_pdf)
subprocess.run([
    kicad_cli_path, "sch", "export", "pdf",
    schematic_file,
    "--output", schematic_pdf,
    "--no-background-color"
], check=True)

# 2. Exportar PDF da PCB (face top e bottom)
pcb_pdf = os.path.join(output_dir, "pcb.pdf")
if os.path.exists(pcb_pdf):
    print("Removendo PDF PCB anterior...")
    os.remove(pcb_pdf)
subprocess.run([
    kicad_cli_path, "pcb", "export", "pdf",
    board_file,
    "--output", pcb_pdf,
    "--theme", "user",
    "--layers", "B.Cu,F.Cu,F.Silkscreen,B.Silkscreen,Edge.Cuts,User.Drawings",
    "--mode-single",
    "--include-border-title"
], check=True)

# 3. Exportar BOM (CSV)
bom_csv = os.path.join(output_dir, "bom.csv")
if os.path.exists(bom_csv):
    print("Removendo BOM .csv anterior...")
    os.remove(bom_csv)
subprocess.run([
    kicad_cli_path, "sch", "export", "bom",
    schematic_file,
    "--output", bom_csv,
    "--ref-range-delimiter", "",
    "--keep-tabs",
    "--keep-line-breaks",
    "--format-preset", "CSV"
], check=True)
    # 3.1 Converter CSV da BOM para PDF com tabela
bom_pdf = os.path.join(output_dir, "bom.pdf")
if os.path.exists(bom_pdf):
    print("Removendo BOM PDF anterior...")
    os.remove(bom_pdf)
def create_bom_pdf(csv_path, pdf_path, refs_per_line=6):
    data = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        rows = list(reader)

    header = rows[0]
    data.append(header)

    # Detecta a coluna de referências
    ref_col_index = next((i for i, col in enumerate(header) if "ref" in col.lower()), None)

    for row in rows[1:]:
        if ref_col_index is not None and len(row) > ref_col_index:
            refs = row[ref_col_index].replace(" ", "").split(",")
            wrapped_refs = "\n".join([", ".join(refs[i:i+refs_per_line]) for i in range(0, len(refs), refs_per_line)])
            row[ref_col_index] = wrapped_refs
        data.append(row)
    pdf = SimpleDocTemplate(pdf_path, pagesize=landscape(A4))
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    pdf.build([table])

bom_agrupado_csv = os.path.join(output_dir, "bom_agrupado.csv")
if os.path.exists(bom_agrupado_csv):
    print("Removendo BOM  agrupado .csv anterior...")
    os.remove(bom_agrupado_csv)
group_bom(bom_csv, bom_agrupado_csv)
create_bom_pdf(bom_agrupado_csv, bom_pdf)

# 4. Exportar imagem 3D com qualidade alta (simulando raytracing)
raytrace_png = os.path.join(output_dir, "render3d.png")
if os.path.exists(raytrace_png):
    print("Removendo PNG 3D anterior...")
    os.remove(raytrace_png)
    
subprocess.run([
    kicad_cli_path, "pcb", "render",
    "--output", raytrace_png,
    "--width", A4_width,
    "--height", A4_height,
    "--quality", "high",
    "--background", "opaque",
    "--floor",
    board_file
], check=True)

# 5. Exportar imagem 3D com qualidade alta (parte debaixo)
raytrace_bottom_png = os.path.join(output_dir, "render3d_bottom.png")
if os.path.exists(raytrace_bottom_png):
    print("Removendo PNG 3D anterior...")
    os.remove(raytrace_bottom_png)
    
subprocess.run([
    kicad_cli_path, "pcb", "render",
    "--output", raytrace_bottom_png,
    "--width", A4_width,
    "--height", A4_height,
    "--quality", "high",
    "--background", "opaque",
    "--rotate", r"'-180,0,0'",
    "--floor",
    board_file
], check=True)

# 6. Exportar imagem 3D com qualidade alta com visao isometrica
raytrace_iso_png = os.path.join(output_dir, "render3d_iso.png")
if os.path.exists(raytrace_iso_png):
    print("Removendo PNG 3D isometrica anterior...")
    os.remove(raytrace_iso_png)
subprocess.run([
    kicad_cli_path, "pcb", "render",
    "--output", raytrace_iso_png,
    "--width", A4_width,
    "--height", A4_height,
    "--quality", "high",
    "--background", "opaque",
    "--perspective",
    "--zoom", "0.85",
    "--rotate", r"'-35,0,-45'",
    "--floor",
    board_file
], check=True)

# 7. Converter imagens para PDF (normal, bottom e isometrica)
render_pdf = os.path.join(output_dir, "render3d.pdf")
image = Image.open(raytrace_png).convert("RGB")
image.save(render_pdf)

render_bottom_pdf = os.path.join(output_dir, "render3d_bottom.pdf")
image = Image.open(raytrace_bottom_png).convert("RGB")
image.save(render_bottom_pdf)

render_iso_pdf = os.path.join(output_dir, "render3d_iso.pdf")
image = Image.open(raytrace_iso_png).convert("RGB")
image.save(render_iso_pdf)


# 8. Juntar tudo em um único PDF
final_pdf = os.path.join(output_dir, "projeto_completo.pdf")
if os.path.exists(final_pdf):
    print("Removendo PDF projeto completo anterior...")
    os.remove(final_pdf)
    
merger = PdfMerger()
print("Mesclando PDFs...")
for pdf in [schematic_pdf, pcb_pdf, bom_pdf, render_pdf, render_bottom_pdf, render_iso_pdf]:
    merger.append(pdf)
merger.write(final_pdf)
merger.close()

print(f"PDF final gerado em: {final_pdf}")
