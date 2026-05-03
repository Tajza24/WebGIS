import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="Visualisasi Jadwal Penerbangan", layout="centered")

# ===================== DATA ======================
data_penerbangan = [
    {"Kode": "GA001", "Maskapai": "Garuda", "Tujuan": "Jakarta", "Waktu": "07:00", "Gate": "A1", "Status": "On Time"},
    {"Kode": "SJ002", "Maskapai": "Sriwijaya", "Tujuan": "Surabaya", "Waktu": "09:30", "Gate": "B2", "Status": "Delay"},
    {"Kode": "JT005", "Maskapai": "Lion Air", "Tujuan": "Yogyakarta", "Waktu": "08:15", "Gate": "A3", "Status": "On Time"},
    {"Kode": "ID007", "Maskapai": "Batik Air", "Tujuan": "Bali", "Waktu": "06:45", "Gate": "B1", "Status": "On Time"},
    {"Kode": "QZ123", "Maskapai": "Air Asia", "Tujuan": "Medan", "Waktu": "10:20", "Gate": "A2", "Status": "Delay"},
]

# ===================== KONVERSI WAKTU ======================
for item in data_penerbangan:
    waktu_obj = datetime.strptime(item["Waktu"], "%H:%M").time()
    item["Waktu_obj"] = waktu_obj
    item["Waktu_menit"] = waktu_obj.hour * 60 + waktu_obj.minute

# ===================== SORTING FUNCTION ======================
def bubble_sort_waktu(data):
    data = data.copy()
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j]["Waktu_obj"] > data[j + 1]["Waktu_obj"]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

def quick_sort_maskapai(data):
    if len(data) <= 1:
        return data
    else:
        pivot = data[0]
        less = [x for x in data[1:] if x["Maskapai"] <= pivot["Maskapai"]]
        greater = [x for x in data[1:] if x["Maskapai"] > pivot["Maskapai"]]
        return quick_sort_maskapai(less) + [pivot] + quick_sort_maskapai(greater)

# ===================== SIDEBAR ======================
st.sidebar.title("✈ Filter dan Opsi")
status_filter = st.sidebar.multiselect("Tampilkan Status:", ["On Time", "Delay"], default=["On Time", "Delay"])
tandai_perubahan = st.sidebar.checkbox("Tandai Perubahan Posisi Elemen", value=True)

# ===================== FILTER DATA ======================
filtered_data = [d for d in data_penerbangan if d["Status"] in status_filter]

# Data untuk sorting waktu (tidak diacak)
data_waktu = filtered_data.copy()
data_bubble_sorted = bubble_sort_waktu(data_waktu)

# Data untuk sorting maskapai (diacak)
data_maskapai = filtered_data.copy()
random.shuffle(data_maskapai)
for i, d in enumerate(data_maskapai):
    d["index_awal"] = i
data_quick_sorted = quick_sort_maskapai(data_maskapai)

# ===================== VISUALISASI ======================
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# ===== Bubble Sort - Sebelum =====
axs[0, 0].barh(
    [d["Waktu_obj"].strftime("%H:%M") for d in data_waktu],
    [d["Waktu_menit"] for d in data_waktu],
    color=["green" if d["Status"] == "On Time" else "red" for d in data_waktu]
)
axs[0, 0].set_title("Sebelum Sorting Waktu (Bubble Sort)")
axs[0, 0].set_xlabel("Menit dari 00:00")
axs[0, 0].set_ylabel("Waktu")
axs[0, 0].invert_yaxis()

# ===== Bubble Sort - Sesudah =====
axs[0, 1].barh(
    [d["Waktu_obj"].strftime("%H:%M") for d in data_bubble_sorted],
    [d["Waktu_menit"] for d in data_bubble_sorted],
    color=["green" if d["Status"] == "On Time" else "red" for d in data_bubble_sorted]
)
axs[0, 1].set_title("Setelah Sorting Waktu (Bubble Sort)")
axs[0, 1].set_xlabel("Menit dari 00:00")
axs[0, 1].set_ylabel("Waktu")
axs[0, 1].invert_yaxis()

if tandai_perubahan:
    for i, d in enumerate(data_bubble_sorted):
        try:
            old_index = data_waktu.index(d)
            old_val = data_waktu[old_index]["Waktu_menit"]
            new_val = d["Waktu_menit"]
            axs[0, 1].hlines(y=i, xmin=old_val, xmax=new_val, color="blue", linestyles="dashed")
        except ValueError:
            pass

# ===== Quick Sort - Sebelum =====
axs[1, 0].barh(
    [d["Maskapai"] for d in data_maskapai],
    list(range(len(data_maskapai))),
    color=["green" if d["Status"] == "On Time" else "red" for d in data_maskapai]
)
axs[1, 0].set_title("Sebelum Sorting Maskapai (Quick Sort)")
axs[1, 0].set_xlabel("Index")
axs[1, 0].set_ylabel("Maskapai")
axs[1, 0].invert_yaxis()

# ===== Quick Sort - Sesudah =====
axs[1, 1].barh(
    [d["Maskapai"] for d in data_quick_sorted],
    list(range(len(data_quick_sorted))),
    color=["green" if d["Status"] == "On Time" else "red" for d in data_quick_sorted]
)
axs[1, 1].set_title("Setelah Sorting Maskapai (Quick Sort)")
axs[1, 1].set_xlabel("Index")
axs[1, 1].set_ylabel("Maskapai")
axs[1, 1].invert_yaxis()

if tandai_perubahan:
    for i, d in enumerate(data_quick_sorted):
        try:
            old_index = d["index_awal"]
            axs[1, 1].hlines(y=i, xmin=old_index, xmax=i, color="blue", linestyles="dashed")
        except KeyError:
            pass

plt.tight_layout()

# ===================== STREAMLIT TAMPILAN ======================
st.markdown("<h1 style='text-align: center; color: #FFCC00;'>✈ Visualisasi Sorting Jadwal Penerbangan</h1>", unsafe_allow_html=True)
st.markdown("Selamat datang! Di Halaman Ini Kamu Bisa Melihat Bagaimana Proses Sorting Jadwal Penerbangan Berdasarkan Waktu Keberangkatan dan Maskapai Dilakukan Menggunakan Bubble Sort dan Quick Sort.")
st.markdown("Gunakan Sidebar Untuk Menyaring Status dan Menandai Perubahan Posisi Setelah Sorting!")

st.pyplot(fig)