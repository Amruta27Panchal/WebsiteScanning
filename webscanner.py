import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def validate_url(url):
    """Validate if the URL is reachable."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        messagebox.showerror("Error", f"Unable to reach the URL: {e}")
        return False

def test_sql_injection(url):
    """Basic SQL Injection Test."""
    payloads = ["' OR '1'='1", "' OR '1'='2"]
    vulnerabilities = []
    for payload in payloads:
        test_url = f"{url}?id={payload}"
        try:
            response = requests.get(test_url)
            if "syntax error" in response.text or "SQL" in response.text:
                vulnerabilities.append(f"SQL Injection detected with payload: {payload}")
        except Exception as e:
            vulnerabilities.append(f"Error testing SQL Injection: {e}")
    return vulnerabilities

def test_xss(url):
    """Basic XSS Test."""
    payload = "<script>alert('XSS')</script>"
    try:
        response = requests.post(url, data={"input": payload})
        if payload in response.text:
            return ["XSS vulnerability detected!"]
        else:
            return []
    except Exception as e:
        return [f"Error testing XSS: {e}"]

def scan_vulnerabilities():
    """Perform vulnerability scan and update the dashboard."""
    url = url_entry.get()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url  # Ensure the URL starts with http:// or https://

    if not validate_url(url):
        return

    sql_results = test_sql_injection(url)
    xss_results = test_xss(url)

    # Clear previous results
    result_text.delete(1.0, tk.END)
    for widget in dashboard_frame.winfo_children():
        widget.destroy()

    vulnerabilities = len(sql_results) + len(xss_results)
    if vulnerabilities:
        result_text.insert(tk.END, "Vulnerabilities Found:\n")
        for result in sql_results + xss_results:
            result_text.insert(tk.END, f"- {result}\n")
    else:
        result_text.insert(tk.END, "No vulnerabilities found!\n")
    
    # Create analytical dashboard
    labels = ['Vulnerabilities', 'Safe']
    sizes = [vulnerabilities, 2 - vulnerabilities]
    colors = ['red', 'green']
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.axis('equal')  # Equal aspect ratio for a perfect circle

    # Embed the pie chart in the Tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=dashboard_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

# Build the UI
app = tk.Tk()
app.title("Website Vulnerability Scanner with Dashboard")

# Input Section
input_frame = ttk.Frame(app)
input_frame.pack(pady=10)
ttk.Label(input_frame, text="Enter Website URL:").grid(row=0, column=0, padx=5)
url_entry = ttk.Entry(input_frame, width=40)
url_entry.grid(row=0, column=1, padx=5)
scan_button = ttk.Button(input_frame, text="Scan", command=scan_vulnerabilities)
scan_button.grid(row=0, column=2, padx=5)

# Results Section
result_frame = ttk.Frame(app)
result_frame.pack(pady=10, fill=tk.BOTH, expand=True)
ttk.Label(result_frame, text="Scan Results:").pack(anchor="w", padx=10)
result_text = tk.Text(result_frame, height=10, wrap=tk.WORD)
result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Dashboard Section
dashboard_frame = ttk.LabelFrame(app, text="Analytical Dashboard")
dashboard_frame.pack(pady=10, fill=tk.BOTH, expand=True)

app.mainloop()

