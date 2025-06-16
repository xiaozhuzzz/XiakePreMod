import os
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def export_sheet(df, sheet_name, output_dir, file_format, encoding):
    df = df.dropna(how='all')  # 删除整行全空的行，保留部分空行
    if df.empty:
        return None
    # 过滤掉第一列为空的行（空字符串或NaN）
    df = df[df.iloc[:, 0].astype(str).str.strip() != '']
    if df.empty:
        return None
    # 防止文件名非法字符
    safe_sheet_name = re.sub(r'[\\/:*?"<>|]', '_', sheet_name)
    os.makedirs(output_dir, exist_ok=True)
    ext = 'txt' if file_format == 'txt' else 'csv'
    output_file = os.path.join(output_dir, f"{safe_sheet_name}.{ext}")
    df.to_csv(output_file, sep='\t', index=False, encoding=encoding)
    return output_file

def select_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:
        excel_path_var.set(file_path)
        load_sheets(file_path)

def load_sheets(file_path):
    try:
        sheets = pd.ExcelFile(file_path).sheet_names
        sheet_listbox.delete(0, tk.END)
        for sheet in sheets:
            sheet_listbox.insert(tk.END, sheet)
    except Exception as e:
        messagebox.showerror("错误", f"加载工作表失败: {e}")

def export_selected_sheet():
    excel_path = excel_path_var.get()
    if not excel_path:
        messagebox.showwarning("提示", "请选择Excel文件")
        return
    selected_sheet = sheet_listbox.get(tk.ACTIVE)
    if not selected_sheet:
        messagebox.showwarning("提示", "请选择要导出的工作表")
        return
    output_dir = filedialog.askdirectory()
    if not output_dir:
        return
    try:
        df = pd.read_excel(excel_path, sheet_name=selected_sheet)
        output_file = export_sheet(df, selected_sheet, output_dir, export_format_var.get(), encoding_var.get())
        if output_file:
            messagebox.showinfo("成功", f"导出成功:\n{output_file}")
        else:
            messagebox.showinfo("提示", "导出内容为空或全部被过滤")
    except Exception as e:
        messagebox.showerror("错误", f"导出失败: {e}")

def show_progress_window(title="导出进度"):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("400x100")
    win.resizable(False, False)
    label = tk.Label(win, text="准备导出...", font=("Arial", 12))
    label.pack(pady=30)
    return win, label

def export_all_sheets_from_file():
    excel_path = excel_path_var.get()
    if not excel_path:
        messagebox.showwarning("提示", "请选择Excel文件")
        return
    output_dir = filedialog.askdirectory()
    if not output_dir:
        return
    try:
        sheets = pd.ExcelFile(excel_path).sheet_names
        progress_win, progress_label = show_progress_window()
        total = len(sheets)
        for i, sheet in enumerate(sheets, start=1):
            progress_label.config(text=f"导出工作表: {sheet} ({i}/{total})")
            root.update()
            df = pd.read_excel(excel_path, sheet_name=sheet)
            export_sheet(df, sheet, output_dir, export_format_var.get(), encoding_var.get())
        progress_win.destroy()
        messagebox.showinfo("成功", f"已导出全部工作表到:\n{output_dir}")
    except Exception as e:
        messagebox.showerror("错误", f"导出失败: {e}")

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_path_var.set(directory)
        load_excel_files(directory)

def load_excel_files(directory):
    try:
        excel_files = [f for f in os.listdir(directory) if f.endswith(('.xlsx', '.xls'))]
        excel_listbox.delete(0, tk.END)
        for file in excel_files:
            excel_listbox.insert(tk.END, file)
    except Exception as e:
        messagebox.showerror("错误", f"加载Excel文件失败: {e}")

def export_all_sheets_from_directory():
    directory = directory_path_var.get()
    if not directory:
        messagebox.showwarning("提示", "请选择Excel文件目录")
        return
    output_dir = filedialog.askdirectory()
    if not output_dir:
        return
    try:
        excel_files = [f for f in os.listdir(directory) if f.endswith(('.xlsx', '.xls'))]
        total_files = len(excel_files)
        progress_win, progress_label = show_progress_window()
        for file_index, file in enumerate(excel_files, start=1):
            file_path = os.path.join(directory, file)
            sheets = pd.ExcelFile(file_path).sheet_names
            total_sheets = len(sheets)
            for sheet_index, sheet in enumerate(sheets, start=1):
                progress_label.config(text=f"文件 {file_index}/{total_files}: {file}\n导出工作表 {sheet_index}/{total_sheets}: {sheet}")
                root.update()
                df = pd.read_excel(file_path, sheet_name=sheet)
                export_sheet(df, sheet, output_dir, export_format_var.get(), encoding_var.get())
        progress_win.destroy()
        messagebox.showinfo("成功", f"已导出目录下所有Excel工作表到:\n{output_dir}")
    except Exception as e:
        messagebox.showerror("错误", f"导出失败: {e}")

# 主窗口和控件布局
root = tk.Tk()
root.title("Excel Sheet 批量导出工具")

excel_path_var = tk.StringVar()
tk.Label(root, text="Excel 文件:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=excel_path_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="浏览...", command=select_excel_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="工作表:").grid(row=1, column=0, padx=10, pady=10)
sheet_listbox = tk.Listbox(root, width=50, height=10)
sheet_listbox.grid(row=1, column=1, padx=10, pady=10)

export_format_var = tk.StringVar(value='txt')
tk.Label(root, text="导出格式:").grid(row=2, column=0, padx=10, pady=10)
frame1 = tk.Frame(root)
frame1.grid(row=2, column=1, sticky='w', padx=10)
tk.Radiobutton(frame1, text="TXT (制表符分隔)", variable=export_format_var, value='txt').pack(side='left')
tk.Radiobutton(frame1, text="CSV (制表符分隔)", variable=export_format_var, value='csv').pack(side='left')

encoding_var = tk.StringVar(value='utf-8')
tk.Label(root, text="编码:").grid(row=3, column=0, padx=10, pady=10)
encoding_options = ['utf-8', 'utf-8-sig', 'utf-16', 'utf-16le', 'utf-16be']
encoding_menu = tk.OptionMenu(root, encoding_var, *encoding_options)
encoding_menu.grid(row=3, column=1, sticky='w', padx=10, pady=10)

tk.Button(root, text="导出选中工作表", command=export_selected_sheet).grid(row=1, column=2, padx=10, pady=10)
tk.Button(root, text="导出文件全部工作表", command=export_all_sheets_from_file).grid(row=2, column=2, padx=10, pady=10)

directory_path_var = tk.StringVar()
tk.Label(root, text="Excel 目录:").grid(row=4, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=directory_path_var, width=50).grid(row=4, column=1, padx=10, pady=10)
tk.Button(root, text="浏览...", command=select_directory).grid(row=4, column=2, padx=10, pady=10)

tk.Label(root, text="Excel 文件列表:").grid(row=5, column=0, padx=10, pady=10)
excel_listbox = tk.Listbox(root, width=50, height=10)
excel_listbox.grid(row=5, column=1, padx=10, pady=10)

tk.Button(root, text="导出目录全部文件全部工作表", command=export_all_sheets_from_directory).grid(row=6, column=1, padx=10, pady=10)

root.mainloop()
