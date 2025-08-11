# bookstore.py (CLI)
# uniform dgn GUI: teks menu, prompt & status
from book_data import books
import os, shutil, time, sys

# clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# lebar column ikut skrin
def get_column_widths():
    total = shutil.get_terminal_size((120, 30)).columns
    pipes = 5
    min_isbn, min_title, min_author, min_price = 16, 30, 24, 10
    min_sum = min_isbn + min_title + min_author + min_price
    text_area = max(total - pipes, min_sum + 4)
    extra = max(text_area - min_sum, 0)
    add_title = int(extra * 0.7)
    add_author = extra - add_title
    return min_isbn, min_title + add_title, min_author + add_author, min_price

def make_border(wi, wt, wa, wp):
    return "+" + "-"*wi + "+" + "-"*wt + "+" + "-"*wa + "+" + "-"*wp + "+"

def fit_cell(text, width):
    s = str(text)
    if len(s) <= width:
        return f"{s:<{width}}"
    if width <= 1:
        return "…"
    return s[:width-1] + "…"

# merge sort (ikut harga)
def merge_sort_books(arr):
    if len(arr) <= 1: return
    mid = len(arr)//2
    left, right = arr[:mid], arr[mid:]
    merge_sort_books(left); merge_sort_books(right)
    i=j=k=0
    while i<len(left) and j<len(right):
        if left[i]['price'] < right[j]['price']:
            arr[k]=left[i]; i+=1
        else:
            arr[k]=right[j]; j+=1
        k+=1
    while i<len(left): arr[k]=left[i]; i+=1; k+=1
    while j<len(right): arr[k]=right[j]; j+=1; k+=1

# binary search (exact 13 digit)
def binary_search_books(arr, target_isbn):
    low, high = 0, len(arr)-1
    while low <= high:
        mid = (low+high)//2
        v = arr[mid]['isbn']
        if v == target_isbn: return arr[mid]
        if v < target_isbn: low = mid+1
        else: high = mid-1
    return None

# cadangan ISBN (prefix > nearest) max 5, sort ikut harga
def suggest_books(arr, user_input):
    s = "".join(ch for ch in str(user_input) if ch.isdigit())
    if not s: return []
    if len(s) < 4:
        hit = [b for b in arr if s in str(b['isbn'])]
        return sorted(hit, key=lambda b: b['price'])[:5]
    pref = [b for b in arr if str(b['isbn']).startswith(s)]
    if pref:
        return sorted(pref, key=lambda b: b['price'])[:5]
    try:
        t = int(s)
        def dist(b):
            bs = str(b['isbn'])
            bp = int(bs[:len(s)]) if len(bs) >= len(s) else int(bs)
            return abs(bp - t)
        near = sorted(arr, key=dist)[:5]
        return sorted(near, key=lambda b: b['price'])
    except:
        return []

# carian tajuk/penulis (separa padanan), sort harga
def search_by_title(arr, q):
    q = q.strip().lower()
    if not q: return []
    res = [b for b in arr if q in b['title'].lower()]
    return sorted(res, key=lambda x: x['price'])

def search_by_author(arr, q):
    q = q.strip().lower()
    if not q: return []
    res = [b for b in arr if q in b['author'].lower()]
    return sorted(res, key=lambda x: x['price'])

# print table penuh skrin
def print_table(data):
    wi, wt, wa, wp = get_column_widths()
    border = make_border(wi, wt, wa, wp)
    print(border)
    print("|" + fit_cell("ISBN", wi) + "|" + fit_cell("Title", wt) + "|" + fit_cell("Author", wa) + "|" + fit_cell("Price", wp) + "|")
    print(border)
    for b in data:
        print("|" + fit_cell(b['isbn'], wi) + "|" + fit_cell(b['title'], wt) + "|" + fit_cell(b['author'], wa) + "|" + fit_cell(f"RM{b['price']:.2f}", wp) + "|")
    print(border)

# siap: sort by ISBN utk binary search
books.sort(key=lambda x: x['isbn'])

# main loop (teks uniform dgn GUI)
clear_screen()
while True:
    clear_screen()
    print("=== Kedai Buku Online ===")
    print("1. Cari buku ikut ISBN")
    print("2. Cari buku ikut Tajuk")
    print("3. Cari buku ikut Penulis")
    print("4. Senarai semua buku mengikut harga")
    print("5. Keluar")
    pilih = input("\nPilih nombor: ").strip()

    if pilih == "1":
        clear_screen()
        raw = input("Masuk ISBN: ").strip()
        only_digits = "".join(ch for ch in raw if ch.isdigit())
        result = None
        if len(only_digits) == 13:
            try: result = binary_search_books(books, int(only_digits))
            except: result = None
        clear_screen()
        if result:
            print("Buku dijumpai:\n")
            print_table([result])
        else:
            cad = suggest_books(books, raw)
            if cad:
                print("ISBN tidak dijumpai. Mungkin anda mencari ISBN buku dibawah:\n")
                print_table(cad)
            else:
                print("ISBN tidak dijumpai dan tiada cadangan.")
        input("\nEnter untuk balik ke menu utama")

    elif pilih == "2":
        clear_screen()
        q = input("Cari Tajuk: ").strip()
        res = search_by_title(books, q)
        clear_screen()
        if res:
            print(f"Carian tajuk mengandungi '{q}':\n")
            print_table(res)
        else:
            print("Tiada buku dengan tajuk tersebut.")
        input("\nEnter untuk balik ke menu utama")

    elif pilih == "3":
        clear_screen()
        q = input("Cari Penulis: ").strip()
        res = search_by_author(books, q)
        clear_screen()
        if res:
            print(f"Carian penulis mengandungi '{q}':\n")
            print_table(res)
        else:
            print("Tiada buku dengan nama penulis tersebut.")
        input("\nEnter untuk balik ke menu utama")

    elif pilih == "4":
        clear_screen()
        data_copy = books[:]
        merge_sort_books(data_copy)
        print("Senarai semua buku mengikut harga:\n")
        print_table(data_copy)
        input("\nEnter untuk balik ke menu utama")

    elif pilih == "5":
        clear_screen()
        print("Sila datang lagi!")
        print("")
        for s in range(5, 0, -1):
            sys.stdout.write(f"\rProgram akan di tutup dalam masa {s} saat... ")
            sys.stdout.flush()
            time.sleep(1)

        clear_screen()
        break  # keluar dari while True dan tamat program

    else:
        clear_screen()
        print("Pilihan tak valid.")
        input("Enter untuk balik ke menu utama")