import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import xlsxwriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


# Veritabanına bağlanma
def connect_db():
    try:
        conn = pymysql.connect(
            host='localhost',
            port= 3306,
            user='root',
            password='150704',
            database='sbs_auto',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        messagebox.showerror("Veritabanı Hatası", str(e))
        return None

# PDF çıktısı
pdfmetrics.registerFont(TTFont('TurkceFont', r"C:\Users\LENOVO\OneDrive - kapadokya.edu.tr\Masaüstü\DejaVuSans.ttf"))
def pdf_dosya_olustur():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM servis_kayit ORDER BY id DESC")
            rows = cursor.fetchall()
            if not rows:
                messagebox.showinfo("Bilgi", "PDF için kayıt bulunamadı.")
                return

            pdf_name = "servis_kayitlari.pdf"
            c = canvas.Canvas(pdf_name, pagesize=letter)
            c.setFont("TurkceFont", 10)

            y = 750

            def sayfa_basligi():
                nonlocal y
                c.setFont("TurkceFont", 10)
                c.drawString(30, y, "PLAKA | TARİH | MÜSTERİ | TELEFON | ISLEM | ÜCRET")
                y -= 20
                c.drawString(30, y, "-" * 100)
                y -= 20

            sayfa_basligi()

            for row in rows:
                tarih = str(row['tarih']) if row['tarih'] else ''
                text = f"{row['plaka']} | {tarih} | {row['musteri_ad']} | {row['telefon']} | {row['islem']} | {row['ucret']} ₺"
                c.drawString(30, y, text)
                y -= 15
                if y < 50:
                    c.showPage()
                    y = 750
                    sayfa_basligi()

            c.save()
            messagebox.showinfo("Başarılı", f"PDF başarıyla oluşturuldu: {pdf_name}")
            os.startfile(pdf_name)  # PDF dosyasını otomatik aç
        except Exception as e:
            messagebox.showerror("PDF Hatası", str(e))
        finally:
            conn.close()

# Excel çıktısı
def excel_dosya_olustur():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM servis_kayit ORDER BY id DESC")
            rows = cursor.fetchall()

            if not rows:
                messagebox.showinfo("Bilgi", "Excel için kayıt bulunamadı.")
                return

            excel_name = "servis_kayitlari.xlsx"
            workbook = xlsxwriter.Workbook(excel_name)
            sheet = workbook.add_worksheet("Kayıtlar")

            headers = ["Plaka", "Tarih", "Müşteri Adı", "Telefon", "İşlem", "Ücret"]
            for col_num, header in enumerate(headers):
                sheet.write(0, col_num, header)

            for row_num, row in enumerate(rows, start=1):
                sheet.write(row_num, 0, row['plaka'])
                sheet.write(row_num, 1, str(row['tarih']))
                sheet.write(row_num, 2, row['musteri_ad'])
                sheet.write(row_num, 3, row['telefon'])
                sheet.write(row_num, 4, row['islem'])
                sheet.write(row_num, 5, float(row['ucret']))

            workbook.close()
            messagebox.showinfo("Başarılı", f"Excel başarıyla oluşturuldu: {excel_name}")
            os.startfile(excel_name)
        except Exception as e:
            messagebox.showerror("Excel Hatası", str(e))
        finally:
            conn.close()

# Verileri tabloya yükle
def verileri_yukle():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM servis_kayit ORDER BY id DESC")
            rows = cursor.fetchall()
            tablo_temizle()
            for row in rows:
                table.insert("", "end", values=(row['id'], row['plaka'], row['tarih'], row['musteri_ad'], row['telefon'], row['islem'], row['ucret']))
        except Exception as e:
            messagebox.showerror("Veri Hatası", str(e))
        finally:
            conn.close()

# Tablodaki verileri temizle
def tablo_temizle():
    for row in table.get_children():
        table.delete(row)

# Kayıt ekleme
def kayit_ekle():
    veriler = [
        entries["Plaka"].get(),
        entries["Tarih"].get(),
        entries["Müşteri Adı Soyadı"].get(),
        entries["Telefon"].get(),
        entries["İşlem"].get(),
        entries["Ücret"].get()
    ]
    if not all(veriler):
        messagebox.showwarning("Eksik Veri", "Tüm alanları doldurun.")
        return
    try:
        veriler[5] = float(veriler[5])
    except ValueError:
        messagebox.showerror("Hata", "Ücret sayısal olmalıdır.")
        return

    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO servis_kayit (plaka, tarih, musteri_ad, telefon, islem, ucret)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, veriler)
            conn.commit()
            messagebox.showinfo("Başarılı", "Kayıt eklendi.")
            verileri_yukle()
        except Exception as e:
            messagebox.showerror("Kayıt Hatası", str(e))
        finally:
            conn.close()

# Kayıt silme
def kayit_sil():
    secilen = table.selection()
    if not secilen:
        messagebox.showwarning("Uyarı", "Silmek için bir kayıt seçin.")
        return
    secilen_id = table.item(secilen)["values"][0]
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM servis_kayit WHERE id = %s", (secilen_id,))
            conn.commit()
            messagebox.showinfo("Başarılı", "Kayıt silindi.")
            verileri_yukle()
        except Exception as e:
            messagebox.showerror("Silme Hatası", str(e))
        finally:
            conn.close()

# Kayıt güncelleme
def kayit_guncelle():
    secilen = table.selection()
    if not secilen:
        messagebox.showwarning("Uyarı", "Güncellemek için bir kayıt seçin.")
        return
    secilen_id = table.item(secilen)["values"][0]
    veriler = [
        entries["Plaka"].get(),
        entries["Tarih"].get(),
        entries["Müşteri Adı Soyadı"].get(),
        entries["Telefon"].get(),
        entries["İşlem"].get(),
        entries["Ücret"].get()
    ]
    if not all(veriler):
        messagebox.showwarning("Eksik Veri", "Tüm alanları doldurun.")
        return
    try:
        veriler[5] = float(veriler[5])
    except ValueError:
        messagebox.showerror("Hata", "Ücret sayısal olmalıdır.")
        return

    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE servis_kayit 
                SET plaka = %s, tarih = %s, musteri_ad = %s, telefon = %s, islem = %s, ucret = %s
                WHERE id = %s
            """, (*veriler, secilen_id))
            conn.commit()
            messagebox.showinfo("Başarılı", "Kayıt güncellendi.")
            verileri_yukle()
        except Exception as e:
            messagebox.showerror("Güncelleme Hatası", str(e))
        finally:
            conn.close()

# Arayüz başlangıcı
root = tk.Tk()
root.title("SBS AUTO - Servis Takip Sistemi")
root.geometry("1100x700")
root.configure(bg="#f4f4f4")

tk.Label(root, text="SBS AUTO SERVİS SİSTEMİ", font=("Arial", 20, "bold"), bg="#f4f4f4").pack(pady=20)

form_frame = tk.Frame(root, bg="#f4f4f4")
form_frame.pack(padx=20, pady=10)

entries = {}
fields = ["Plaka", "Tarih", "Müşteri Adı Soyadı", "Telefon", "İşlem", "Ücret"]
for i, field in enumerate(fields):
    tk.Label(form_frame, text=field, font=("Arial", 12), bg="#f4f4f4").grid(row=i, column=0, pady=5, sticky="e")
    ent = tk.Entry(form_frame, font=("Arial", 12), width=30)
    ent.grid(row=i, column=1, pady=5, padx=10)
    entries[field] = ent

btn_frame = tk.Frame(root, bg="#f4f4f4")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Ekle", command=kayit_ekle, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Sil", command=kayit_sil, font=("Arial", 12), bg="#F44336", fg="white").grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Güncelle", command=kayit_guncelle, font=("Arial", 12), bg="#FF9800", fg="white").grid(row=0, column=2, padx=10)

columns = ("ID", "Plaka", "Tarih", "Müşteri Adı Soyadı", "Telefon", "İşlem", "Ücret")
table = ttk.Treeview(root, columns=columns, show="headings", height=12)
table.pack(padx=20, pady=10)
for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center")

btn_export = tk.Frame(root, bg="#f4f4f4")
btn_export.pack(pady=10)
tk.Button(btn_export, text="Excel Çıktısı", command=excel_dosya_olustur, font=("Arial", 12), bg="#2196F3", fg="white").pack(side="left", padx=10)
tk.Button(btn_export, text="PDF Çıktısı", command=pdf_dosya_olustur, font=("Arial", 12), bg="#9C27B0", fg="white").pack(side="right", padx=10)

verileri_yukle()
root.mainloop()
