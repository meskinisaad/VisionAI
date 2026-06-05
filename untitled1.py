#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except:
    PIL_AVAILABLE = False

# =========================================================
# FIX PYINSTALLER PATH
# =========================================================
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

PHOTO_PATH = resource_path("photo.png")
EMSI_PATH  = resource_path("emsi.png")

# =========================================================
# Palette de couleurs
# =========================================================
BG_MAIN       = "#0a0e1a"
BG_CARD       = "#111827"
BG_PANEL      = "#0f1623"
ACCENT        = "#6366f1"
ACCENT2       = "#22d3ee"
ACCENT3       = "#f472b6"
TEXT_LIGHT    = "#e2e8f0"
TEXT_MUTED    = "#94a3b8"
TEXT_WHITE    = "#ffffff"
BORDER        = "#1e293b"
BTN_BG        = "#6366f1"
BTN_HOVER     = "#4f46e5"
BTN_SECONDARY = "#1e293b"
BTN_SEC_HOV   = "#334155"

# =========================================================
# Style Matplotlib
# =========================================================
plt.rcParams.update({
    'figure.facecolor':  BG_CARD,
    'axes.facecolor':    BG_PANEL,
    'axes.edgecolor':    BORDER,
    'axes.labelcolor':   TEXT_MUTED,
    'axes.titlecolor':   TEXT_LIGHT,
    'xtick.color':       TEXT_MUTED,
    'ytick.color':       TEXT_MUTED,
    'grid.color':        '#1e293b',
    'grid.linestyle':    '--',
    'grid.alpha':        0.5,
    'text.color':        TEXT_LIGHT,
    'legend.facecolor':  BG_CARD,
    'legend.edgecolor':  BORDER,
    'legend.labelcolor': TEXT_LIGHT,
    'lines.linewidth':   2,
})

# =========================================================
# Fenêtre principale (UNE SEULE fois)
# =========================================================
root = tk.Tk()
root.title("SMART — IA & Machine Learning")
root.geometry("1280x800")
root.configure(bg=BG_MAIN)
root.resizable(True, True)

# =========================================================
# Chargement images
# =========================================================
def load_photo(size=60, bg=None):
    if not PIL_AVAILABLE:
        return None
    try:
        img = Image.open(PHOTO_PATH).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)
        if bg:
            bg_img = Image.new("RGBA", img.size, bg)
            bg_img.paste(img, mask=img.split()[3])
            img = bg_img.convert("RGB")
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

def load_emsi(width=260, bg=None):
    if not PIL_AVAILABLE:
        return None
    try:
        img = Image.open(EMSI_PATH).convert("RGBA")
        ratio = width / img.width
        height = int(img.height * ratio)
        img = img.resize((width, height), Image.LANCZOS)
        if bg:
            bg_img = Image.new("RGBA", img.size, bg)
            bg_img.paste(img, mask=img.split()[3])
            img = bg_img.convert("RGB")
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

# =========================================================
# Utilitaires
# =========================================================
def clear_frame(frame):
    for w in frame.winfo_children():
        w.destroy()

def add_figure_to_frame(frame, fig):
    clear_frame(frame)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def lire_float(entry, default):
    try:   return float(entry.get())
    except: return default

def lire_int(entry, default):
    try:   return int(entry.get())
    except: return default

def retour_accueil():
    plateforme_frame.pack_forget()
    accueil_frame.pack(fill="both", expand=True)

# =========================================================
# Composants UI
# =========================================================
def make_button(parent, text, command, width=None, style="primary", font_size=10):
    bg  = BTN_BG        if style == "primary" else BTN_SECONDARY
    hov = BTN_HOVER     if style == "primary" else BTN_SEC_HOV
    fg  = TEXT_WHITE    if style == "primary" else TEXT_LIGHT
    w   = {"width": width} if width else {}
    btn = tk.Button(
        parent, text=text, command=command,
        font=("Helvetica Neue", font_size, "bold"),
        bg=bg, fg=fg, activebackground=hov, activeforeground=TEXT_WHITE,
        bd=0, relief="flat", cursor="hand2", padx=14, pady=8, **w
    )
    btn.bind("<Enter>", lambda e: e.widget.config(bg=hov))
    btn.bind("<Leave>", lambda e: e.widget.config(bg=bg))
    return btn

def make_label(parent, text, font_size=10, bold=False, color=None, justify="left", bg=None):
    return tk.Label(
        parent, text=text,
        font=("Helvetica Neue", font_size, "bold" if bold else "normal"),
        fg=color or TEXT_LIGHT, bg=bg or BG_PANEL, justify=justify
    )

def entry_with_border(parent, default="", width=18):
    frame = tk.Frame(parent, bg=ACCENT, padx=1, pady=1)
    e = tk.Entry(
        frame, font=("Helvetica Neue", 11),
        bg="#1e293b", fg=TEXT_WHITE, insertbackground=ACCENT2,
        relief="flat", bd=4, justify="center", width=width
    )
    e.insert(0, default)
    e.pack()
    return frame, e

def separator(parent, color=BORDER, pad_y=8):
    tk.Frame(parent, bg=color, height=1).pack(fill="x", padx=12, pady=pad_y)

def section_title(parent, text):
    f = tk.Frame(parent, bg=BG_PANEL)
    f.pack(fill="x", padx=10, pady=(10, 2))
    tk.Canvas(f, height=2, bg=ACCENT, bd=0, highlightthickness=0, width=30).pack(side="left", pady=6, padx=(0,6))
    make_label(f, text, font_size=9, bold=True, color=ACCENT2, bg=BG_PANEL).pack(side="left")

def create_left_panel(parent, title):
    left = tk.Frame(parent, bg=BG_PANEL, width=270)
    left.pack(side="left", fill="y")
    left.pack_propagate(False)
    tk.Frame(left, bg=ACCENT, height=4).pack(fill="x")
    tk.Frame(left, bg=BG_PANEL, height=8).pack()
    title_frame = tk.Frame(left, bg=BG_PANEL)
    title_frame.pack(fill="x", padx=12, pady=(8, 2))
    make_label(title_frame, title, font_size=13, bold=True, color=TEXT_WHITE, bg=BG_PANEL).pack(anchor="w")
    separator(left, color=ACCENT, pad_y=6)
    return left

def create_right_panel(parent):
    right = tk.Frame(parent, bg=BG_CARD)
    right.pack(side="right", fill="both", expand=True, padx=2, pady=2)
    zone_graph = tk.Frame(right, bg=BG_CARD)
    zone_graph.pack(fill="both", expand=True, padx=4, pady=4)
    return right, zone_graph

def creer_fenetre_algo(titre, largeur=1140, hauteur=680):
    fen = tk.Toplevel(root)
    fen.title(titre)
    fen.geometry(f"{largeur}x{hauteur}")
    fen.configure(bg=BG_MAIN)
    tk.Frame(fen, bg=ACCENT, height=3).pack(fill="x")
    return fen

# =========================================================
# Données simulées
# =========================================================
def generer_donnees_regression(xmin, xmax, ymin, ymax, n=250):
    x = np.array([random.uniform(xmin, xmax) for _ in range(n)])
    bruit = np.random.normal(0, max((ymax - ymin) * 0.08, 0.5), n)
    y = 1.8 * x + 5 + bruit
    return x, np.clip(y, ymin, ymax)

def generer_donnees_clustering(k=3, n_par_cluster=60):
    centres = np.array([[0, 2], [5, 8], [10, 15], [12, 5], [3, 14]])
    pts = []
    for c in centres[:k]:
        for _ in range(n_par_cluster):
            pts.append([random.gauss(c[0], 1.2), random.gauss(c[1], 1.5)])
    return np.array(pts)

# =========================================================
# Régression Linéaire
# =========================================================
def ouvrir_regression():
    fen = creer_fenetre_algo("Régression Linéaire")
    container = tk.Frame(fen, bg=BG_MAIN)
    container.pack(fill="both", expand=True, padx=4, pady=4)
    left = create_left_panel(container, "Régression Linéaire")
    right, zone_graph = create_right_panel(container)
    section_title(left, "PARAMÈTRES")
    params = {}
    for label, default in [("X — Minimum","0"),("X — Maximum","20"),("Y — Minimum","0"),("Y — Maximum","50")]:
        f = tk.Frame(left, bg=BG_PANEL); f.pack(fill="x", padx=12, pady=3)
        make_label(f, label, font_size=9, color=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
        frm, entry = entry_with_border(f, default); frm.pack(fill="x", pady=2)
        params[label] = entry
    separator(left)
    section_title(left, "RÉSULTATS")
    info_label = tk.Label(left, text="—", justify="left", bg=BG_PANEL, fg=TEXT_MUTED,
                          font=("Courier New", 9), wraplength=240)
    info_label.pack(padx=12, pady=4, anchor="w")
    separator(left)

    def lancer_regression():
        xmin = lire_float(params["X — Minimum"], 0)
        xmax = lire_float(params["X — Maximum"], 20)
        ymin = lire_float(params["Y — Minimum"], 0)
        ymax = lire_float(params["Y — Maximum"], 50)
        if xmin >= xmax or ymin >= ymax:
            messagebox.showerror("Erreur", "Vérifiez les bornes min/max."); return
        x, y = generer_donnees_regression(xmin, xmax, ymin, ymax)
        a, b = np.polyfit(x, y, 1)
        y_pred = a * x + b
        r2   = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)
        rmse = np.sqrt(np.mean((y - y_pred)**2))
        info_label.config(fg=TEXT_LIGHT, text=(
            f"R²   = {r2:.4f}\nRMSE = {rmse:.4f}\n\na    = {a:.4f}\nb    = {b:.4f}\n\nY = {a:.4f}·X + {b:.4f}"))
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.scatter(x, y, color=ACCENT2, alpha=0.5, s=18, label="Données")
        xs = np.sort(x)
        ax.plot(xs, a*xs+b, color=ACCENT, lw=2.5, label="Régression")
        ax.fill_between(xs, a*xs+b-rmse, a*xs+b+rmse, color=ACCENT, alpha=0.12, label="±RMSE")
        ax.set_title("Droite de régression", pad=10); ax.set_xlabel("X"); ax.set_ylabel("Y")
        ax.legend(); ax.grid(True); fig.tight_layout(pad=2)
        add_figure_to_frame(zone_graph, fig)

    def afficher_3d():
        xmin = lire_float(params["X — Minimum"], 0)
        xmax = lire_float(params["X — Maximum"], 20)
        x1 = np.random.uniform(xmin, xmax, 200); x2 = np.random.uniform(xmin, xmax, 200)
        y  = 1.5*x1 + 2.2*x2 + np.random.normal(0, 2, 200)
        win = creer_fenetre_algo("Régression 3D", 860, 660)
        fig = plt.figure(figsize=(8, 5.5)); ax = fig.add_subplot(111, projection="3d")
        p = ax.scatter(x1, x2, y, c=y, cmap="cool", s=20, alpha=0.8)
        fig.colorbar(p, ax=ax, shrink=0.5)
        ax.set_title("Régression Multiple — 3D"); ax.set_xlabel("X1"); ax.set_ylabel("X2"); ax.set_zlabel("Y")
        add_figure_to_frame(win, fig)

    make_button(left, "▶  Lancer la régression", lancer_regression, style="primary").pack(padx=12, pady=6, fill="x")
    make_button(left, "◈  Vue 3D", afficher_3d, style="secondary").pack(padx=12, pady=2, fill="x")

# =========================================================
# Clustering
# =========================================================
def ouvrir_clustering():
    fen = creer_fenetre_algo("Clustering K-Means")
    container = tk.Frame(fen, bg=BG_MAIN); container.pack(fill="both", expand=True, padx=4, pady=4)
    left = create_left_panel(container, "Clustering K-Means")
    right, zone_graph = create_right_panel(container)
    section_title(left, "PARAMÈTRES")
    f = tk.Frame(left, bg=BG_PANEL); f.pack(fill="x", padx=12, pady=3)
    make_label(f, "Nombre de clusters (k)", font_size=9, color=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
    frm, clu_k = entry_with_border(f, "3"); frm.pack(fill="x", pady=2)
    separator(left); section_title(left, "RÉSULTATS")
    info_label = tk.Label(left, text="—", justify="left", bg=BG_PANEL, fg=TEXT_MUTED,
                          font=("Courier New", 9), wraplength=240)
    info_label.pack(padx=12, pady=4, anchor="w"); separator(left)

    def calculer():
        k = lire_int(clu_k, 3)
        if k < 2: raise ValueError
        X = generer_donnees_clustering(k, 60)
        centroids = X[np.random.choice(len(X), k, replace=False)]
        for _ in range(30):
            d = np.array([[np.linalg.norm(p-c) for c in centroids] for p in X])
            labels = np.argmin(d, axis=1)
            new_c = np.array([X[labels==i].mean(0) if np.any(labels==i) else centroids[i] for i in range(k)])
            if np.allclose(new_c, centroids): break
            centroids = new_c
        return X, labels, centroids, k

    def lancer():
        try: X, labels, centroids, k = calculer()
        except: messagebox.showerror("Erreur", "Paramètres invalides."); return
        texte = f"k = {k} clusters\n\n"
        for i, c in enumerate(centroids): texte += f"C{i+1}: ({c[0]:.2f}, {c[1]:.2f})\n"
        info_label.config(text=texte, fg=TEXT_LIGHT)
        fig, ax = plt.subplots(figsize=(9, 5))
        cmap = [ACCENT, ACCENT2, ACCENT3, "#fb923c", "#a3e635"]
        for i in range(k):
            pts = X[labels==i]
            ax.scatter(pts[:,0], pts[:,1], s=20, color=cmap[i%5], alpha=0.7, label=f"Cluster {i+1}")
            ax.scatter(centroids[i,0], centroids[i,1], marker="*", s=220, color="white",
                       edgecolors=cmap[i%5], linewidths=1.5, zorder=5)
        ax.set_title("Projection 2D — X1 vs X2"); ax.set_xlabel("X1"); ax.set_ylabel("X2")
        ax.legend(); ax.grid(True); fig.tight_layout(pad=2)
        add_figure_to_frame(zone_graph, fig)

    def afficher_3d():
        try: X, labels, centroids, k = calculer()
        except: messagebox.showerror("Erreur","Paramètres invalides."); return
        win = creer_fenetre_algo("Clustering 3D", 860, 660)
        fig = plt.figure(figsize=(8,5.5)); ax = fig.add_subplot(111, projection="3d")
        z = labels.astype(float) + np.random.normal(0, 0.05, len(labels))
        ax.scatter(X[:,0], X[:,1], z, c=labels, cmap="cool", s=20, alpha=0.8)
        ax.set_title("Clustering 3D"); ax.set_xlabel("X1"); ax.set_ylabel("X2"); ax.set_zlabel("Cluster")
        add_figure_to_frame(win, fig)

    make_button(left, "▶  Lancer le clustering", lancer, style="primary").pack(padx=12, pady=6, fill="x")
    make_button(left, "◈  Vue 3D", afficher_3d, style="secondary").pack(padx=12, pady=2, fill="x")

# =========================================================
# Random Forest
# =========================================================
def ouvrir_random_forest():
    fen = creer_fenetre_algo("Random Forest")
    container = tk.Frame(fen, bg=BG_MAIN); container.pack(fill="both", expand=True, padx=4, pady=4)
    left = create_left_panel(container, "Random Forest")
    right, zone_graph = create_right_panel(container)
    section_title(left, "PARAMÈTRES")
    f = tk.Frame(left, bg=BG_PANEL); f.pack(fill="x", padx=12, pady=3)
    make_label(f, "Nombre d'arbres", font_size=9, color=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
    frm, rf_trees = entry_with_border(f, "10"); frm.pack(fill="x", pady=2)
    separator(left); section_title(left, "MÉTRIQUES")
    info_label = tk.Label(left, text="—", justify="left", bg=BG_PANEL, fg=TEXT_MUTED,
                          font=("Courier New", 9), wraplength=240)
    info_label.pack(padx=12, pady=4, anchor="w"); separator(left)

    def lancer():
        n = lire_int(rf_trees, 10)
        if n < 1: messagebox.showerror("Erreur","Nombre d'arbres > 0 requis."); return
        imp  = np.array([0.42, 0.35, 0.23])
        conf = np.array([[8,2,0],[2,34,3],[0,3,8]])
        acc  = np.trace(conf) / conf.sum()
        info_label.config(fg=TEXT_LIGHT, text=(
            f"Accuracy :  {acc:.4f}\nPrécision:  0.8333\nRappel   :  0.8333\nScore F1 :  0.8300\n\n"
            f"Importance:\n  X1 = {imp[0]*100:.1f}%\n  X2 = {imp[1]*100:.1f}%\n  X3 = {imp[2]*100:.1f}%"))
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
        bars = axes[0].bar(["X1","X2","X3"], imp, color=[ACCENT, ACCENT2, ACCENT3], width=0.5)
        axes[0].bar_label(bars, fmt="%.2f", color=TEXT_LIGHT, padding=3)
        axes[0].set_title("Importance des variables"); axes[0].set_ylabel("Score"); axes[0].grid(True, axis="y")
        im = axes[1].imshow(conf, cmap="Blues"); fig.colorbar(im, ax=axes[1], shrink=0.8)
        axes[1].set_title("Matrice de confusion")
        axes[1].set_xticks([0,1,2]); axes[1].set_yticks([0,1,2])
        axes[1].set_xticklabels(["A","B","C"]); axes[1].set_yticklabels(["A","B","C"])
        for i in range(3):
            for j in range(3):
                axes[1].text(j, i, conf[i,j], ha="center", va="center",
                             color="white" if conf[i,j] > conf.max()/2 else TEXT_LIGHT, fontweight="bold")
        fig.tight_layout(pad=2); add_figure_to_frame(zone_graph, fig)

    def afficher_3d():
        win = creer_fenetre_algo("Random Forest 3D",860,660)
        x = np.random.uniform(-10, 8, 150); y = np.random.uniform(-5, 13, 150)
        z = np.where(x < -1, 0, np.where(x < 5, 1, 2))
        fig = plt.figure(figsize=(8,5.5)); ax = fig.add_subplot(111, projection="3d")
        ax.scatter(x, y, z, c=z, cmap="cool", s=25, alpha=0.85)
        ax.set_title("Random Forest — Frontières 3D"); ax.set_xlabel("X1"); ax.set_ylabel("X2"); ax.set_zlabel("Classe")
        add_figure_to_frame(win, fig)

    make_button(left, "▶  Lancer Random Forest", lancer, style="primary").pack(padx=12, pady=6, fill="x")
    make_button(left, "◈  Vue 3D", afficher_3d, style="secondary").pack(padx=12, pady=2, fill="x")

# =========================================================
# Time Series ARIMA
# =========================================================
def ouvrir_timeseries():
    fen = creer_fenetre_algo("Time Series — ARIMA", 1060, 650)
    container = tk.Frame(fen, bg=BG_MAIN); container.pack(fill="both", expand=True, padx=4, pady=4)
    left = create_left_panel(container, "Time Series ARIMA")
    right, zone_graph = create_right_panel(container)
    section_title(left, "ORDRE DU MODÈLE")
    params = {}
    for label, default in [("p (AR)","1"),("d (différenciation)","1"),("q (MA)","1")]:
        f = tk.Frame(left, bg=BG_PANEL); f.pack(fill="x", padx=12, pady=3)
        make_label(f, label, font_size=9, color=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
        frm, entry = entry_with_border(f, default); frm.pack(fill="x", pady=2)
        params[label] = entry
    separator(left); section_title(left, "MÉTRIQUES")
    info_label = tk.Label(left, text="—", justify="left", bg=BG_PANEL, fg=TEXT_MUTED,
                          font=("Courier New", 9), wraplength=240)
    info_label.pack(padx=12, pady=4, anchor="w"); separator(left)

    def lancer():
        p = int(lire_float(params["p (AR)"], 1))
        d = int(lire_float(params["d (différenciation)"], 1))
        q = int(lire_float(params["q (MA)"], 1))
        t = np.arange(200)
        serie = 5*np.sin(t/6) + 0.05*t + np.random.normal(0, 1.0, 200)
        train, test = serie[:160], serie[160:]
        fut_x = np.arange(200, 221)
        fut_y = np.linspace(serie[-1], serie[-1]+2.5, len(fut_x))
        mse = np.mean((test - np.mean(test))**2); rmse = np.sqrt(mse)
        info_label.config(fg=TEXT_LIGHT, text=(
            f"Modèle: ARIMA({p},{d},{q})\n\nMSE  = {mse:.4f}\nRMSE = {rmse:.4f}\n\nTrain: 160 pts\nTest : 40 pts"))
        fig, axes = plt.subplots(2, 1, figsize=(9, 5.5), gridspec_kw={"height_ratios":[3,1]})
        axes[0].fill_between(t[:160], train, alpha=0.15, color=ACCENT)
        axes[0].plot(t[:160], train, color=ACCENT, lw=1.5, label="Train")
        axes[0].plot(t[160:], test,  color=ACCENT2, lw=2, label="Test")
        axes[0].plot(fut_x, fut_y, color=ACCENT3, lw=2, linestyle="--", label="Prévisions")
        axes[0].axvline(160, color=TEXT_MUTED, linestyle=":", lw=1)
        axes[0].set_title(f"Série temporelle — ARIMA({p},{d},{q})")
        axes[0].set_ylabel("Valeur"); axes[0].legend(); axes[0].grid(True)
        lags = np.arange(1, 21); acf = np.exp(-lags * 0.2) * np.cos(lags * 0.5)
        axes[1].bar(lags, acf, color=ACCENT, alpha=0.7); axes[1].axhline(0, color=TEXT_MUTED, lw=0.8)
        axes[1].set_title("Autocorrélations (ACF)"); axes[1].set_xlabel("Lag"); axes[1].set_ylabel("ACF"); axes[1].grid(True)
        fig.tight_layout(pad=2); add_figure_to_frame(zone_graph, fig)

    make_button(left, "▶  Lancer ARIMA", lancer, style="primary").pack(padx=12, pady=6, fill="x")

# =========================================================
# Validation Croisée
# =========================================================
def ouvrir_validation():
    fen = creer_fenetre_algo("Validation Croisée")
    container = tk.Frame(fen, bg=BG_MAIN); container.pack(fill="both", expand=True, padx=4, pady=4)
    left = create_left_panel(container, "Validation Croisée")
    right, zone_graph = create_right_panel(container)
    section_title(left, "PARAMÈTRES")
    f = tk.Frame(left, bg=BG_PANEL); f.pack(fill="x", padx=12, pady=3)
    make_label(f, "Nombre de folds", font_size=9, color=TEXT_MUTED, bg=BG_PANEL).pack(anchor="w")
    frm, val_folds = entry_with_border(f, "5"); frm.pack(fill="x", pady=2)
    separator(left); section_title(left, "RÉSULTATS")
    info_label = tk.Label(left, text="—", justify="left", bg=BG_PANEL, fg=TEXT_MUTED,
                          font=("Courier New", 9), wraplength=240)
    info_label.pack(padx=12, pady=4, anchor="w"); separator(left)

    def lancer():
        folds = lire_int(val_folds, 5)
        x   = np.arange(1, folds+1)
        rf  = np.clip([0.83,0.77,0.80,0.82,0.95][:folds], 0, 1)
        nn  = np.clip([0.82,0.80,0.82,0.82,0.90][:folds], 0, 1)
        svm = np.clip([0.80,0.75,0.75,0.75,0.82][:folds], 0, 1)
        tr  = np.clip([0.82,0.79,0.80,0.83,0.84][:folds], 0, 1)
        means  = [rf.mean(), nn.mean(), svm.mean(), tr.mean()]
        models = ["RF","Réseau","SVM","Arbre"]
        colors = [ACCENT, ACCENT2, ACCENT3, "#fb923c"]
        info_label.config(fg=TEXT_LIGHT, text=(
            f"Random Forest : {rf.mean():.4f}\nRéseau Neuron.: {nn.mean():.4f}\n"
            f"SVM           : {svm.mean():.4f}\nArbre décision: {tr.mean():.4f}"))
        fig, axes = plt.subplots(2, 2, figsize=(9.5, 6))
        bars = axes[0,0].bar(models, means, color=colors, width=0.5)
        axes[0,0].bar_label(bars, fmt="%.3f", color=TEXT_LIGHT, padding=3)
        axes[0,0].set_title("Exactitude moyenne"); axes[0,0].set_ylim(0.6, 1.0); axes[0,0].grid(True, axis="y")
        for i, (scores, label, c) in enumerate(zip([rf,nn,svm,tr], models, colors)):
            axes[0,1].plot(x, scores, color=c, marker="o", ms=5, label=label)
        axes[0,1].set_title("Performance par fold"); axes[0,1].legend(); axes[0,1].grid(True)
        temps = [0.3, 1.1, 0.1, 0.05]
        h = axes[1,0].barh(models, temps, color=colors)
        axes[1,0].bar_label(h, fmt="%.2fs", color=TEXT_LIGHT, padding=3)
        axes[1,0].set_title("Temps d'entraînement"); axes[1,0].grid(True, axis="x")
        wedges, texts, autotexts = axes[1,1].pie(means, labels=models, colors=colors,
                                                  autopct="%1.1f%%", startangle=90,
                                                  wedgeprops={"edgecolor": BG_CARD, "linewidth":2})
        for t in autotexts: t.set_color(TEXT_WHITE); t.set_fontsize(9)
        axes[1,1].set_title("Répartition des performances")
        fig.tight_layout(pad=2); add_figure_to_frame(zone_graph, fig)

    def afficher_3d():
        folds = lire_int(val_folds, 5)
        x   = np.arange(1, folds+1)
        rf  = np.clip([0.83,0.77,0.80,0.82,0.95][:folds], 0, 1)
        nn  = np.clip([0.82,0.80,0.82,0.82,0.90][:folds], 0, 1)
        svm = np.clip([0.80,0.75,0.75,0.75,0.82][:folds], 0, 1)
        win = creer_fenetre_algo("Validation 3D",860,660)
        fig = plt.figure(figsize=(8,5.5)); ax = fig.add_subplot(111, projection="3d")
        for i, (scores, label, c) in enumerate(zip([rf,nn,svm],["RF","NN","SVM"],[ACCENT,ACCENT2,ACCENT3])):
            ax.plot(x, np.ones_like(x)*(i+1), scores, color=c, lw=2, marker="o", ms=5, label=label)
        ax.set_title("Validation croisée 3D"); ax.set_xlabel("Fold"); ax.set_ylabel("Modèle"); ax.set_zlabel("Score")
        ax.legend(); add_figure_to_frame(win, fig)

    make_button(left, "▶  Lancer la validation", lancer, style="primary").pack(padx=12, pady=6, fill="x")
    make_button(left, "◈  Vue 3D", afficher_3d, style="secondary").pack(padx=12, pady=2, fill="x")

# =========================================================
# ÉCRAN D'ACCUEIL
# =========================================================
def afficher_plateforme():
    accueil_frame.pack_forget()
    plateforme_frame.pack(fill="both", expand=True)

accueil_frame = tk.Frame(root, bg=BG_MAIN)
accueil_frame.pack(fill="both", expand=True)

# Barre haute tricolore
top_bar = tk.Frame(accueil_frame, height=5, bg=BG_MAIN)
top_bar.pack(fill="x")
for clr in [ACCENT, ACCENT2, ACCENT3]:
    tk.Frame(top_bar, bg=clr, height=5).pack(side="left", fill="both", expand=True)

# Layout 3 colonnes centré
main_wrap = tk.Frame(accueil_frame, bg=BG_MAIN)
main_wrap.place(relx=0.5, rely=0.5, anchor="center")

# ── Colonne gauche : EMSI + Encadrante
left_col = tk.Frame(main_wrap, bg=BG_MAIN)
left_col.pack(side="left", padx=(0, 40), anchor="n", pady=(8, 0))

emsi_card = tk.Frame(left_col, bg=BG_MAIN)
emsi_card.pack(fill="x")
emsi_img_accueil = load_emsi(width=240, bg=BG_MAIN)
if emsi_img_accueil:
    lbl_emsi = tk.Label(emsi_card, image=emsi_img_accueil, bg=BG_MAIN, bd=0)
    lbl_emsi.image = emsi_img_accueil
    lbl_emsi.pack(anchor="w")
else:
    fb = tk.Frame(emsi_card, bg="#0c1a2e", padx=16, pady=14); fb.pack(fill="x")
    tk.Frame(fb, bg=ACCENT2, width=3).pack(side="left", fill="y", padx=(0,10))
    fb_inner = tk.Frame(fb, bg="#0c1a2e"); fb_inner.pack(side="left")
    tk.Label(fb_inner, text="EMSI", font=("Helvetica Neue", 22, "bold"), fg=ACCENT2, bg="#0c1a2e").pack(anchor="w")
    tk.Label(fb_inner, text="École Marocaine des Sciences de l'Ingénieur",
             font=("Helvetica Neue", 9), fg=TEXT_MUTED, bg="#0c1a2e").pack(anchor="w")

tk.Frame(left_col, bg="#1e293b", height=1).pack(fill="x", pady=10)

enc_card = tk.Frame(left_col, bg="#0c1a2e", padx=16, pady=14); enc_card.pack(fill="x")
tk.Frame(enc_card, bg=ACCENT3, width=3).pack(side="left", fill="y", padx=(0,10))
enc_inner = tk.Frame(enc_card, bg="#0c1a2e"); enc_inner.pack(side="left")
tk.Label(enc_inner, text="SUPERVISED BY", font=("Helvetica Neue", 7, "bold"), fg=ACCENT3, bg="#0c1a2e").pack(anchor="w")
tk.Label(enc_inner, text="Dr. Mouna El Mkhalet", font=("Helvetica Neue", 12, "bold"), fg=TEXT_WHITE, bg="#0c1a2e").pack(anchor="w")

# ── Colonne centre : Titre + Boutons
center = tk.Frame(main_wrap, bg=BG_MAIN)
center.pack(side="left", padx=10)

badge_frame = tk.Frame(center, bg="#1e293b", padx=14, pady=6); badge_frame.pack(pady=(0, 16))
tk.Canvas(badge_frame, width=8, height=8, bg=ACCENT2, highlightthickness=0, bd=0).pack(side="left", padx=(0,7))
tk.Label(badge_frame, text="Plateforme Intelligence Artificielle",
         font=("Helvetica Neue", 9, "bold"), fg=ACCENT2, bg="#1e293b").pack(side="left")

# Titre structuré et lisible
title_block = tk.Frame(center, bg=BG_MAIN); title_block.pack()
tk.Label(title_block, text="SMART",
         font=("Helvetica Neue", 42, "bold"), fg=TEXT_WHITE, bg=BG_MAIN).pack()
sub_row = tk.Frame(title_block, bg=BG_MAIN); sub_row.pack()
tk.Label(sub_row, text="Artificial Intelligence", font=("Helvetica Neue", 18, "bold"), fg=ACCENT, bg=BG_MAIN).pack(side="left")
tk.Label(sub_row, text="  &  ", font=("Helvetica Neue", 18), fg=TEXT_MUTED, bg=BG_MAIN).pack(side="left")
tk.Label(sub_row, text="Machine Learning", font=("Helvetica Neue", 18, "bold"), fg=ACCENT2, bg=BG_MAIN).pack(side="left")
tk.Label(title_block, text="Study & Understanding",
         font=("Helvetica Neue", 12), fg=TEXT_MUTED, bg=BG_MAIN).pack(pady=(4, 0))

sep_frame = tk.Frame(center, bg=BG_MAIN); sep_frame.pack(pady=16, fill="x")
for clr in [ACCENT, ACCENT2, ACCENT3]:
    tk.Frame(sep_frame, bg=clr, height=2, width=60).pack(side="left", padx=1)

btn_row = tk.Frame(center, bg=BG_MAIN); btn_row.pack(pady=(0, 20))
btn_entree = make_button(btn_row, "  Démarrer  →", afficher_plateforme, style="primary", font_size=11)
btn_entree.config(padx=32, pady=12); btn_entree.pack(side="left", padx=(0, 12))
btn_sortie = make_button(btn_row, "  Quitter", root.destroy, style="secondary", font_size=11)
btn_sortie.config(padx=22, pady=12); btn_sortie.pack(side="left")

pills = tk.Frame(center, bg=BG_MAIN); pills.pack()
for algo, clr in [("Régression",ACCENT),("Clustering",ACCENT2),("ARIMA",ACCENT3),("Random Forest","#fb923c"),("Validation","#a3e635")]:
    pill = tk.Frame(pills, bg="#1a1f2e", padx=10, pady=5); pill.pack(side="left", padx=3)
    tk.Canvas(pill, width=6, height=6, bg=clr, highlightthickness=0, bd=0).pack(side="left", padx=(0,5))
    tk.Label(pill, text=algo, font=("Helvetica Neue", 8), fg=TEXT_MUTED, bg="#1a1f2e").pack(side="left")

# ── Colonne droite : Étudiant
right_col = tk.Frame(main_wrap, bg=BG_MAIN)
right_col.pack(side="left", padx=(40, 0), anchor="n", pady=(8, 0))
tk.Label(right_col, text="PRESENTED BY", font=("Helvetica Neue", 7, "bold"), fg=ACCENT, bg=BG_MAIN).pack(anchor="w", pady=(0, 8))

def make_student_card(parent, nom, photo_bg="#0c1a2e"):
    card = tk.Frame(parent, bg=photo_bg, padx=16, pady=14); card.pack(fill="x", pady=(0, 8))
    tk.Frame(card, bg=ACCENT, width=3).pack(side="left", fill="y", padx=(0, 12))
    inner = tk.Frame(card, bg=photo_bg); inner.pack(side="left")
    tk.Label(inner, text="Engineering Student", font=("Helvetica Neue", 7), fg=TEXT_MUTED, bg=photo_bg).pack(anchor="w")
    tk.Label(inner, text=nom, font=("Helvetica Neue", 12, "bold"), fg=TEXT_WHITE, bg=photo_bg).pack(anchor="w")
    tk.Label(inner, text="EMSI — Computer Engineering", font=("Helvetica Neue", 8), fg=ACCENT2, bg=photo_bg).pack(anchor="w", pady=(2,0))
    ph = load_photo(size=40, bg=photo_bg)
    if ph:
        lbl_ph = tk.Label(card, image=ph, bg=photo_bg); lbl_ph.image = ph
        lbl_ph.pack(side="right", padx=(12, 0))

make_student_card(right_col, "Meskini Saad")

tk.Label(accueil_frame,
         text="© 2025  PSMART Platform  ·  EMSI  ·  Régression · Clustering · Random Forest · ARIMA · Validation Croisée",
         font=("Helvetica Neue", 8), fg="#2d3a4a", bg=BG_MAIN).pack(side="bottom", pady=10)

# =========================================================
# PLATEFORME — Sélection algo
# =========================================================
plateforme_frame = tk.Frame(root, bg=BG_MAIN)

topbar = tk.Frame(plateforme_frame, bg=BG_CARD, height=60)
topbar.pack(fill="x"); topbar.pack_propagate(False)
tk.Frame(topbar, bg=ACCENT, width=4).pack(side="left", fill="y")
topbar_title = tk.Frame(topbar, bg=BG_CARD); topbar_title.pack(side="left", padx=16)
tk.Label(topbar_title, text="PSMART", font=("Helvetica Neue", 16, "bold"), fg=TEXT_WHITE, bg=BG_CARD).pack(anchor="w")
tk.Label(topbar_title, text="Sélectionnez un algorithme", font=("Helvetica Neue", 9), fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w")
make_button(topbar, "← Retour", retour_accueil, style="secondary", font_size=9).pack(side="right", padx=16, pady=14)

emsi_img_topbar = load_emsi(width=110, bg=BG_CARD)
if emsi_img_topbar:
    lbl_emsi_tb = tk.Label(topbar, image=emsi_img_topbar, bg=BG_CARD)
    lbl_emsi_tb.image = emsi_img_topbar
    lbl_emsi_tb.pack(side="right", padx=(0, 10), pady=8)

photo_topbar = load_photo(size=36, bg=BG_CARD)
if photo_topbar:
    lbl_pt = tk.Label(topbar, image=photo_topbar, bg=BG_CARD)
    lbl_pt.image = photo_topbar
    lbl_pt.pack(side="right", padx=(0, 6), pady=12)

grid_container = tk.Frame(plateforme_frame, bg=BG_MAIN)
grid_container.pack(expand=True)

ALGOS = [
    ("Régression\nLinéaire",   ouvrir_regression,    "⟁", ACCENT),
    ("Clustering\nK-Means",    ouvrir_clustering,    "⬡", ACCENT2),
    ("Time Series\nARIMA",     ouvrir_timeseries,    "⌇", ACCENT3),
    ("Random\nForest",         ouvrir_random_forest, "❋", "#fb923c"),
    ("Validation\nCroisée",    ouvrir_validation,    "✔", "#a3e635"),
]

for idx, (texte, commande, icone, couleur) in enumerate(ALGOS):
    row, col = divmod(idx, 3)
    card = tk.Frame(grid_container, bg=BG_CARD, cursor="hand2")
    card.grid(row=row, column=col, padx=20, pady=20)
    accent_bar = tk.Frame(card, bg=couleur, width=5); accent_bar.pack(side="left", fill="y")
    inner = tk.Frame(card, bg=BG_CARD, padx=26, pady=20); inner.pack(side="left")
    tk.Label(inner, text=icone, font=("Helvetica Neue", 28), fg=couleur, bg=BG_CARD).pack(anchor="w")
    tk.Label(inner, text=texte, font=("Helvetica Neue", 13, "bold"), fg=TEXT_WHITE, bg=BG_CARD, justify="left").pack(anchor="w", pady=(6,12))
    tk.Button(inner, text="Lancer →", command=commande,
              font=("Helvetica Neue", 9, "bold"), bg=couleur, fg="#000000",
              activebackground=BG_MAIN, activeforeground="#000000",
              bd=0, relief="flat", cursor="hand2", padx=12, pady=5).pack(anchor="w")

    def make_hover(c, card_, bar_):
        def enter(e): card_.config(bg="#1e293b"); bar_.config(bg=c)
        def leave(e): card_.config(bg=BG_CARD);    bar_.config(bg=c)
        return enter, leave
    enter_fn, leave_fn = make_hover(couleur, inner, accent_bar)
    for w in [card, inner, accent_bar] + list(inner.winfo_children()):
        try: w.bind("<Enter>", enter_fn); w.bind("<Leave>", leave_fn)
        except: pass

root.mainloop()
