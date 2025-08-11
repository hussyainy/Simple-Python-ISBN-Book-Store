# bookstore.py
# simple: kedai buku + cari ISBN + cadangan
from book_data import books
import os
import shutil

# clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# lebar column ikut skrin
def get_column_widths():
    total = shutil.get_terminal_size((120, 30)).columns  # default 120 kalau tak detect
    pipes = 5  # '|' kiri/kanan/antara
    # min lebar
    min_isbn, min_title, min_author, min_price = 16, 30, 24, 10
    min_sum = min_isbn + min_title + min_author + min_price
    text_area = max(total - pipes, min_sum + 4)
    extra = max(text_area - min_sum, 0)
    # bagi title paling banyak ruang
    add_title = int(extra * 0.7)
    add_author = extra - add_title
    return min_isbn, min_title + add_title, min_author + add_author, min_price

# border table
def make_border(wi, wt, wa, wp):
    return "+" + "-"*wi + "+" + "-"*wt + "+" + "-"*wa + "+" + "-"*wp + "+"

# potong teks kalau panjang (letak …)
def fit_cell(text, width):
    s = str(text)
    if len(s) <= width:
        return f"{s:<{width}}"
    if width <= 1:
        return "…"
    return s[:width-1] + "…"

# merge sort (ikut harga)
def merge_sort_books(arr):
    if len(arr) <= 1:
        return
    mid = len(arr) // 2
    left, right = arr[:mid], arr[mid:]
    merge_sort_books(left)
    merge_sort_books(right)
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i]['price'] < right[j]['price']:
            arr[k] = left[i]; i += 1
        else:
            arr[k] = right[j]; j += 1
        k += 1
    while i < len(left): arr[k] = left[i]; i += 1; k += 1
    while j < len(right): arr[k] = right[j]; j += 1; k += 1

# binary search (exact 13 digit)
def binary_search_books(arr, target_isbn):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        v = arr[mid]['isbn']
        if v == target_isbn: return arr[mid]
        if v < target_isbn: low = mid + 1
        else: high = mid - 1
    return None

# cadangan ISBN (prefix > nearest) max 5
def suggest_books(arr, user_input):
    s = "".join(ch for ch in str(user_input) if ch.isdigit())
    if not s:
        return []
    # <4 digit: longgar (substring)
    if len(s) < 4:
        hit = [b for b in arr if s in str(b['isbn'])]
        return hit[:5]
    # cuba prefix
    pref = [b for b in arr if str(b['isbn']).startswith(s)]
    if pref:
        return pref[:5]
    # nearest ikut prefix numeric
    try:
        t = int(s)
        def dist(b):
            bs = str(b['isbn'])
            bp = int(bs[:len(s)]) if len(bs) >= len(s) else int(bs)
            return abs(bp - t)
        near = sorted(arr, key=dist)
        return near[:5]
    except:
        return []

# print table full skrin
def print_table(data):
    wi, wt, wa, wp = get_column_widths()
    border = make_border(wi, wt, wa, wp)
    print(border)
    print("|" + fit_cell("ISBN", wi) + "|" + fit_cell("Title", wt) + "|" + fit_cell("Author", wa) + "|" + fit_cell("Price", wp) + "|")
    print(border)
    for b in data:
        print("|" + fit_cell(b['isbn'], wi) + "|" + fit_cell(b['title'], wt) + "|" + fit_cell(b['author'], wa) + "|" + fit_cell(f"RM{b['price']:.2f}", wp) + "|")
    print(border)

# ready: sort by isbn utk binary search
books.sort(key=lambda x: x['isbn'])

# start
clear_screen()
while True:
    clear_screen()
    print("=== Kedai Buku Online ===")
    print("1. Cari buku ikut ISBN")
    print("2. Senarai semua buku ikut harga (dari murah -> mahal)")
    print("3. Keluar")
    pilih = input("\nPilih nombor: ").strip()

    if pilih == "1":
        clear_screen()
        raw = input("Masuk ISBN: ").strip()
        only_digits = "".join(ch for ch in raw if ch.isdigit())
        result = None
        if len(only_digits) == 13:
            try:
                result = binary_search_books(books, int(only_digits))
            except:
                result = None

        clear_screen()
        if result:
            print("Buku dijumpai:\n")
            print_table([result])
        else:
            cad = suggest_books(books, raw)
            if cad:
                print("ISBN tidak dijumpai. Mungkin anda mencari ISBN buku dibawah :\n")
                print_table(cad)
            else:
                print("ISBN tidak dijumpai dan tiada cadangan.")
        input("\nEnter untuk balik ke menu...")

    elif pilih == "2":
        clear_screen()
        data_copy = books[:]  # tak kacau order asal
        merge_sort_books(data_copy)
        print("Senarai semua buku ikut harga (dari murah -> mahal):\n")
        print_table(data_copy)
        input("\nEnter untuk balik ke menu...")

    elif pilih == "3":
        clear_screen()
        print("Bye bye~")
        break

    else:
        clear_screen()
        print("Pilihan tak valid.")
        input("Enter untuk balik ke menu...")