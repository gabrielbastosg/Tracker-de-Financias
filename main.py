"""
Finance Tracker - Versão A (Moderna com emojis)
Requisitos: customtkinter, matplotlib

Instalação (se necessário):
pip install customtkinter matplotlib
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#* ---------------------------
#* Paleta de cores (tema)
#* ---------------------------
PRIMARY = "#4CAF50"       # *verde suave
PRIMARY_DARK = "#2E7D32"
ACCENT = "#00BCD4"        #* azul ciano
BACKGROUND = "#181818"
SURFACE = "#242424"
TEXT = "#FFFFFF"
TEXT_LIGHT = "#BFBFBF"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        #* Configurações da janela
        self.title("Controle Financeiro — Moderno")
        self.geometry("1000x600")
        self.minsize(900, 520)

        # *Dados
        self.income = 0.0
        self.expense = 0.0
        self.income_transactions = []   #* lista de tuples (categoria, valor)
        self.expense_transactions = []

        #* Grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #* ---------------------------
        #* Sidebar
        # *---------------------------
        self.sidebar = ctk.CTkFrame(self, width=260, fg_color=SURFACE, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="💰 Finance Tracker",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=PRIMARY
        )
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        #* Botões com estilo
        button_style = {
            "width": 220,
            "height": 48,
            "corner_radius": 10,
            "fg_color": PRIMARY,
            "hover_color": PRIMARY_DARK,
            "font": ctk.CTkFont(size=15, weight="bold")
        }

        self.btn_income = ctk.CTkButton(self.sidebar, text="📈 Receitas", command=self.show_income, **button_style)
        self.btn_income.grid(row=1, column=0, padx=20, pady=8)

        self.btn_expense = ctk.CTkButton(self.sidebar, text="💸 Despesas", command=self.show_expense, **button_style)
        self.btn_expense.grid(row=2, column=0, padx=20, pady=8)

        self.btn_balance = ctk.CTkButton(self.sidebar, text="📊 Balanço", command=self.show_balance, **button_style)
        self.btn_balance.grid(row=3, column=0, padx=20, pady=8)

        #* Espaço e versão/autor
        self.version_label = ctk.CTkLabel(self.sidebar, text="v1.0 • por você", text_color=TEXT_LIGHT, font=ctk.CTkFont(size=11))
        self.version_label.grid(row=7, column=0, padx=20, pady=10, sticky="s")

        #* ---------------------------
        #* Área principal (conteúdo)
        #* ---------------------------
        self.main_area = ctk.CTkFrame(self, fg_color=BACKGROUND, corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=(20, 20), pady=20)

        #* Container interno para padding
        self.container = ctk.CTkFrame(self.main_area, fg_color=SURFACE, corner_radius=12)
        # corrigido: não passar width/height para place(); usar relx/rely/relwidth/relheight
        self.container.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        #* Frames para as views
        self.frame_income = self.build_transaction_frame("Receita", self.add_income, self.income_transactions)
        self.frame_expense = self.build_transaction_frame("Despesa", self.add_expense, self.expense_transactions)
        self.frame_balance = self.create_balance_frame()

        #* Mostrar a view inicial
        self.show_income()

        #* ---------------------------
        #* Estilização do Treeview (ttk)
        #* ---------------------------
        self.style_treeview()

    #* ---------------------------
    #* Construção dos frames
    #* ---------------------------
    def build_transaction_frame(self, title, add_command, transactions_list):
        frame = ctk.CTkFrame(self.container, fg_color=SURFACE, corner_radius=8)
        frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        #* Cabeçalho
        header = ctk.CTkLabel(frame, text=f"Adicionar {title}", font=ctk.CTkFont(size=18, weight="bold"))
        header.grid(row=0, column=0, columnspan=3, padx=20, pady=(16, 8), sticky="w")

        #* Categoria
        lbl_cat = ctk.CTkLabel(frame, text="Categoria", font=ctk.CTkFont(size=12))
        lbl_cat.grid(row=1, column=0, padx=(20, 8), pady=6, sticky="w")
        entry_cat = ctk.CTkEntry(frame, placeholder_text="ex: Salário, Freelance, Supermercado", width=320, height=36, corner_radius=8)
        entry_cat.grid(row=1, column=1, padx=(0, 20), pady=6, sticky="w")

        #* Valor
        lbl_val = ctk.CTkLabel(frame, text="Valor (R$)", font=ctk.CTkFont(size=12))
        lbl_val.grid(row=2, column=0, padx=(20, 8), pady=6, sticky="w")
        entry_val = ctk.CTkEntry(frame, placeholder_text="ex: 1500.00", width=160, height=36, corner_radius=8)
        entry_val.grid(row=2, column=1, padx=(0, 20), pady=6, sticky="w")

        #* Botão adicionar
        add_btn = ctk.CTkButton(frame, text=f"➕ Adicionar {title}", command=lambda: add_command(entry_cat, entry_val),
                                width=160, height=40, corner_radius=8, fg_color=ACCENT, hover_color="#007A86", font=ctk.CTkFont(size=12, weight="bold"))
        add_btn.grid(row=3, column=1, padx=20, pady=(6, 16), sticky="w")

        #* Tabela de transações com Scrollbar
        tree_frame = ctk.CTkFrame(frame, fg_color=SURFACE, corner_radius=8)
        tree_frame.grid(row=4, column=0, columnspan=3, padx=20, pady=(10, 20), sticky="nsew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        cols = ("Categoria", "Valor (R$)")
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse", height=10)
        tree.heading("Categoria", text="Categoria")
        tree.heading("Valor (R$)", text="Valor (R$)")
        tree.column("Categoria", anchor="w", width=420)
        tree.column("Valor (R$)", anchor="e", width=120)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")
        tree.grid(row=0, column=0, sticky="nsew", padx=(6, 0), pady=6)

        #* Inicializa com transações existentes (se houver)
        self.update_table(tree, transactions_list)

        #* Guarda referência para uso posterior
        if title.lower().startswith("recei"):
            self.income_tree = tree
        else:
            self.expense_tree = tree

        return frame

    def create_balance_frame(self):
        frame = ctk.CTkFrame(self.container, fg_color=SURFACE, corner_radius=8)
        frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        header = ctk.CTkLabel(frame, text="Balanço", font=ctk.CTkFont(size=18, weight="bold"))
        header.grid(row=0, column=0, padx=20, pady=(16, 8), sticky="w")

        #* Painel resumo (Receita / Despesa / Saldo)
        resumen_frame = ctk.CTkFrame(frame, fg_color="#1F1F1F", corner_radius=8)
        resumen_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        resumen_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.lbl_income = ctk.CTkLabel(resumen_frame, text=f"Receitas\nR$ {self.income:,.2f}", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_income.grid(row=0, column=0, padx=12, pady=12, sticky="w")

        self.lbl_expense = ctk.CTkLabel(resumen_frame, text=f"Despesas\nR$ {self.expense:,.2f}", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_expense.grid(row=0, column=1, padx=12, pady=12)

        self.lbl_balance = ctk.CTkLabel(resumen_frame, text=f"Saldo\nR$ {self.income - self.expense:,.2f}", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_balance.grid(row=0, column=2, padx=12, pady=12, sticky="e")

        #* Gráfico (matplotlib)
        self.fig = Figure(figsize=(4, 3), dpi=100)
        self.fig.patch.set_facecolor(BACKGROUND)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")

        #* Legenda/nota
        note = ctk.CTkLabel(frame, text="Distribuição de Receitas vs Despesas", text_color=TEXT_LIGHT, font=ctk.CTkFont(size=11))
        note.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="w")

        return frame

    #* ---------------------------
    #* Mostrar views
    #* ---------------------------
    def hide_all_frames(self):
        for f in [self.frame_income, self.frame_expense, self.frame_balance]:
            f.place_forget()

    def show_income(self):
        self.hide_all_frames()
        self.frame_income.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def show_expense(self):
        self.hide_all_frames()
        self.frame_expense.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def show_balance(self):
        self.hide_all_frames()
        self.frame_balance.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        self.update_balance_view()

    #*---------------------------
    #* Operações de dados
    #* ---------------------------
    def add_income(self, category_entry, amount_entry):
        category = category_entry.get().strip()
        amount = self.parse_amount(amount_entry.get().strip())
        if amount is None:
            return
        if category == "":
            category = "Sem categoria"

        self.income += amount
        self.income_transactions.append((category, amount))
        self.update_table(self.income_tree, self.income_transactions)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)

    def add_expense(self, category_entry, amount_entry):
        category = category_entry.get().strip()
        amount = self.parse_amount(amount_entry.get().strip())
        if amount is None:
            return
        if category == "":
            category = "Sem categoria"

        self.expense += amount
        self.expense_transactions.append((category, amount))
        self.update_table(self.expense_tree, self.expense_transactions)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)

    def parse_amount(self, text):
        try:
            #* permitir vírgula ou ponto
            text = text.replace(",", ".")
            value = float(text)
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            messagebox.showerror("Valor inválido", "Digite um número positivo (ex: 1500.00)")
            return None

    #* ---------------------------
    #* Atualizações visuais
    #* ---------------------------
    def update_table(self, tree, transactions):
        #* limpa
        for i in tree.get_children():
            tree.delete(i)
        #* insere
        for cat, val in transactions:
            tree.insert("", "end", values=(cat, f"{val:,.2f}"))

    def update_balance_view(self):
        #* atualizar labels de resumo
        self.lbl_income.configure(text=f"Receitas\nR$ {self.income:,.2f}")
        self.lbl_expense.configure(text=f"Despesas\nR$ {self.expense:,.2f}")
        self.lbl_balance.configure(text=f"Saldo\nR$ {self.income - self.expense:,.2f}")

        #* atualizar gráfico
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(SURFACE)
        self.fig.patch.set_facecolor(BACKGROUND)

        #* evitar divisão por zero
        inc = self.income if self.income > 0 else 0.0001
        exp = self.expense if self.expense > 0 else 0.0001

        wedges, texts, autotexts = ax.pie(
            [inc, exp],
            labels=["Receitas", "Despesas"],
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.75,
            wedgeprops={"linewidth": 1, "edgecolor": BACKGROUND}
        )

        for t in texts + autotexts:
            t.set_color(TEXT)

        ax.axis("equal")
        self.canvas.draw()

    #* ---------------------------
    #* Estilização Treeview (ttk)
    #* ---------------------------
    def style_treeview(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass

        style.configure("Treeview",
                        background=SURFACE,
                        foreground=TEXT,
                        fieldbackground=SURFACE,
                        rowheight=28,
                        borderwidth=0,
                        font=("Segoe UI", 11))
        style.configure("Treeview.Heading",
                        background=PRIMARY,
                        foreground="white",
                        font=("Segoe UI", 12, "bold"))
        style.map("Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "black")])

        #* Scrollbar style (apenas visual padrão)
        style.configure("TScrollbar", background=SURFACE)

#* ---------------------------
#* Execução
#* ---------------------------
if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()
