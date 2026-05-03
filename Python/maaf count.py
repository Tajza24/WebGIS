def count_apologies(text):
    """
    Menghitung jumlah kata maaf dan sorry dalam teks.
    Menangani berbagai variasi penulisan dan case sensitivity.
    
    Args:
        text (str): Teks yang akan dianalisis
        
    Returns:
        dict: Dictionary berisi jumlah kemunculan tiap jenis kata maaf
    """
    # Konversi teks ke lowercase untuk menangani case sensitivity
    text = text.lower()
    
    # List kata maaf dalam berbagai bentuk
    maaf_variations = [
        'maaf', 'sorry', 'sori', 'maap', 'map', 
        'ma\'af', 'maaff', 'maafin', 'maafkan',
        'sorry\'s', 'sori ya', 'maaf ya'
    ]
    
    # Dictionary untuk menyimpan hasil perhitungan
    apology_count = {variation: 0 for variation in maaf_variations}
    
    # Split teks menjadi kata-kata
    words = text.split()
    
    # Hitung kemunculan setiap variasi
    for word in words:
        word = word.strip('.,!?()[]{}":;')  # Hapus tanda baca
        for variation in maaf_variations:
            if word == variation:
                apology_count[variation] += 1
    
    # Hitung total
    total_count = sum(apology_count.values())
    apology_count['total'] = total_count
    
    return apology_count

def print_apology_stats(text):
    """
    Mencetak statistik kata maaf dalam format yang mudah dibaca
    
    Args:
        text (str): Teks yang akan dianalisis
    """
    results = count_apologies(text)
    
    print("Statistik Kata Maaf:")
    print("-" * 30)
    
    # Cetak hasil untuk setiap variasi yang ditemukan
    for variation, count in results.items():
        if count > 0 and variation != 'total':
            print(f"'{variation}': {count} kali")
    
    print("-" * 30)
    print(f"Total kata maaf: {results['total']}")

# Contoh penggunaan
if __name__ == "__main__":
    sample_text = """
    Maaf saya terlambat. Sorry for being late. 
    Maafkan saya, saya tidak bermaksud. Maaf ya.
    Sori, saya lupa. Ma'af telah mengganggu.
    """
    
    print_apology_stats(sample_text)