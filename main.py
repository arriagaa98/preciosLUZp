import os
import requests
from datetime import datetime, timedelta
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedTk
from tkcalendar import DateEntry
import requests
from tqdm import tqdm

def download_file(url, folder, filename, progress_bar):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        os.makedirs(folder, exist_ok=True)
        total_size = int(response.headers.get('content-length', 0))
        with open(f"{folder}/{filename}", "wb") as f:
            downloaded_size = 0
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
                downloaded_size += len(chunk)
                progress_bar['value'] = downloaded_size
                progress_bar.update()
        
        progress_bar['value'] = 0
        progress_bar.update()
    else:
        print(f"File {filename} not found")

def read_file(folder, filename):
    with open(f"{folder}/{filename}", "r") as f:
        content = f.read()
    return content

def get_period(hour, weekday, holiday):
    if weekday < 5 and not holiday:
        if 11 <= hour <= 14 or 19 <= hour <= 22:
            period = 'p1'
        elif 9 <= hour <= 10 or 15 <= hour <= 18 or 23 <= hour <= 24:
            period = 'p2'
        else:
            period = 'p3'
    else:
        period = 'p3'
    return period

def process_data(content, bank_holidays):
    data = []
    lines = content.split("\n")
    for line in lines[1:-2]:
        items = line.split(";")
        year, month, day, hour, _, price = items[:6]
        date = f"{year}-{month}-{day}"
        weekday = datetime.strptime(date, "%Y-%m-%d").weekday()
        holiday = f"{month}-{day}" in bank_holidays
        period = get_period(int(hour), weekday, holiday)
        data.append([year, month, day, hour, float(price), period])
    return data

def download_and_process_data(start_date, end_date, bank_holidays, progress_bar):
    date = start_date
    all_data = []
    total_days = (end_date - start_date).days +1
    days_downloaded = 0

    while date <= end_date:
        folder = f"{date.year}_{date.month:02d}"
        filename = f"marginalpdbc_{date.strftime('%Y%m%d')}.1"
        file_path = f"{folder}/{filename}"
        
        if not os.path.exists(file_path):
            url = f"https://www.omie.es/es/file-download?parents%5B0%5D=marginalpdbc&filename={filename}"
            download_file(url, folder, filename, progress_bar)

        content = read_file(folder, filename)
        data = process_data(content, bank_holidays)
        all_data.extend(data)
        date += timedelta(days=1)

        days_downloaded += 1
        progress_percentage = (days_downloaded / total_days) * 100
        progress_bar['value'] = progress_percentage
        progress_label['text'] = f"Descargando datos desde OMIE: {progress_percentage:.2f}%"
        root.update_idletasks()

    progress_bar['value'] = 100
    progress_label['text'] = "Descargando datos desde OMIE: 100%"
    return all_data

def save_to_excel(data, file_path):
    df = pd.DataFrame(data, columns=['year', 'month', 'day', 'hour', 'price', 'period'])
    df.to_excel(file_path, index=False)

def main():
    bank_holidays = ['01-06', '05-01', '08-15', '10-12', '11-01', '12-06', '12-08', '12-25']
    file_path = 'OMIE_data.xlsx'

    start_date_str = input('Enter the start date (YYYY-MM-DD): ')
    end_date_str = input('Enter the end date   (YYYY-MM-DD): ')

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    data = download_and_process_data(start_date, end_date, bank_holidays, progress_bar)
    save_to_excel(data, file_path)

    df = pd.DataFrame
    df = pd.DataFrame(data, columns=['year', 'month', 'day', 'hour', 'price', 'period'])

    # Filter rows by period
    p1_df = df[df['period'] == 'p1']
    p2_df = df[df['period'] == 'p2']
    p3_df = df[df['period'] == 'p3']

    # Calculate average price for each period
    p1_avg_price = p1_df['price'].mean() / 1000
    p2_avg_price = p2_df['price'].mean() / 1000
    p3_avg_price = p3_df['price'].mean() / 1000

    # Print the results
    print(f'Precio medio para p1: {p1_avg_price:.6f} €/KWh')
    print(f'Precio medio para p2: {p2_avg_price:.6f} €/KWh')
    print(f'Precio medio para p3: {p3_avg_price:.6f} €/KWh')

    # Calculate average price for each period with comission
    p1_avg_price_cm = p1_df['price'].mean() / 1000 + 0.005 + 0.029098 + 0.043893
    p2_avg_price_cm = p2_df['price'].mean() / 1000 + 0.005 + 0.019794 + 0.008779
    p3_avg_price_cm = p3_df['price'].mean() / 1000 + 0.005 + 0.000980 + 0.002195

    # Print the results with comisison
    print(f'Precio medio con comisones para p1: {p1_avg_price_cm:.6f} €/KWh')
    print(f'Precio medio con comisones para p2: {p2_avg_price_cm:.6f} €/KWh')
    print(f'Precio medio con comisones para p3: {p3_avg_price_cm:.6f} €/KWh')
    
def on_submit():
    bank_holidays = ['01-06', '05-01', '08-15', '10-12', '11-01', '12-06', '12-08', '12-25']
    file_path = 'OMIE_data.xlsx'

    start_date_str = start_date_entry.get()
    end_date_str = end_date_entry.get()

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    data = download_and_process_data(start_date, end_date, bank_holidays, progress_bar)
    save_to_excel(data, file_path)

    df = pd.DataFrame(data, columns=['year', 'month', 'day', 'hour', 'price', 'period'])

    # Filter rows by period
    p1_df = df[df['period'] == 'p1']
    p2_df = df[df['period'] == 'p2']
    p3_df = df[df['period'] == 'p3']

    # Calculate average price for each period and convert to €/KWh
    p1_avg_price = p1_df['price'].mean() / 1000
    p2_avg_price = p2_df['price'].mean() / 1000
    p3_avg_price = p3_df['price'].mean() / 1000

    # Set the results
    p1_result_var.set(f'Precio medio para p1: {p1_avg_price:.6f} €/KWh')
    p2_result_var.set(f'Precio medio para p2: {p2_avg_price:.6f} €/KWh')
    p3_result_var.set(f'Precio medio para p3: {p3_avg_price:.6f} €/KWh')

    # Calculate average price for each period with comission
    p1_avg_price_cm = p1_df['price'].mean() / 1000 + 0.005 + 0.029098 + 0.043893
    p2_avg_price_cm = p2_df['price'].mean() / 1000 + 0.005 + 0.019794 + 0.008779
    p3_avg_price_cm = p3_df['price'].mean() / 1000 + 0.005 + 0.000980 + 0.002195

    # Set the results with commissions
    p1_result_cm_var.set(f'Precio medio con comisones para p1: {p1_avg_price_cm:.6f} €/KWh')
    p2_result_cm_var.set(f'Precio medio con comisones para p2: {p2_avg_price_cm:.6f} €/KWh')
    p3_result_cm_var.set(f'Precio medio con comisones para p3: {p3_avg_price_cm:.6f} €/KWh')

    # Call the second window
    open_second_window(p1_avg_price_cm, p2_avg_price_cm, p3_avg_price_cm)

def open_second_window(p1_avg_price_cm, p2_avg_price_cm, p3_avg_price_cm):
    #second_window = tk.Toplevel(root)
    #second_window.title("Consumo de energia y previsión de factura")
    #second_window.geometry("500x500")

    frame2 = ttk.Frame(root, padding=(10, 10, 10, 10))
    frame2.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))


    # Input fields and labels for total kWh and percentages
    ttk.Label(frame2, text="Consumo de red en p1 (kWh):").grid(row=1, column=0, sticky=tk.W)
    p1_percentage_entry = ttk.Entry(frame2)
    p1_percentage_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame2, text="Consumo de red en p2 (kWh):").grid(row=2, column=0, sticky=tk.W)
    p2_percentage_entry = ttk.Entry(frame2)
    p2_percentage_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame2, text="Consumo de red en p3 (kWh):").grid(row=3, column=0, sticky=tk.W)
    p3_percentage_entry = ttk.Entry(frame2)
    p3_percentage_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

    # extra
    ttk.Label(frame2, text="Energia solar injectada (kWh):").grid(row=4, column=0, sticky=tk.W)
    solar_kwh_entry = ttk.Entry(frame2)
    solar_kwh_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))

    # Submit button
    submit_button = ttk.Button(frame2, text="Calcular gasto energia", command=lambda: calculate_final_bill(p1_avg_price_cm, p2_avg_price_cm, p3_avg_price_cm, p1_percentage_entry, p2_percentage_entry, p3_percentage_entry, solar_kwh_entry, final_price_var, solar_deduction_var, final_price_deducted_var))
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Solar deduction label
    solar_deduction_var = tk.StringVar()
    ttk.Label(frame2, textvariable=solar_deduction_var).grid(row=7, column=0, columnspan=2)

    # Final price labels
    final_price_var = tk.StringVar()
    ttk.Label(frame2, textvariable=final_price_var).grid(row=6, column=0, columnspan=2)

    final_price_deducted_var = tk.StringVar()
    ttk.Label(frame2, textvariable=final_price_deducted_var).grid(row=8, column=0, columnspan=2)


def calculate_final_bill(p1_avg_price_cm, p2_avg_price_cm, p3_avg_price_cm, p1_percentage_entry, p2_percentage_entry, p3_percentage_entry, solar_kwh_entry, final_price_var, solar_deduction_var, final_price_deducted_var):

    p1_percentage = float(p1_percentage_entry.get()) 
    p2_percentage = float(p2_percentage_entry.get())
    p3_percentage = float(p3_percentage_entry.get())
    solar_kwh = float(solar_kwh_entry.get())

    # Calculate the final bill price
    final_price = (p1_avg_price_cm * p1_percentage) + (p2_avg_price_cm * p2_percentage) + (p3_avg_price_cm * p3_percentage)
    final_price_var.set(f'Precio de la energia consumida de red: {final_price:.4f} €')

    # Calculate the final price with solar deduction (no taxes)
    solar_deduction = solar_kwh * 0.11
    solar_deduction_var.set(f'Injección a red: {solar_deduction:.4f} €')
    final_price_deducted = final_price - solar_deduction
    final_price_deducted_var.set(f'Precio Descontado (consumo - excedentes): {final_price_deducted:.4f} €')


root = ThemedTk(theme="yaru")
root.title("preciosLUZp - Precios de la luz")
root.geometry("1000x500")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

start_date_label = ttk.Label(frame, text="Fecha de inicio (YYYY-MM-DD):")
start_date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

end_date_label = ttk.Label(frame, text="Fecha de fin (YYYY-MM-DD):")
end_date_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

start_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
start_date_entry.grid(row=0, column=1, padx=5, pady=5)

end_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
end_date_entry.grid(row=1, column=1, padx=5, pady=5)

submit_button = ttk.Button(frame, text="Calcular precios €/kWh", command=on_submit)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

progress_label = tk.Label(root, text="Descargando datos desde OMIE")
progress_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))
progress_bar = ttk.Progressbar(frame, orient='horizontal', mode='determinate', length=200)
progress_bar.grid(row=4, column=0, pady=10, padx=10)

p1_result_var = tk.StringVar()
p1_result_label = ttk.Label(frame, textvariable=p1_result_var)
p1_result_label.grid(row=5, column=0, columnspan=2, pady=2)
p2_result_var = tk.StringVar()
p2_result_label = ttk.Label(frame, textvariable=p2_result_var)
p2_result_label.grid(row=6, column=0, columnspan=2, pady=2)
p3_result_var = tk.StringVar()
p3_result_label = ttk.Label(frame, textvariable=p3_result_var)
p3_result_label.grid(row=7, column=0, columnspan=2, pady=2)

p1_result_cm_var = tk.StringVar()
p1_result_cm_label = ttk.Label(frame, textvariable=p1_result_cm_var)
p1_result_cm_label.grid(row=9, column=0, columnspan=2, pady=2)
p2_result_cm_var = tk.StringVar()
p2_result_cm_label = ttk.Label(frame, textvariable=p2_result_cm_var)
p2_result_cm_label.grid(row=10, column=0, columnspan=2, pady=2)
p3_result_cm_var = tk.StringVar()
p3_result_cm_label = ttk.Label(frame, textvariable=p3_result_cm_var)
p3_result_cm_label.grid(row=11, column=0, columnspan=2, pady=2)


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

if __name__ == '__main__':
    root.mainloop()