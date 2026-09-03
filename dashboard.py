import tkinter as tk
from tkinter import ttk

class CLiPDashboard:
    def __init__(self, on_close_callback=None):
        self.root = tk.Tk()
        self.root.title("CLiP MVP")
        self.root.geometry("300x310")
        self.root.attributes('-topmost', True)
        self.on_close = on_close_callback
        
        self.score_label = tk.Label(
            self.root, 
            text="--", 
            font=("Helvetica", 64, "bold")
        )
        self.score_label.pack(pady=10)
        
        self.status_label = tk.Label(
            self.root, 
            text="Calibrating...", 
            font=("Helvetica", 14)
        )
        self.status_label.pack()
        
        self.breakdown_frame = tk.Frame(self.root)
        self.breakdown_frame.pack(pady=10)
        
        self.breakdown_labels = {}
        for metric in ['typing', 'backspace', 'pause', 'mouse']:
            lbl = tk.Label(self.breakdown_frame, text=f"{metric}: --", font=("Courier", 10))
            lbl.pack(anchor="w")
            self.breakdown_labels[metric] = lbl
        
        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="History", command=self.show_history).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="Export", command=self.export_data).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="Upload", command=self.upload_data).pack(side=tk.LEFT, padx=3)
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def update(self, score, interpretation, color, breakdown, features):
        self.score_label.config(text=str(score), fg=color)
        self.status_label.config(text=interpretation)
        for metric, val in breakdown.items():
            self.breakdown_labels[metric].config(
                text=f"{metric:10s}: +{val:.1f}"
            )
    
    def show_history(self):
        hist_win = tk.Toplevel(self.root)
        hist_win.title("CLiP History")
        hist_win.geometry("400x300")
        text = tk.Text(hist_win, wrap=tk.WORD)
        text.pack(expand=True, fill=tk.BOTH)
        try:
            from database import Database
            db = Database()
            rows = db.get_history(limit=50)
            for row in rows:
                ts, score, interp, _, _ = row
                text.insert(tk.END, f"{ts}  |  Score: {score}  |  {interp}\n")
        except Exception as e:
            text.insert(tk.END, f"Error loading history: {e}")
        text.config(state=tk.DISABLED)
    
    def export_data(self):
        from export import export_data
        filepath = export_data()
        if filepath:
            import tkinter.messagebox as msg
            msg.showinfo("Export Complete", f"Data exported!\n\nFile: {filepath}")
    
    def upload_data(self):
        """Send data directly to researcher server."""
        import tkinter.messagebox as msg
        from upload import upload_data
        
        confirm = msg.askyesno(
            "Upload Data",
            "This will send your anonymized data to the researcher.\n\n"
            "No personal content is included — only timing scores.\n\n"
            "Proceed?"
        )
        if not confirm:
            return
        
        ok, message = upload_data()
        if ok:
            msg.showinfo("Upload Successful", message)
        else:
            msg.showerror("Upload Failed", message)
    
    def _on_close(self):
        if self.on_close:
            self.on_close()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()