# bookstore_gui.py
# GUI kemas: ISBN + cadangan, carian Tajuk & Penulis, semua ikut gaya seragam
import tkinter as tk
from tkinter import ttk
from book_data import books as DATA

# ============== LOGIC ==============
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

def binary_search_books(arr, target_isbn):
    low, high = 0, len(arr)-1
    while low <= high:
        mid = (low+high)//2
        v = arr[mid]['isbn']
        if v == target_isbn: return arr[mid]
        if v < target_isbn: low = mid+1
        else: high = mid-1
    return None

def suggest_books(arr, user_input):
    s = "".join(ch for ch in str(user_input) if ch.isdigit())
    if not s: return []
    if len(s) < 4:
        hit = [b for b in arr if s in str(b['isbn'])]
        return hit[:5]
    pref = [b for b in arr if str(b['isbn']).startswith(s)]
    if pref: return pref[:5]
    try:
        t = int(s)
        def dist(b):
            bs = str(b['isbn'])
            bp = int(bs[:len(s)]) if len(bs) >= len(s) else int(bs)
            return abs(bp - t)
        return sorted(arr, key=dist)[:5]
    except:
        return []

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

BOOKS = sorted(DATA, key=lambda x: x['isbn'])

# ============== GUI (styling) ==============
BG      = "#f5f7fb"
CARD    = "#ffffff"
TEXT    = "#0f172a"
MUTED   = "#475569"
BTN_BG  = "#e2e8f0"
BTN_HOV = "#cbd5e1"
BTN_ACT = "#94a3b8"
HEAD_BG = "#e5e7eb"
ROW_ODD = "#fbfdff"
ROW_EVN = "#ffffff"
SEL_BG  = "#dbeafe"

root = tk.Tk()
root.title("=== Kedai Buku Online ===")
root.minsize(1000, 620)
root.configure(bg=BG)

style = ttk.Style()
try: style.theme_use("clam")
except: pass
style.configure("TFrame", background=BG)
style.configure("Card.TFrame", background=CARD, relief="flat")
style.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 14, "bold"))
style.configure("Body.TLabel",  background=BG, foreground=MUTED, font=("Segoe UI", 10))
style.configure("Input.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10, "bold"))

style.layout("Menu.TButton", [("Button.border", {"sticky":"nswe","children":[
    ("Button.padding", {"sticky":"nswe","children":[("Button.label", {"sticky":"nswe"})]})
]})])
style.configure("Menu.TButton", background=BTN_BG, foreground=TEXT,
                borderwidth=0, focusthickness=0, padding=(14,10),
                font=("Segoe UI", 10), relief="flat")
style.map("Menu.TButton",
          background=[("active", BTN_HOV), ("pressed", BTN_ACT)],
          relief=[("pressed","flat"), ("!pressed","flat")])

style.configure("TEntry", padding=8, fieldbackground="white", foreground=TEXT)

style.configure("Treeview", background="white", fieldbackground="white",
                foreground=TEXT, rowheight=28, borderwidth=0)
style.map("Treeview", background=[("selected", SEL_BG)], foreground=[("selected", TEXT)])
style.configure("Treeview.Heading", background=HEAD_BG, foreground=TEXT,
                font=("Segoe UI", 10, "bold"), relief="flat")

# header
ttk.Label(root, text="=== Kedai Buku Online ===", style="Title.TLabel").pack(anchor="w", padx=8, pady=(2,10))

# inputs
inp = ttk.Frame(root); inp.pack(fill="x", padx=8)
# ISBN
ttk.Label(inp, text="Masuk ISBN:", style="Input.TLabel").grid(row=0, column=0, sticky="w")
isbn_var = tk.StringVar(); isbn_entry = ttk.Entry(inp, textvariable=isbn_var, width=36)
isbn_entry.grid(row=0, column=1, sticky="we", padx=(8,16))
# Title
ttk.Label(inp, text="Cari Tajuk:", style="Input.TLabel").grid(row=0, column=2, sticky="w")
title_var = tk.StringVar(); title_entry = ttk.Entry(inp, textvariable=title_var, width=36)
title_entry.grid(row=0, column=3, sticky="we", padx=(8,16))
# Author
ttk.Label(inp, text="Cari Penulis:", style="Input.TLabel").grid(row=0, column=4, sticky="w")
author_var = tk.StringVar(); author_entry = ttk.Entry(inp, textvariable=author_var, width=28)
author_entry.grid(row=0, column=5, sticky="we", padx=(8,0))
for c in (1,3,5): inp.columnconfigure(c, weight=1)

# buttons
btns = ttk.Frame(root); btns.pack(fill="x", padx=8, pady=(10,6))

def clear_table():
    for i in tree.get_children(): tree.delete(i)

def fill_table(rows):
    clear_table()
    for idx, b in enumerate(rows):
        tag = "odd" if idx % 2 else "even"
        tree.insert("", "end", values=(b['isbn'], b['title'], b['author'], f"RM{b['price']:.2f}"), tags=(tag,))
    tree.tag_configure("odd", background=ROW_ODD)
    tree.tag_configure("even", background=ROW_EVN)

def action_search_isbn():
    raw = isbn_var.get().strip()
    only_digits = "".join(ch for ch in raw if ch.isdigit())
    result = None
    if len(only_digits) == 13:
        try: result = binary_search_books(BOOKS, int(only_digits))
        except: result = None
    if result:
        status.set("Buku dijumpai:")
        fill_table([result])
    else:
        cand = suggest_books(BOOKS, raw)
        if cand:
            cand_sorted = sorted(cand, key=lambda b: b['price'])  # sort cadangan ikut harga
            status.set("ISBN tidak dijumpai. Mungkin anda mencari ISBN buku dibawah:")
            fill_table(cand_sorted)
        else:
            status.set("ISBN tidak dijumpai dan tiada cadangan.")
            clear_table()

def action_search_title():
    q = title_var.get()
    res = search_by_title(BOOKS, q)
    if res:
        status.set(f"Carian tajuk mengandungi '{q}':")
        fill_table(res)
    else:
        status.set("Tiada buku dengan tajuk tersebut.")
        clear_table()

def action_search_author():
    q = author_var.get()
    res = search_by_author(BOOKS, q)
    if res:
        status.set(f"Carian penulis mengandungi '{q}':")
        fill_table(res)
    else:
        status.set("Tiada buku dengan nama penulis tersebut.")
        clear_table()

def action_list_all():
    data_copy = BOOKS[:]
    merge_sort_books(data_copy)
    status.set("Senarai semua buku mengikut harga:")
    fill_table(data_copy)

ttk.Button(btns, text="1. Cari buku ikut ISBN", style="Menu.TButton", command=action_search_isbn).pack(fill="x", pady=(0,8))
ttk.Button(btns, text="2. Cari buku ikut Tajuk", style="Menu.TButton", command=action_search_title).pack(fill="x", pady=(0,8))
ttk.Button(btns, text="3. Cari buku ikut Penulis", style="Menu.TButton", command=action_search_author).pack(fill="x", pady=(0,8))
ttk.Button(btns, text="4. Senarai semua buku mengikut harga", style="Menu.TButton", command=action_list_all).pack(fill="x", pady=(0,8))
ttk.Button(btns, text="5. Keluar", style="Menu.TButton", command=root.destroy).pack(fill="x")

# status
status = tk.StringVar(value="")
ttk.Label(root, textvariable=status, style="Body.TLabel").pack(fill="x", padx=8, pady=(10,4))

# table
card = ttk.Frame(root, style="Card.TFrame"); card.pack(fill="both", expand=True, padx=8, pady=(0,8))
columns = ("isbn", "title", "author", "price")
tree = ttk.Treeview(card, columns=columns, show="headings")
for col, w, anchor in (("isbn",180,"w"), ("title",560,"w"), ("author",280,"w"), ("price",120,"e")):
    tree.heading(col, text=col.capitalize() if col!="isbn" else "ISBN")
    tree.column(col, width=w, anchor=anchor)
vsb = ttk.Scrollbar(card, orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(card, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
tree.grid(row=0, column=0, sticky="nsew"); vsb.grid(row=0, column=1, sticky="ns"); hsb.grid(row=1, column=0, sticky="ew")
card.rowconfigure(0, weight=1); card.columnconfigure(0, weight=1)

isbn_entry.focus()
root.mainloop()