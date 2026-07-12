# =====================================================
# SCRIPT PEMBUAT PPT - Healthcare Data Mining
# Jalankan: python buat_ppt.py
# =====================================================

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# â”€â”€ Warna Tema â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BG_DARK      = RGBColor(0x0A, 0x0E, 0x1A)   # latar utama
BG_CARD      = RGBColor(0x0D, 0x12, 0x24)   # latar kartu
BLUE         = RGBColor(0x60, 0xA5, 0xFA)   # aksen biru
PURPLE       = RGBColor(0xC0, 0x84, 0xFC)   # aksen ungu
GREEN        = RGBColor(0x4A, 0xDE, 0x80)   # aksen hijau
ORANGE       = RGBColor(0xFB, 0x92, 0x3C)   # aksen oranye
WHITE        = RGBColor(0xF1, 0xF5, 0xF9)   # putih terang
GRAY         = RGBColor(0x94, 0xA3, 0xB8)   # abu-abu
LIGHT_BLUE   = RGBColor(0x81, 0x8C, 0xF8)   # biru muda

# Dimensi slide 16:9 widescreen
SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H

blank_layout = prs.slide_layouts[6]   # blank


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# FUNGSI HELPER
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

def add_slide():
    slide = prs.slides.add_slide(blank_layout)
    # Latar belakang gelap
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = BG_DARK
    return slide


def add_rect(slide, l, t, w, h, fill_color=None, line_color=None, line_width=Pt(1)):
    shape = slide.shapes.add_shape(1, l, t, w, h)   # 1 = MSO_SHAPE_TYPE.RECTANGLE
    shape.line.width = 0
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = line_width
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, text, l, t, w, h,
             font_size=Pt(14), bold=False, color=WHITE,
             align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txb = slide.shapes.add_textbox(l, t, w, h)
    txb.word_wrap = wrap
    tf  = txb.text_frame
    tf.word_wrap = wrap
    p   = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = font_size
    run.font.bold  = bold
    run.font.color.rgb = color
    run.font.italic = italic
    run.font.name  = "Calibri"
    return txb


def add_multiline(slide, lines, l, t, w, h,
                  font_size=Pt(13), color=WHITE, bold_first=False):
    """lines = list of strings; tiap string = satu paragraf"""
    txb = slide.shapes.add_textbox(l, t, w, h)
    txb.word_wrap = True
    tf  = txb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_before = Pt(3)
        run = p.add_run()
        run.text = line
        run.font.size  = font_size
        run.font.color.rgb = color
        run.font.bold  = (bold_first and i == 0)
        run.font.name  = "Calibri"
    return txb


def top_accent_bar(slide, color):
    """Garis tipis berwarna di bagian atas slide"""
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.07), fill_color=color)


def slide_number(slide, num, total):
    add_text(slide, f"{num} / {total}",
             SLIDE_W - Inches(1.2), SLIDE_H - Inches(0.4),
             Inches(1.1), Inches(0.35),
             font_size=Pt(10), color=GRAY, align=PP_ALIGN.RIGHT)


def section_badge(slide, label, color, l=Inches(0.4), t=Inches(0.15)):
    add_rect(slide, l, t, Inches(2.4), Inches(0.35),
             fill_color=RGBColor(color[0]//6, color[1]//6, color[2]//6),
             line_color=color, line_width=Pt(1))
    add_text(slide, f"  {label}", l+Inches(0.05), t+Inches(0.02),
             Inches(2.3), Inches(0.32),
             font_size=Pt(10), bold=True, color=RGBColor(*color.rgb),
             align=PP_ALIGN.LEFT)


def card(slide, l, t, w, h, accent_color):
    """Kartu dengan border aksen kiri"""
    add_rect(slide, l, t, w, h,
             fill_color=RGBColor(0x0D, 0x12, 0x24),
             line_color=RGBColor(accent_color[0]//3, accent_color[1]//3, accent_color[2]//3),
             line_width=Pt(0.75))
    add_rect(slide, l, t, Inches(0.06), h, fill_color=accent_color)


TOTAL = 22   # total slide

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 1 â€” COVER
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()

# Gradien visual â†’ pakai dua rect yang overlap
add_rect(sl, Inches(0), Inches(0), SLIDE_W, SLIDE_H,
         fill_color=RGBColor(0x0A, 0x0E, 0x1A))
add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(3.5),
         fill_color=RGBColor(0x0D, 0x14, 0x2E))

# Garis aksen atas
add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(0.1),
         fill_color=LIGHT_BLUE)

# Icon rumah sakit besar
add_text(sl, "ðŸ¥", Inches(0.6), Inches(1.2), Inches(1.5), Inches(1.5),
         font_size=Pt(60), align=PP_ALIGN.CENTER)

# Judul utama
add_text(sl, "Dashboard Healthcare Analytics",
         Inches(2.1), Inches(1.1), Inches(10.5), Inches(1.0),
         font_size=Pt(36), bold=True, color=WHITE)

# Sub judul
add_text(sl, "Penerapan Data Mining untuk Mendukung Pengambilan Keputusan",
         Inches(2.1), Inches(2.0), Inches(10.5), Inches(0.6),
         font_size=Pt(18), color=BLUE)

# Garis pemisah
add_rect(sl, Inches(2.1), Inches(2.75), Inches(9.0), Inches(0.04),
         fill_color=LIGHT_BLUE)

# Info bawah
add_text(sl, "Regresi  â€¢  Klasifikasi  â€¢  Clustering",
         Inches(2.1), Inches(2.95), Inches(10), Inches(0.5),
         font_size=Pt(15), color=PURPLE, bold=True)

add_text(sl, "Data Mining  |  Healthcare Dataset  |  55.500 Record",
         Inches(2.1), Inches(3.45), Inches(10), Inches(0.4),
         font_size=Pt(13), color=GRAY)

# Kotak badge bawah kanan
add_rect(sl, Inches(9.5), Inches(6.5), Inches(3.5), Inches(0.65),
         fill_color=RGBColor(0x1A, 0x20, 0x40),
         line_color=LIGHT_BLUE, line_width=Pt(1))
add_text(sl, "Healthcare Analytics Dashboard  2024",
         Inches(9.6), Inches(6.58), Inches(3.4), Inches(0.5),
         font_size=Pt(10), color=GRAY, align=PP_ALIGN.CENTER)

slide_number(sl, 1, TOTAL)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 2 â€” DAFTAR ISI
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, LIGHT_BLUE)
slide_number(sl, 2, TOTAL)

add_text(sl, "Daftar Isi", Inches(0.5), Inches(0.2), Inches(12), Inches(0.7),
         font_size=Pt(28), bold=True, color=WHITE)
add_rect(sl, Inches(0.5), Inches(0.88), Inches(2.5), Inches(0.05), fill_color=LIGHT_BLUE)

items = [
    ("01", "Latar Belakang & Tujuan",  BLUE),
    ("02", "Dataset yang Digunakan",    BLUE),
    ("03", "Overview Dashboard",        BLUE),
    ("04", "Rancangan 1 â€” Regresi (Linear Regression)",       PURPLE),
    ("05", "Rancangan 2 â€” Klasifikasi (Decision Tree)",        PURPLE),
    ("06", "Rancangan 3 â€” Clustering (K-Means)",               GREEN),
    ("07", "Kesimpulan & Manfaat",      ORANGE),
]

col_w = Inches(5.8)
for i, (num, title, color) in enumerate(items):
    col = i % 2
    row = i // 2
    lx = Inches(0.5) + col * (col_w + Inches(0.4))
    ty = Inches(1.15) + row * Inches(1.15)

    add_rect(sl, lx, ty, col_w, Inches(0.95),
             fill_color=RGBColor(0x0D, 0x12, 0x24),
             line_color=RGBColor(color[0]//3, color[1]//3, color[2]//3),
             line_width=Pt(0.75))
    add_rect(sl, lx, ty, Inches(0.06), Inches(0.95), fill_color=color)

    add_text(sl, num, lx + Inches(0.18), ty + Inches(0.08),
             Inches(0.5), Inches(0.4),
             font_size=Pt(20), bold=True, color=color)
    add_text(sl, title, lx + Inches(0.7), ty + Inches(0.22),
             col_w - Inches(0.8), Inches(0.55),
             font_size=Pt(13), color=WHITE, bold=False)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 3 â€” LATAR BELAKANG & TUJUAN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, BLUE)
slide_number(sl, 3, TOTAL)

add_text(sl, "01  Latar Belakang & Tujuan",
         Inches(0.5), Inches(0.2), Inches(12), Inches(0.65),
         font_size=Pt(26), bold=True, color=WHITE)
add_rect(sl, Inches(0.5), Inches(0.85), Inches(4.0), Inches(0.05), fill_color=BLUE)

# Kolom kiri â€” Latar belakang
card(sl, Inches(0.4), Inches(1.0), Inches(5.9), Inches(5.9), BLUE)
add_text(sl, "ðŸ“‹  Latar Belakang",
         Inches(0.6), Inches(1.1), Inches(5.6), Inches(0.5),
         font_size=Pt(15), bold=True, color=BLUE)

lb_lines = [
    "Rumah sakit menghasilkan data pasien dalam jumlah besar setiap harinya â€” mulai dari data demografis, diagnosis, hingga biaya perawatan.",
    "",
    "Data yang banyak ini seringkali tidak dimanfaatkan secara optimal untuk mendukung pengambilan keputusan.",
    "",
    "Data Mining hadir sebagai solusi untuk mengolah data tersebut menjadi informasi yang berguna bagi manajemen rumah sakit.",
]
add_multiline(sl, lb_lines, Inches(0.6), Inches(1.6), Inches(5.6), Inches(4.5),
              font_size=Pt(13), color=GRAY)

# Kolom kanan â€” Tujuan
card(sl, Inches(6.6), Inches(1.0), Inches(6.3), Inches(5.9), PURPLE)
add_text(sl, "ðŸŽ¯  Tujuan",
         Inches(6.8), Inches(1.1), Inches(6.0), Inches(0.5),
         font_size=Pt(15), bold=True, color=PURPLE)

tujuan = [
    "âœ…  Merancang dashboard interaktif untuk memvisualisasikan data kesehatan pasien",
    "",
    "âœ…  Menerapkan 3 teknik Data Mining:\n     â€¢ Regresi â€” prediksi biaya tagihan\n     â€¢ Klasifikasi â€” prediksi hasil tes\n     â€¢ Clustering â€” segmentasi pasien",
    "",
    "âœ…  Menjelaskan fungsi Data Mining dalam mendukung pengambilan keputusan untuk mencapai tujuan organisasi rumah sakit",
]
add_multiline(sl, tujuan, Inches(6.8), Inches(1.6), Inches(5.9), Inches(4.8),
              font_size=Pt(12.5), color=GRAY)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 4 â€” DATASET
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, BLUE)
slide_number(sl, 4, TOTAL)

add_text(sl, "02  Dataset yang Digunakan",
         Inches(0.5), Inches(0.2), Inches(12), Inches(0.65),
         font_size=Pt(26), bold=True, color=WHITE)
add_rect(sl, Inches(0.5), Inches(0.85), Inches(4.5), Inches(0.05), fill_color=BLUE)

# KPI boxes
kpis = [
    ("55.500", "Total Record", BLUE),
    ("15", "Jumlah Kolom", PURPLE),
    ("6", "Jenis Penyakit", GREEN),
    ("3", "Hasil Tes", ORANGE),
]
for i, (val, lbl, color) in enumerate(kpis):
    lx = Inches(0.4) + i * Inches(3.2)
    add_rect(sl, lx, Inches(1.05), Inches(3.0), Inches(1.05),
             fill_color=RGBColor(0x0D, 0x12, 0x24),
             line_color=RGBColor(color[0]//3, color[1]//3, color[2]//3),
             line_width=Pt(0.75))
    add_rect(sl, lx, Inches(1.05), Inches(3.0), Inches(0.07), fill_color=color)
    add_text(sl, val, lx, Inches(1.18), Inches(3.0), Inches(0.6),
             font_size=Pt(28), bold=True, color=color, align=PP_ALIGN.CENTER)
    add_text(sl, lbl, lx, Inches(1.72), Inches(3.0), Inches(0.35),
             font_size=Pt(11), color=GRAY, align=PP_ALIGN.CENTER)

# Tabel kolom
add_text(sl, "Struktur Kolom Dataset", Inches(0.4), Inches(2.3),
         Inches(12.5), Inches(0.45), font_size=Pt(14), bold=True, color=WHITE)

cols_data = [
    ("Name",               "Teks",  "Nama lengkap pasien"),
    ("Age",                "Angka", "Umur pasien (tahun)"),
    ("Gender",             "Teks",  "Jenis kelamin (Male/Female)"),
    ("Blood Type",         "Teks",  "Golongan darah pasien"),
    ("Medical Condition",  "Teks",  "Diagnosis/penyakit yang diderita"),
    ("Date of Admission",  "Teks",  "Tanggal masuk rawat inap"),
    ("Doctor",             "Teks",  "Nama dokter yang menangani"),
    ("Hospital",           "Teks",  "Nama rumah sakit"),
    ("Insurance Provider", "Teks",  "Nama perusahaan asuransi"),
    ("Billing Amount",     "Angka", "Total tagihan biaya perawatan ($)"),
    ("Room Number",        "Angka", "Nomor kamar yang ditempati"),
    ("Admission Type",     "Teks",  "Jenis rawat inap (Darurat/Elektif/Mendesak)"),
    ("Discharge Date",     "Teks",  "Tanggal keluar dari rumah sakit"),
    ("Medication",         "Teks",  "Nama obat yang diberikan"),
    ("Test Results",       "Teks",  "Hasil tes lab (Normal/Abnormal/Tidak Meyakinkan)"),
]

# Header tabel
hdr_y = Inches(2.75)
add_rect(sl, Inches(0.4), hdr_y, Inches(3.5), Inches(0.32), fill_color=BLUE)
add_rect(sl, Inches(3.95), hdr_y, Inches(1.3), Inches(0.32), fill_color=BLUE)
add_rect(sl, Inches(5.3), hdr_y, Inches(7.6), Inches(0.32), fill_color=BLUE)
add_text(sl, "Nama Kolom", Inches(0.45), hdr_y+Inches(0.04), Inches(3.4), Inches(0.28),
         font_size=Pt(10), bold=True, color=BG_DARK)
add_text(sl, "Tipe", Inches(3.97), hdr_y+Inches(0.04), Inches(1.25), Inches(0.28),
         font_size=Pt(10), bold=True, color=BG_DARK)
add_text(sl, "Keterangan", Inches(5.32), hdr_y+Inches(0.04), Inches(7.5), Inches(0.28),
         font_size=Pt(10), bold=True, color=BG_DARK)

row_h = Inches(0.285)
for i, (col_name, col_type, keterangan) in enumerate(cols_data):
    ry = hdr_y + Inches(0.33) + i * row_h
    bg = RGBColor(0x0D, 0x12, 0x24) if i % 2 == 0 else RGBColor(0x10, 0x17, 0x2E)
    add_rect(sl, Inches(0.4), ry, Inches(3.5), row_h, fill_color=bg)
    add_rect(sl, Inches(3.95), ry, Inches(1.3), row_h, fill_color=bg)
    add_rect(sl, Inches(5.3), ry, Inches(7.6), row_h, fill_color=bg)
    add_text(sl, col_name, Inches(0.48), ry+Inches(0.04), Inches(3.3), row_h,
             font_size=Pt(9.5), color=WHITE, bold=True)
    clr = BLUE if col_type == "Angka" else GRAY
    add_text(sl, col_type, Inches(3.97), ry+Inches(0.04), Inches(1.25), row_h,
             font_size=Pt(9.5), color=clr)
    add_text(sl, keterangan, Inches(5.32), ry+Inches(0.04), Inches(7.45), row_h,
             font_size=Pt(9.5), color=GRAY)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 5 â€” OVERVIEW DASHBOARD
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, LIGHT_BLUE)
slide_number(sl, 5, TOTAL)

add_text(sl, "03  Overview Dashboard",
         Inches(0.5), Inches(0.2), Inches(12), Inches(0.65),
         font_size=Pt(26), bold=True, color=WHITE)
add_rect(sl, Inches(0.5), Inches(0.85), Inches(3.5), Inches(0.05), fill_color=LIGHT_BLUE)

# Kotak screenshot
add_rect(sl, Inches(0.4), Inches(1.05), Inches(12.5), Inches(5.0),
         fill_color=RGBColor(0x0D, 0x12, 0x24),
         line_color=LIGHT_BLUE, line_width=Pt(1.5))
add_text(sl, "[ Letakkan Screenshot Dashboard Utama di sini ]",
         Inches(0.4), Inches(3.0), Inches(12.5), Inches(1.0),
         font_size=Pt(16), color=GRAY, align=PP_ALIGN.CENTER, italic=True)
add_text(sl, "ðŸ“Œ  Buka http://localhost:8501 â†’ tekan F12 atau Snipping Tool untuk screenshot",
         Inches(0.4), Inches(3.8), Inches(12.5), Inches(0.5),
         font_size=Pt(12), color=RGBColor(0x4B, 0x55, 0x63), align=PP_ALIGN.CENTER, italic=True)

# Fitur-fitur
feats = [
    ("ðŸ“Š", "6 KPI Metrics",    "Total pasien, rata-rata umur, dokter, RS, billing, lama rawat"),
    ("ðŸ¥§", "5 Grafik Visual",  "Distribusi gender, golongan darah, penyakit, hasil tes, tipe rawat"),
    ("ðŸ¤–", "3 Fitur Data Mining", "Regresi, Klasifikasi, Clustering masing-masing di halaman tersendiri"),
    ("ðŸ“„", "Tabel Data Lengkap", "55.500 baris data pasien dapat dijelajahi secara interaktif"),
]
for i, (icon, title, desc) in enumerate(feats):
    lx = Inches(0.4) + i * Inches(3.23)
    add_rect(sl, lx, Inches(6.2), Inches(3.0), Inches(1.05),
             fill_color=RGBColor(0x0D, 0x12, 0x24),
             line_color=RGBColor(0x81, 0x8C, 0xF8), line_width=Pt(0.5))
    add_text(sl, f"{icon}  {title}", lx+Inches(0.1), Inches(6.28), Inches(2.8), Inches(0.38),
             font_size=Pt(11), bold=True, color=LIGHT_BLUE)
    add_text(sl, desc, lx+Inches(0.1), Inches(6.62), Inches(2.85), Inches(0.55),
             font_size=Pt(9.5), color=GRAY)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 6 â€” RANCANGAN 1 COVER
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
add_rect(sl, Inches(0), Inches(0), SLIDE_W, SLIDE_H, fill_color=RGBColor(0x0A, 0x10, 0x25))
add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(0.12), fill_color=BLUE)
slide_number(sl, 6, TOTAL)

add_text(sl, "RANCANGAN 1", Inches(1.5), Inches(1.8), Inches(10), Inches(0.65),
         font_size=Pt(16), bold=True, color=BLUE, align=PP_ALIGN.CENTER)
add_text(sl, "ðŸ“ˆ  Regresi", Inches(1.0), Inches(2.3), Inches(11), Inches(1.5),
         font_size=Pt(54), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(sl, "Prediksi Biaya Tagihan Pasien", Inches(1.0), Inches(3.75), Inches(11), Inches(0.65),
         font_size=Pt(22), color=BLUE, align=PP_ALIGN.CENTER)
add_rect(sl, Inches(4.0), Inches(4.5), Inches(5.3), Inches(0.06), fill_color=BLUE)
add_text(sl, "Algoritma: Linear Regression", Inches(1.0), Inches(4.7), Inches(11), Inches(0.5),
         font_size=Pt(16), color=GRAY, align=PP_ALIGN.CENTER)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 7 â€” REGRESI: ALGORITMA
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, BLUE)
slide_number(sl, 7, TOTAL)

add_text(sl, "04  Rancangan 1: Regresi",
         Inches(0.5), Inches(0.15), Inches(12), Inches(0.55),
         font_size=Pt(22), bold=True, color=WHITE)
add_text(sl, "ðŸ§®  Algoritma yang Diterapkan â€” Linear Regression",
         Inches(0.5), Inches(0.72), Inches(12.5), Inches(0.52),
         font_size=Pt(16), bold=True, color=BLUE)
add_rect(sl, Inches(0.5), Inches(1.22), Inches(3.5), Inches(0.05), fill_color=BLUE)

# Definisi
card(sl, Inches(0.4), Inches(1.35), Inches(12.5), Inches(2.2), BLUE)
add_text(sl, "Apa itu Linear Regression?",
         Inches(0.65), Inches(1.42), Inches(12.0), Inches(0.4),
         font_size=Pt(13), bold=True, color=BLUE)
defin = [
    "Linear Regression (Regresi Linier) adalah metode statistik untuk memprediksi nilai angka berdasarkan data-data yang sudah ada.",
    "",
    'Analogi: Seperti seorang agen properti berpengalaman yang bisa menaksir harga rumah hanya dengan melihat luas, lokasi, dan jumlah kamarnya â€” tanpa perlu survey mendetail.',
    "",
    "Dalam konteks ini: komputer belajar dari data 55.500 pasien, lalu memprediksi berapa tagihan pasien berikutnya berdasarkan profil mereka.",
]
add_multiline(sl, defin, Inches(0.65), Inches(1.82), Inches(12.0), Inches(1.65),
              font_size=Pt(12.5), color=GRAY)

# Formula
add_rect(sl, Inches(0.4), Inches(3.65), Inches(12.5), Inches(0.75),
         fill_color=RGBColor(0x0D, 0x18, 0x3A),
         line_color=BLUE, line_width=Pt(1))
add_text(sl, "Formula:   Prediksi Tagihan  =  Konstanta + (a Ã— Umur) + (b Ã— Jenis Penyakit) + (c Ã— Asuransi) + ...",
         Inches(0.6), Inches(3.73), Inches(12.1), Inches(0.55),
         font_size=Pt(13), color=BLUE, bold=True)

# 3 Keunggulan
keugs = [
    ("ðŸ“ Sederhana", "Mudah dipahami dan mudah dijelaskan hasilnya kepada non-teknisi"),
    ("âš¡ Cepat",     "Proses training sangat cepat meskipun data sangat besar"),
    ("ðŸ”® Praktis",  "Dapat langsung memberikan angka prediksi yang spesifik"),
]
for i, (judul, isi) in enumerate(keugs):
    lx = Inches(0.4) + i * Inches(4.23)
    add_rect(sl, lx, Inches(4.55), Inches(4.0), Inches(2.65),
             fill_color=RGBColor(0x0D, 0x12, 0x24),
             line_color=RGBColor(0x1E, 0x40, 0xAF), line_width=Pt(0.75))
    add_rect(sl, lx, Inches(4.55), Inches(4.0), Inches(0.08), fill_color=BLUE)
    add_text(sl, judul, lx+Inches(0.15), Inches(4.7), Inches(3.7), Inches(0.45),
             font_size=Pt(13), bold=True, color=BLUE)
    add_text(sl, isi, lx+Inches(0.15), Inches(5.15), Inches(3.75), Inches(1.8),
             font_size=Pt(12), color=GRAY)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 8 â€” REGRESI: DATA & CARA KERJA
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, BLUE)
slide_number(sl, 8, TOTAL)

add_text(sl, "04  Rancangan 1: Regresi",
         Inches(0.5), Inches(0.15), Inches(12), Inches(0.55),
         font_size=Pt(22), bold=True, color=WHITE)

# KOLOM KIRI â€” Data
card(sl, Inches(0.4), Inches(0.85), Inches(6.1), Inches(6.3), BLUE)
add_text(sl, "ðŸ“Š  Data / Kolom yang Digunakan",
         Inches(0.6), Inches(0.93), Inches(5.8), Inches(0.5),
         font_size=Pt(14), bold=True, color=BLUE)

add_text(sl, "Data Masukan (Bahan Prediksi):",
         Inches(0.65), Inches(1.45), Inches(5.7), Inches(0.38),
         font_size=Pt(12), bold=True, color=WHITE)

inputs = [
    ("Age",               "Umur pasien"),
    ("Gender",            "Jenis kelamin (Laki / Perempuan)"),
    ("Medical Condition", "Jenis penyakit yang diderita"),
    ("Admission Type",    "Tipe rawat inap (Darurat / Elektif / Mendesak)"),
    ("Insurance Provider","Nama perusahaan asuransi"),
    ("Room Number",       "Nomor kamar yang ditempati"),
]
for i, (col, desc) in enumerate(inputs):
    ty = Inches(1.85) + i * Inches(0.5)
    add_rect(sl, Inches(0.65), ty, Inches(5.6), Inches(0.43),
             fill_color=RGBColor(0x10, 0x1A, 0x3A),
             line_color=RGBColor(0x1E, 0x40, 0xAF), line_width=Pt(0.5))
    add_text(sl, f"  {col}", Inches(0.68), ty+Inches(0.05), Inches(2.1), Inches(0.38),
             font_size=Pt(11), bold=True, color=BLUE)
    add_text(sl, f"â†’  {desc}", Inches(2.85), ty+Inches(0.05), Inches(3.3), Inches(0.38),
             font_size=Pt(11), color=GRAY)

add_rect(sl, Inches(0.65), Inches(4.88), Inches(5.6), Inches(0.55),
         fill_color=RGBColor(0x0D, 0x1E, 0x40), line_color=BLUE, line_width=Pt(1.5))
add_text(sl, "  ðŸŽ¯  Output / Target  â†’  Billing Amount (Tagihan dalam $)",
         Inches(0.68), Inches(4.95), Inches(5.5), Inches(0.45),
         font_size=Pt(12), bold=True, color=WHITE)

# KOLOM KANAN â€” Cara Kerja
card(sl, Inches(6.75), Inches(0.85), Inches(6.2), Inches(6.3), BLUE)
add_text(sl, "âš™ï¸  Cara Kerja",
         Inches(6.95), Inches(0.93), Inches(5.9), Inches(0.5),
         font_size=Pt(14), bold=True, color=BLUE)

steps = [
    ("1", "Persiapan Data",   "Kolom berisi teks (Gender, Jenis Penyakit, dll) diubah menjadi angka agar bisa diproses komputer"),
    ("2", "Bagi Data",        "80% data dipakai untuk belajar (training), 20% untuk diuji (testing)"),
    ("3", "Proses Belajar",   "Model mencari pola: seberapa besar pengaruh tiap faktor terhadap besarnya tagihan"),
    ("4", "Prediksi",         "Model diuji pada 20% data yang belum pernah dilihat sebelumnya"),
    ("5", "Ukur Akurasi",     "Dihitung seberapa jauh selisih prediksi vs tagihan asli (MAE, RMSE, RÂ²)"),
]
for i, (num, title, desc) in enumerate(steps):
    ty = Inches(1.45) + i * Inches(1.05)
    add_rect(sl, Inches(6.95), ty, Inches(0.45), Inches(0.45),
             fill_color=BLUE)
    add_text(sl, num, Inches(6.95), ty+Inches(0.04), Inches(0.45), Inches(0.42),
             font_size=Pt(14), bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    add_text(sl, title, Inches(7.48), ty, Inches(5.2), Inches(0.4),
             font_size=Pt(12), bold=True, color=WHITE)
    add_text(sl, desc, Inches(7.48), ty+Inches(0.38), Inches(5.2), Inches(0.6),
             font_size=Pt(11), color=GRAY)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 9 â€” REGRESI: FUNGSI PENGAMBILAN KEPUTUSAN + SCREENSHOT
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, BLUE)
slide_number(sl, 9, TOTAL)

add_text(sl, "04  Rancangan 1: Regresi",
         Inches(0.5), Inches(0.15), Inches(12), Inches(0.55),
         font_size=Pt(22), bold=True, color=WHITE)
add_text(sl, "ðŸŽ¯  Fungsi dalam Mendukung Pengambilan Keputusan Rumah Sakit",
         Inches(0.5), Inches(0.72), Inches(12.5), Inches(0.52),
         font_size=Pt(15), bold=True, color=BLUE)

fungsi_reg = [
    ("ðŸ’°", "Kelola Keuangan Lebih Baik",
     "Pihak manajemen rumah sakit dapat memperkirakan berapa total pendapatan yang akan masuk dalam sebulan ke depan, sehingga pengelolaan anggaran menjadi lebih terencana dan akurat."),
    ("ðŸ·ï¸", "Tentukan Tarif yang Adil",
     "Manajemen bisa menentukan tarif layanan yang wajar berdasarkan data nyata dari ribuan pasien sebelumnya, bukan hanya berdasarkan perkiraan atau intuisi belaka."),
    ("ðŸ“‹", "Bantu Pasien Rencanakan Biaya",
     "Sebelum pasien masuk rawat inap, pihak RS bisa memberikan estimasi biaya sehingga pasien dan keluarga dapat mempersiapkan dana sejak awal dan tidak terkejut dengan tagihan."),
    ("ðŸ¤", "Percepat Proses Klaim Asuransi",
     "Data prediksi tagihan dapat dijadikan referensi awal saat mengajukan klaim kepada perusahaan asuransi, sehingga proses administrasi menjadi lebih cepat dan transparan."),
]

for i, (icon, judul, isi) in enumerate(fungsi_reg):
    col = i % 2
    row = i // 2
    lx = Inches(0.4) + col * Inches(6.4)
    ty = Inches(1.35) + row * Inches(2.0)
    add_rect(sl, lx, ty, Inches(6.1), Inches(1.85),
             fill_color=RGBColor(0x0D, 0x12, 0x24),
             line_color=RGBColor(0x1E, 0x40, 0xAF), line_width=Pt(0.75))
    add_rect(sl, lx, ty, Inches(0.07), Inches(1.85), fill_color=BLUE)
    add_text(sl, f"{icon}  {judul}", lx+Inches(0.2), ty+Inches(0.12),
             Inches(5.7), Inches(0.45), font_size=Pt(13), bold=True, color=BLUE)
    add_text(sl, isi, lx+Inches(0.2), ty+Inches(0.57),
             Inches(5.7), Inches(1.15), font_size=Pt(12), color=GRAY)

# Box screenshot
add_rect(sl, Inches(0.4), Inches(5.42), Inches(12.5), Inches(1.85),
         fill_color=RGBColor(0x0D, 0x12, 0x24), line_color=BLUE, line_width=Pt(1))
add_text(sl, "[ Screenshot Halaman Regresi â€” http://localhost:8501/1_Regresi ]",
         Inches(0.4), Inches(6.1), Inches(12.5), Inches(0.6),
         font_size=Pt(13), color=GRAY, align=PP_ALIGN.CENTER, italic=True)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 10 â€” RANCANGAN 2 COVER
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
add_rect(sl, Inches(0), Inches(0), SLIDE_W, SLIDE_H, fill_color=RGBColor(0x10, 0x08, 0x24))
add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(0.12), fill_color=PURPLE)
slide_number(sl, 10, TOTAL)

add_text(sl, "RANCANGAN 2", Inches(1.5), Inches(1.8), Inches(10), Inches(0.65),
         font_size=Pt(16), bold=True, color=PURPLE, align=PP_ALIGN.CENTER)
add_text(sl, "ðŸ”¬  Klasifikasi", Inches(1.0), Inches(2.3), Inches(11), Inches(1.5),
         font_size=Pt(54), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(sl, "Prediksi Hasil Tes Pasien", Inches(1.0), Inches(3.75), Inches(11), Inches(0.65),
         font_size=Pt(22), color=PURPLE, align=PP_ALIGN.CENTER)
add_rect(sl, Inches(4.0), Inches(4.5), Inches(5.3), Inches(0.06), fill_color=PURPLE)
add_text(sl, "Algoritma: Decision Tree (Pohon Keputusan)", Inches(1.0), Inches(4.7), Inches(11), Inches(0.5),
         font_size=Pt(16), color=GRAY, align=PP_ALIGN.CENTER)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 11 â€” KLASIFIKASI: ALGORITMA
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, PURPLE)
slide_number(sl, 11, TOTAL)

add_text(sl, "05  Rancangan 2: Klasifikasi",
         Inches(0.5), Inches(0.15), Inches(12), Inches(0.55),
         font_size=Pt(22), bold=True, color=WHITE)
add_text(sl, "ðŸŒ³  Algoritma yang Diterapkan â€” Decision Tree (Pohon Keputusan)",
         Inches(0.5), Inches(0.72), Inches(12.5), Inches(0.52),
         font_size=Pt(16), bold=True, color=PURPLE)
add_rect(sl, Inches(0.5), Inches(1.22), Inches(4.5), Inches(0.05), fill_color=PURPLE)

card(sl, Inches(0.4), Inches(1.35), Inches(12.5), Inches(2.3), PURPLE)
add_text(sl, "Apa itu Decision Tree (Pohon Keputusan)?",
         Inches(0.65), Inches(1.42), Inches(12.0), Inches(0.4),
         font_size=Pt(13), bold=True, color=PURPLE)
defin2 = [
    "Decision Tree adalah metode yang cara kerjanya mirip seperti alur tanya-jawab bercabang â€” persis seperti ketika dokter mendiagnosis penyakit dengan mengajukan pertanyaan satu per satu.",
    "",
    'Contoh: "Apakah pasien berumur di atas 60?" â†’ Ya â†’ "Apakah penyakitnya Kanker?" â†’ Ya â†’ "Hasil tes kemungkinan: Abnormal"',
    "",
    "Komputer membuat ribuan pertanyaan seperti itu secara otomatis dari data pasien yang sudah ada, lalu menyusunnya menjadi sebuah pohon keputusan yang bisa dipakai untuk memprediksi pasien baru.",
]
add_multiline(sl, defin2, Inches(0.65), Inches(1.82), Inches(12.0), Inches(1.75),
              font_size=Pt(12.5), color=GRAY)

# Ilustrasi pohon sederhana
add_rect(sl, Inches(0.4), Inches(3.78), Inches(12.5), Inches(3.45),
         fill_color=RGBColor(0x0D, 0x12, 0x24),
         line_color=RGBColor(0x5B, 0x21, 0xB6), line_width=Pt(0.75))
add_text(sl, "Ilustrasi Alur Pohon Keputusan:",
         Inches(0.6), Inches(3.85), Inches(12.0), Inches(0.38),
         font_size=Pt(12), bold=True, color=PURPLE)

tree_items = [
    (Inches(5.5),  Inches(4.3),  "Umur > 60?",        PURPLE),
    (Inches(2.0),  Inches(5.15), "Penyakit Kanker?",   BLUE),
    (Inches(9.0),  Inches(5.15), "Penyakit Diabetes?", BLUE),
    (Inches(0.7),  Inches(6.1),  "âœ… NORMAL",           GREEN),
    (Inches(3.3),  Inches(6.1),  "ðŸš¨ ABNORMAL",         RGBColor(0xF8, 0x71, 0x71)),
    (Inches(7.7),  Inches(6.1),  "âš ï¸ TIDAK MEYAKINKAN", ORANGE),
    (Inches(10.2), Inches(6.1),  "âœ… NORMAL",            GREEN),
]
for lx, ty, label, color in tree_items:
    add_rect(sl, lx, ty, Inches(2.2), Inches(0.5),
             fill_color=RGBColor(0x10, 0x17, 0x2E), line_color=color, line_width=Pt(1))
    add_text(sl, label, lx, ty+Inches(0.08), Inches(2.2), Inches(0.38),
             font_size=Pt(11), bold=True, color=color, align=PP_ALIGN.CENTER)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 12 â€” KLASIFIKASI: DATA & CARA KERJA
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, PURPLE)
slide_number(sl, 12, TOTAL)

add_text(sl, "05  Rancangan 2: Klasifikasi",
         Inches(0.5), Inches(0.15), Inches(12), Inches(0.55),
         font_size=Pt(22), bold=True, color=WHITE)

# Kolom kiri
card(sl, Inches(0.4), Inches(0.85), Inches(6.1), Inches(6.3), PURPLE)
add_text(sl, "ðŸ“Š  Data / Kolom yang Digunakan",
         Inches(0.6), Inches(0.93), Inches(5.8), Inches(0.5),
         font_size=Pt(14), bold=True, color=PURPLE)
add_text(sl, "Data Masukan (Bahan Prediksi):",
         Inches(0.65), Inches(1.45), Inches(5.7), Inches(0.38),
         font_size=Pt(12), bold=True, color=WHITE)

inputs2 = [
    ("Age",              "Umur pasien"),
    ("Gender",           "Jenis kelamin"),
    ("Blood Type",       "Golongan darah"),
    ("Medical Condition","Jenis penyakit yang diderita"),
    ("Admission Type",   "Tipe rawat inap"),
    ("Medication",       "Obat yang diberikan kepada pasien"),
    ("Billing Amount",   "Total tagihan biaya perawatan"),
]
for i, (col, desc) in enumerate(inputs2):
    ty = Inches(1.85) + i * Inches(0.47)
    add_rect(sl, Inches(0.65), ty, Inches(5.6), Inches(0.4),
             fill_color=RGBColor(0x12, 0x0A, 0x28),
             line_color=RGBColor(0x5B, 0x21, 0xB6), line_width=Pt(0.5))
    add_text(sl, f"  {col}", Inches(0.68), ty+Inches(0.04), Inches(2.1), Inches(0.36),
             font_size=Pt(11), bold=True, color=PURPLE)
    add_text(sl, f"â†’  {desc}", Inches(2.85), ty+Inches(0.04), Inches(3.3), Inches(0.36),
             font_size=Pt(11), color=GRAY)

add_rect(sl, Inches(0.65), Inches(5.16), Inches(5.6), Inches(0.6),
         fill_color=RGBColor(0x12, 0x08, 0x2E), line_color=PURPLE, line_width=Pt(1.5))
add_text(sl, "  ðŸŽ¯  Output / Target  â†’  Test Results\n        (Normal / Abnormal / Tidak Meyakinkan)",
         Inches(0.68), Inches(5.22), Inches(5.5), Inches(0.52),
         font_size=Pt(11), bold=True, color=WHITE)

# Kolom kanan
card(sl, Inches(6.75), Inches(0.85), Inches(6.2), Inches(6.3), PURPLE)
add_text(sl, "âš™ï¸  Cara Kerja",
         Inches(6.95), Inches(0.93), Inches(5.9), Inches(0.5),
         font_size=Pt(14), bold=True, color=PURPLE)

steps2 = [
    ("1", "Persiapan Data",     "Teks seperti nama obat dan jenis penyakit diubah menjadi angka agar bisa diproses"),
    ("2", "Bagi Data",          "80% untuk belajar, 20% untuk diuji â€” pembagian dilakukan secara merata untuk tiap kelas hasil tes"),
    ("3", "Proses Belajar",     "Komputer membuat pohon keputusan â€” mencari pertanyaan terbaik yang bisa memisahkan Normal, Abnormal, dan Tidak Meyakinkan"),
    ("4", "Prediksi",           "Pasien baru 'ditelusuri' melalui pohon keputusan dari atas hingga mendapat jawaban akhir"),
    ("5", "Ukur Akurasi",       "Dihitung seberapa sering prediksi benar (Akurasi, Confusion Matrix, F1-Score)"),
]
for i, (num, title, desc) in enumerate(steps2):
    ty = Inches(1.45) + i * Inches(1.05)
    add_rect(sl, Inches(6.95), ty, Inches(0.45), Inches(0.45), fill_color=PURPLE)
    add_text(sl, num, Inches(6.95), ty+Inches(0.04), Inches(0.45), Inches(0.42),
             font_size=Pt(14), bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    add_text(sl, title, Inches(7.48), ty, Inches(5.2), Inches(0.4),
             font_size=Pt(12), bold=True, color=WHITE)
    add_text(sl, desc, Inches(7.48), ty+Inches(0.38), Inches(5.2), Inches(0.62),
             font_size=Pt(11), color=GRAY)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 13 â€” KLASIFIKASI: FUNGSI KEPUTUSAN + SCREENSHOT
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, PURPLE)
slide_number(sl, 13, TOTAL)

add_text(sl, "05  Rancangan 2: Klasifikasi",
         Inches(0.5), Inches(0.15), Inches(12), Inches(0.55),
         font_size=Pt(22), bold=True, color=WHITE)
add_text(sl, "ðŸŽ¯  Fungsi dalam Mendukung Pengambilan Keputusan Rumah Sakit",
         Inches(0.5), Inches(0.72), Inches(12.5), Inches(0.52),
         font_size=Pt(15), bold=True, color=PURPLE)

fungsi_cls = [
    ("ðŸš‘", "Utamakan Pasien yang Paling Butuh",
     "Pasien yang diprediksi hasilnya Abnormal bisa langsung ditangani lebih cepat tanpa perlu menunggu hasil lab keluar. Ini bisa menyelamatkan nyawa di situasi darurat."),
    ("ðŸ‘¨â€âš•ï¸", "Atur Jumlah Tenaga Medis",
     "Jika prediksi menunjukkan banyak pasien dengan hasil Abnormal minggu ini, manajemen bisa langsung menyiapkan dokter spesialis yang cukup sejak awal."),
    ("âš ï¸", "Sistem Peringatan Dini",
     "Pasien yang berisiko tinggi bisa segera dirujuk ke unit perawatan intensif (ICU) sebelum kondisinya memburuk, sehingga penanganan lebih proaktif."),
    ("â±ï¸", "Kurangi Waktu Tunggu Pasien",
     "Dengan mengetahui prioritas setiap pasien berbasis data, antrian penanganan bisa diatur jauh lebih efisien dan tidak membuang waktu pasien yang kritis."),
]
for i, (icon, judul, isi) in enumerate(fungsi_cls):
    col = i % 2
    row = i // 2
    lx = Inches(0.4) + col * Inches(6.4)
    ty = Inches(1.35) + row * Inches(2.0)
    add_rect(sl, lx, ty, Inches(6.1), Inches(1.85),
             fill_color=RGBColor(0x0D, 0x12, 0x24),
             line_color=RGBColor(0x5B, 0x21, 0xB6), line_width=Pt(0.75))
    add_rect(sl, lx, ty, Inches(0.07), Inches(1.85), fill_color=PURPLE)
    add_text(sl, f"{icon}  {judul}", lx+Inches(0.2), ty+Inches(0.12),
             Inches(5.7), Inches(0.45), font_size=Pt(13), bold=True, color=PURPLE)
    add_text(sl, isi, lx+Inches(0.2), ty+Inches(0.57),
             Inches(5.7), Inches(1.15), font_size=Pt(12), color=GRAY)

add_rect(sl, Inches(0.4), Inches(5.42), Inches(12.5), Inches(1.85),
         fill_color=RGBColor(0x0D, 0x12, 0x24), line_color=PURPLE, line_width=Pt(1))
add_text(sl, "[ Screenshot Halaman Klasifikasi â€” http://localhost:8501/2_Klasifikasi ]",
         Inches(0.4), Inches(6.1), Inches(12.5), Inches(0.6),
         font_size=Pt(13), color=GRAY, align=PP_ALIGN.CENTER, italic=True)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 14 â€” RANCANGAN 3 COVER
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
add_rect(sl, Inches(0), Inches(0), SLIDE_W, SLIDE_H, fill_color=RGBColor(0x04, 0x14, 0x0E))
add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(0.12), fill_color=GREEN)
slide_number(sl, 14, TOTAL)

add_text(sl, "RANCANGAN 3", Inches(1.5), Inches(1.8), Inches(10), Inches(0.65),
         font_size=Pt(16), bold=True, color=GREEN, align=PP_ALIGN.CENTER)
add_text(sl, "ðŸ”µ  Clustering", Inches(1.0), Inches(2.3), Inches(11), Inches(1.5),
         font_size=Pt(54), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(sl, "Segmentasi & Pengelompokan Pasien", Inches(1.0), Inches(3.75), Inches(11), Inches(0.65),
         font_size=Pt(22), color=GREEN, align=PP_ALIGN.CENTER)
add_rect(sl, Inches(4.0), Inches(4.5), Inches(5.3), Inches(0.06), fill_color=GREEN)
add_text(sl, "Algoritma: K-Means Clustering", Inches(1.0), Inches(4.7), Inches(11), Inches(0.5),
         font_size=Pt(16), color=GRAY, align=PP_ALIGN.CENTER)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 15 â€” CLUSTERING: ALGORITMA
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, GREEN)
slide_number(sl, 15, TOTAL)

add_text(sl, "06  Rancangan 3: Clustering",
         Inches(0.5), Inches(0.15), Inches(12), Inches(0.55),
         font_size=Pt(22), bold=True, color=WHITE)
add_text(sl, "ðŸ”µ  Algoritma yang Diterapkan â€” K-Means Clustering",
         Inches(0.5), Inches(0.72), Inches(12.5), Inches(0.52),
         font_size=Pt(16), bold=True, color=GREEN)
add_rect(sl, Inches(0.5), Inches(1.22), Inches(4.0), Inches(0.05), fill_color=GREEN)

card(sl, Inches(0.4), Inches(1.35), Inches(12.5), Inches(2.3), GREEN)
add_text(sl, "Apa itu K-Means Clustering?",
         Inches(0.65), Inches(1.42), Inches(12.0), Inches(0.4),
         font_size=Pt(13), bold=True, color=GREEN)
defin3 = [
    "K-Means Clustering adalah metode yang digunakan untuk mengelompokkan data secara otomatis tanpa perlu memberi label terlebih dahulu. Ini yang membedakannya dari Regresi dan Klasifikasi.",
    "",
    'Analogi: Seperti ketika kita memilah-milah ratusan foto ke dalam beberapa album â€” tanpa tahu ada berapa kategori. Komputer sendiri yang menentukan kelompok mana yang paling masuk akal.',
    "",
    "Dalam konteks ini: dari 55.500 data pasien, komputer secara otomatis membagi mereka ke dalam beberapa kelompok berdasarkan kemiripan profil (umur, tagihan, lama rawat).",
]
add_multiline(sl, defin3, Inches(0.65), Inches(1.82), Inches(12.0), Inches(1.75),
              font_size=Pt(12.5), color=GRAY)

# Perbedaan dengan supervised
add_rect(sl, Inches(0.4), Inches(3.75), Inches(12.5), Inches(0.65),
         fill_color=RGBColor(0x04, 0x1A, 0x0E), line_color=GREEN, line_width=Pt(1))
add_text(sl, "ðŸ“Œ  Perbedaan Utama: Regresi & Klasifikasi = belajar dari data berlabel (tahu jawabannya) | Clustering = tidak ada jawaban sebelumnya, komputer yang menemukan sendiri",
         Inches(0.6), Inches(3.82), Inches(12.1), Inches(0.55),
         font_size=Pt(12), color=GREEN, bold=True)

proses = [
    ("1ï¸âƒ£", "Tentukan K", "Coba beberapa jumlah kelompok (2 s.d. 10) â†’ pilih yang terbaik pakai Elbow Method"),
    ("2ï¸âƒ£", "Pilih Pusat", "Komputer memilih K titik pusat (centroid) secara acak sebagai pusat kelompok awal"),
    ("3ï¸âƒ£", "Kelompokkan", "Setiap pasien dimasukkan ke kelompok dengan pusat yang paling mirip profilnya"),
    ("4ï¸âƒ£", "Perbarui Pusat","Pusat kelompok dihitung ulang sebagai rata-rata seluruh anggotanya"),
    ("5ï¸âƒ£", "Ulangi & Selesai","Langkah 3-4 diulang hingga kelompok tidak berubah lagi (konvergen)"),
]
for i, (icon, title, desc) in enumerate(proses):
    lx = Inches(0.4) + i * Inches(2.57)
    add_rect(sl, lx, Inches(4.55), Inches(2.45), Inches(2.65),
             fill_color=RGBColor(0x04, 0x12, 0x0A),
             line_color=RGBColor(0x06, 0x60, 0x30), line_width=Pt(0.75))
    add_rect(sl, lx, Inches(4.55), Inches(2.45), Inches(0.08), fill_color=GREEN)
    add_text(sl, icon, lx+Inches(0.08), Inches(4.68), Inches(2.3), Inches(0.38),
             font_size=Pt(14), bold=True, color=GREEN)
    add_text(sl, title, lx+Inches(0.08), Inches(5.05), Inches(2.3), Inches(0.38),
             font_size=Pt(12), bold=True, color=WHITE)
    add_text(sl, desc, lx+Inches(0.08), Inches(5.43), Inches(2.32), Inches(1.65),
             font_size=Pt(11), color=GRAY)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 16 â€” CLUSTERING: DATA & CARA KERJA
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, GREEN)
slide_number(sl, 16, TOTAL)

add_text(sl, "06  Rancangan 3: Clustering",
         Inches(0.5), Inches(0.15), Inches(12), Inches(0.55),
         font_size=Pt(22), bold=True, color=WHITE)

card(sl, Inches(0.4), Inches(0.85), Inches(6.1), Inches(6.3), GREEN)
add_text(sl, "ðŸ“Š  Data / Kolom yang Digunakan",
         Inches(0.6), Inches(0.93), Inches(5.8), Inches(0.5),
         font_size=Pt(14), bold=True, color=GREEN)
add_text(sl, "Data yang Dipakai untuk Mengelompokkan Pasien:",
         Inches(0.65), Inches(1.45), Inches(5.7), Inches(0.38),
         font_size=Pt(12), bold=True, color=WHITE)
inputs3 = [
    ("Age",            "Umur pasien (tahun)"),
    ("Billing Amount", "Total tagihan biaya perawatan ($)"),
    ("Room Number",    "Nomor kamar yang ditempati"),
    ("Length of Stay", "Lama rawat inap dalam hari\n(dihitung dari tanggal masuk hingga keluar)"),
]
for i, (col, desc) in enumerate(inputs3):
    ty = Inches(1.88) + i * Inches(0.72)
    add_rect(sl, Inches(0.65), ty, Inches(5.6), Inches(0.65),
             fill_color=RGBColor(0x04, 0x14, 0x0A),
             line_color=RGBColor(0x06, 0x60, 0x30), line_width=Pt(0.5))
    add_text(sl, f"  {col}", Inches(0.68), ty+Inches(0.07), Inches(2.0), Inches(0.55),
             font_size=Pt(12), bold=True, color=GREEN)
    add_text(sl, f"â†’  {desc}", Inches(2.75), ty+Inches(0.07), Inches(3.4), Inches(0.55),
             font_size=Pt(11), color=GRAY)

add_rect(sl, Inches(0.65), Inches(4.8), Inches(5.6), Inches(1.0),
         fill_color=RGBColor(0x04, 0x1A, 0x0E), line_color=GREEN, line_width=Pt(1.5))
add_text(sl, "  ðŸŽ¯  Output: Label Kelompok\n  (Cluster 0, Cluster 1, Cluster 2, ...)",
         Inches(0.68), Inches(4.9), Inches(5.5), Inches(0.8),
         font_size=Pt(12), bold=True, color=WHITE)
add_text(sl, "  âš™ï¸  Pra-pemrosesan: Semua data disamakan skalanya\n  agar tidak ada kolom yang mendominasi pengelompokan",
         Inches(0.68), Inches(5.72), Inches(5.5), Inches(0.8),
         font_size=Pt(11), color=GRAY)

card(sl, Inches(6.75), Inches(0.85), Inches(6.2), Inches(6.3), GREEN)
add_text(sl, "âš™ï¸  Cara Kerja",
         Inches(6.95), Inches(0.93), Inches(5.9), Inches(0.5),
         font_size=Pt(14), bold=True, color=GREEN)

steps3 = [
    ("1", "Hitung Lama Rawat",       "Dari tanggal masuk dan keluar, kita hitung berapa hari setiap pasien dirawat"),
    ("2", "Samakan Skala Data",      "Karena umur, tagihan, dan hari rawat punya satuan berbeda, semua diseragamkan"),
    ("3", "Cari Jumlah Kelompok",    "Dicoba 2 s.d. 10 kelompok â†’ dipilih yang paling baik pemisahannya (Elbow Method)"),
    ("4", "Kelompokkan Pasien",      "Tiap pasien dimasukkan ke kelompok yang paling mirip profilnya secara otomatis"),
    ("5", "Analisis Tiap Kelompok",  "Ciri-ciri tiap kelompok dianalisis (misalnya: pasien muda tagihan rendah, pasien lansia tagihan tinggi)"),
    ("6", "Tampilkan Visual",        "Kelompok divisualisasikan dalam grafik 2D (PCA) agar mudah dipahami semua pihak"),
]
for i, (num, title, desc) in enumerate(steps3):
    ty = Inches(1.45) + i * Inches(0.87)
    add_rect(sl, Inches(6.95), ty, Inches(0.45), Inches(0.45), fill_color=GREEN)
    add_text(sl, num, Inches(6.95), ty+Inches(0.04), Inches(0.45), Inches(0.42),
             font_size=Pt(14), bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
    add_text(sl, title, Inches(7.48), ty, Inches(5.2), Inches(0.38),
             font_size=Pt(12), bold=True, color=WHITE)
    add_text(sl, desc, Inches(7.48), ty+Inches(0.37), Inches(5.2), Inches(0.5),
             font_size=Pt(11), color=GRAY)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 17 â€” CLUSTERING: FUNGSI KEPUTUSAN + SCREENSHOT
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, GREEN)
slide_number(sl, 17, TOTAL)

add_text(sl, "06  Rancangan 3: Clustering",
         Inches(0.5), Inches(0.15), Inches(12), Inches(0.55),
         font_size=Pt(22), bold=True, color=WHITE)
add_text(sl, "ðŸŽ¯  Fungsi dalam Mendukung Pengambilan Keputusan Rumah Sakit",
         Inches(0.5), Inches(0.72), Inches(12.5), Inches(0.52),
         font_size=Pt(15), bold=True, color=GREEN)

fungsi_clust = [
    ("ðŸŽ¯", "Layanan yang Lebih Personal",
     "Setiap kelompok pasien mendapatkan pelayanan yang sesuai dengan kebutuhan dan kondisi mereka â€” bukan satu layanan yang sama untuk semua pasien."),
    ("ðŸŽª", "Program Kesehatan Tepat Sasaran",
     "Kelompok pasien lansia bisa ditawarkan paket perawatan khusus, sedangkan kelompok pasien muda bisa mendapat program pencegahan penyakit yang berbeda."),
    ("ðŸ¥", "Atur Kapasitas & Sumber Daya",
     "Jika satu kelompok pasien biasanya membutuhkan rawat inap yang lama, rumah sakit bisa menyiapkan lebih banyak kamar dan tenaga medis untuk mereka."),
    ("ðŸ”", "Temukan Pasien yang Tidak Biasa",
     "Pasien yang profilnya sangat berbeda dari kelompok manapun dapat langsung mendapat perhatian dan pemeriksaan khusus dari tenaga medis."),
]
for i, (icon, judul, isi) in enumerate(fungsi_clust):
    col = i % 2
    row = i // 2
    lx = Inches(0.4) + col * Inches(6.4)
    ty = Inches(1.35) + row * Inches(2.0)
    add_rect(sl, lx, ty, Inches(6.1), Inches(1.85),
             fill_color=RGBColor(0x0D, 0x12, 0x24),
             line_color=RGBColor(0x06, 0x60, 0x30), line_width=Pt(0.75))
    add_rect(sl, lx, ty, Inches(0.07), Inches(1.85), fill_color=GREEN)
    add_text(sl, f"{icon}  {judul}", lx+Inches(0.2), ty+Inches(0.12),
             Inches(5.7), Inches(0.45), font_size=Pt(13), bold=True, color=GREEN)
    add_text(sl, isi, lx+Inches(0.2), ty+Inches(0.57),
             Inches(5.7), Inches(1.15), font_size=Pt(12), color=GRAY)

add_rect(sl, Inches(0.4), Inches(5.42), Inches(12.5), Inches(1.85),
         fill_color=RGBColor(0x0D, 0x12, 0x24), line_color=GREEN, line_width=Pt(1))
add_text(sl, "[ Screenshot Halaman Clustering â€” http://localhost:8501/3_Clustering ]",
         Inches(0.4), Inches(6.1), Inches(12.5), Inches(0.6),
         font_size=Pt(13), color=GRAY, align=PP_ALIGN.CENTER, italic=True)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 18 â€” PERBANDINGAN 3 RANCANGAN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, LIGHT_BLUE)
slide_number(sl, 18, TOTAL)

add_text(sl, "Perbandingan 3 Rancangan Data Mining",
         Inches(0.5), Inches(0.2), Inches(12.5), Inches(0.65),
         font_size=Pt(26), bold=True, color=WHITE)
add_rect(sl, Inches(0.5), Inches(0.85), Inches(6.0), Inches(0.05), fill_color=LIGHT_BLUE)

headers = ["Aspek", "Regresi", "Klasifikasi", "Clustering"]
col_ws  = [Inches(2.3), Inches(3.4), Inches(3.4), Inches(3.4)]
hdr_colors = [LIGHT_BLUE, BLUE, PURPLE, GREEN]
col_x = [Inches(0.4), Inches(2.75), Inches(6.2), Inches(9.65)]

hy = Inches(1.0)
for i, (hdr, color, lx, cw) in enumerate(zip(headers, hdr_colors, col_x, col_ws)):
    add_rect(sl, lx, hy, cw, Inches(0.48), fill_color=color)
    add_text(sl, hdr, lx, hy+Inches(0.06), cw, Inches(0.38),
             font_size=Pt(13), bold=True, color=BG_DARK if i > 0 else BG_DARK,
             align=PP_ALIGN.CENTER)

rows = [
    ("Jenis Masalah",   "Prediksi nilai angka\n(Berapa besar?)",     "Prediksi kategori/kelas\n(Termasuk yang mana?)",    "Pengelompokan otomatis\n(Mirip dengan siapa?)"),
    ("Label Data",      "Butuh data berlabel\n(supervised)",          "Butuh data berlabel\n(supervised)",                 "Tidak butuh label\n(unsupervised)"),
    ("Input",           "6 kolom profil pasien",                      "7 kolom profil pasien",                             "4 kolom numerik pasien"),
    ("Output",          "Angka â€” Billing Amount ($)",                  "Kelas â€” Normal/Abnormal/\nTidak Meyakinkan",        "Label kelompok â€” Cluster 0, 1, 2..."),
    ("Metrik Evaluasi", "RÂ² Score, MAE, RMSE",                        "Akurasi, F1-Score,\nConfusion Matrix",              "Silhouette Score,\nElbow Method"),
    ("Manfaat Utama",   "Estimasi biaya perawatan\nsebelum dirawat",  "Prioritas penanganan\npasien darurat",              "Personalisasi layanan\nper segmen pasien"),
]

for r, (aspek, reg, cls, clust) in enumerate(rows):
    ry = Inches(1.5) + r * Inches(0.95)
    row_bg = RGBColor(0x0D, 0x12, 0x24) if r % 2 == 0 else RGBColor(0x10, 0x17, 0x2E)
    for lx, cw in zip(col_x, col_ws):
        add_rect(sl, lx, ry, cw, Inches(0.9), fill_color=row_bg,
                 line_color=RGBColor(0x1E, 0x28, 0x40), line_width=Pt(0.5))
    vals = [aspek, reg, cls, clust]
    txt_colors = [WHITE, BLUE, PURPLE, GREEN]
    for lx, cw, val, color in zip(col_x, col_ws, vals, txt_colors):
        add_text(sl, val, lx+Inches(0.08), ry+Inches(0.07), cw-Inches(0.12), Inches(0.8),
                 font_size=Pt(11), color=color,
                 bold=(color == WHITE), align=PP_ALIGN.LEFT if color == WHITE else PP_ALIGN.CENTER)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 19 â€” KESIMPULAN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
top_accent_bar(sl, ORANGE)
slide_number(sl, 19, TOTAL)

add_text(sl, "07  Kesimpulan & Manfaat",
         Inches(0.5), Inches(0.2), Inches(12), Inches(0.65),
         font_size=Pt(26), bold=True, color=WHITE)
add_rect(sl, Inches(0.5), Inches(0.85), Inches(3.5), Inches(0.05), fill_color=ORANGE)

add_text(sl, "Dengan menerapkan Data Mining pada data kesehatan rumah sakit, organisasi mendapatkan kemampuan:",
         Inches(0.5), Inches(1.05), Inches(12.3), Inches(0.5),
         font_size=Pt(14), color=GRAY)

kesimpulan = [
    (BLUE,   "ðŸ“ˆ Regresi â€” Linear Regression",
             "Dari yang sebelumnya hanya bisa menentukan tarif berdasarkan perkiraan, kini manajemen rumah sakit dapat memprediksi estimasi biaya perawatan setiap pasien secara otomatis sebelum mereka masuk. Ini membantu pengelolaan keuangan yang lebih terencana, transparan, dan akuntabel."),
    (PURPLE, "ðŸ”¬ Klasifikasi â€” Decision Tree",
             "Dokter dan perawat kini memiliki alat bantu berbasis data untuk mengidentifikasi pasien berisiko tinggi lebih cepat. Dengan prediksi hasil tes sejak awal, penanganan darurat bisa dilakukan lebih proaktif, alokasi tenaga medis lebih efisien, dan waktu tunggu pasien berkurang signifikan."),
    (GREEN,  "ðŸ”µ Clustering â€” K-Means",
             "Manajemen kini bisa melihat 'wajah' populasi pasien mereka melalui segmentasi otomatis. Setiap kelompok pasien mendapatkan layanan yang disesuaikan dengan profil mereka â€” bukan layanan yang seragam untuk semua â€” sehingga kualitas layanan meningkat dan kepuasan pasien lebih terjaga."),
]
for i, (color, judul, isi) in enumerate(kesimpulan):
    ty = Inches(1.65) + i * Inches(1.82)
    add_rect(sl, Inches(0.4), ty, Inches(12.5), Inches(1.7),
             fill_color=RGBColor(0x0D, 0x12, 0x24),
             line_color=RGBColor(color[0]//3, color[1]//3, color[2]//3),
             line_width=Pt(0.75))
    add_rect(sl, Inches(0.4), ty, Inches(0.08), Inches(1.7), fill_color=color)
    add_text(sl, judul, Inches(0.65), ty+Inches(0.12), Inches(12.0), Inches(0.45),
             font_size=Pt(13), bold=True, color=color)
    add_text(sl, isi, Inches(0.65), ty+Inches(0.58), Inches(12.0), Inches(1.0),
             font_size=Pt(12), color=GRAY)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SLIDE 20 â€” PENUTUP
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
sl = add_slide()
add_rect(sl, Inches(0), Inches(0), SLIDE_W, SLIDE_H, fill_color=RGBColor(0x0A, 0x0E, 0x1A))
add_rect(sl, Inches(0), Inches(0), SLIDE_W, Inches(0.12), fill_color=LIGHT_BLUE)
slide_number(sl, 20, TOTAL)

add_text(sl, "ðŸ¥", Inches(5.8), Inches(1.5), Inches(1.5), Inches(1.5),
         font_size=Pt(60), align=PP_ALIGN.CENTER)
add_text(sl, "Terima Kasih", Inches(1.0), Inches(2.8), Inches(11), Inches(1.0),
         font_size=Pt(46), bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(sl, "Healthcare Analytics Dashboard  |  Data Mining Implementation",
         Inches(1.0), Inches(3.75), Inches(11), Inches(0.5),
         font_size=Pt(16), color=LIGHT_BLUE, align=PP_ALIGN.CENTER)
add_rect(sl, Inches(3.5), Inches(4.35), Inches(6.3), Inches(0.05), fill_color=LIGHT_BLUE)
add_text(sl, "Regresi  â€¢  Klasifikasi  â€¢  Clustering",
         Inches(1.0), Inches(4.5), Inches(11), Inches(0.45),
         font_size=Pt(15), color=PURPLE, bold=True, align=PP_ALIGN.CENTER)

# 3 badge bawah
badges = [("ðŸ“ˆ Regresi", BLUE), ("ðŸ”¬ Klasifikasi", PURPLE), ("ðŸ”µ Clustering", GREEN)]
for i, (label, color) in enumerate(badges):
    lx = Inches(2.2) + i * Inches(3.1)
    add_rect(sl, lx, Inches(5.3), Inches(2.8), Inches(0.65),
             fill_color=RGBColor(color[0]//6, color[1]//6, color[2]//6),
             line_color=color, line_width=Pt(1))
    add_text(sl, label, lx, Inches(5.38), Inches(2.8), Inches(0.5),
             font_size=Pt(14), bold=True, color=color, align=PP_ALIGN.CENTER)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SIMPAN FILE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
output_path = "Healthcare_DataMining_Presentation.pptx"
prs.save(output_path)
print(f"\nâœ… PPT berhasil dibuat: {output_path}")
print(f"   Total slide: {TOTAL}")
print(f"\nðŸ“Œ Langkah selanjutnya:")
print(f"   1. Buka file PPT â†’ ganti teks [Screenshot...] dengan screenshot asli dashboard")
print(f"   2. Screenshot dashboard: buka http://localhost:8501 â†’ Snipping Tool (Win+Shift+S)")
print(f"   3. File tersimpan di: C:\\Users\\ACER\\Downloads\\healthcare-dashboard\\{output_path}")

