import tkinter as tk
from tkinter import ttk, messagebox
import os

CONSENT_MARKER = os.path.join(os.path.dirname(__file__), ".consent_given")

def has_consented():
    """Check if user already consented in a previous session."""
    return os.path.exists(CONSENT_MARKER)

def show_consent_form(on_result):
    """
    Display the informed consent dialog.
    on_result(True)  -> user agreed
    on_result(False) -> user declined
    """
    root = tk.Tk()
    root.title("CLiP — Informed Consent")
    root.geometry("520x580")
    root.resizable(False, False)
    root.configure(bg="white")
    
    # ========== HEADER ==========
    header = tk.Label(
        root,
        text="CLiP MVP — Participant Consent Form",
        font=("Helvetica", 15, "bold"),
        bg="white",
        fg="#1a1a1a"
    )
    header.pack(pady=(15, 5))
    
    subheader = tk.Label(
        root,
        text="Cognitive Load Intelligence Platform — Research Study",
        font=("Helvetica", 10),
        bg="white",
        fg="#555555"
    )
    subheader.pack(pady=(0, 10))
    
    # ========== SCROLLABLE TEXT AREA ==========
    frame = tk.Frame(root, bg="white")
    frame.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
    
    text_widget = tk.Text(
        frame,
        wrap=tk.WORD,
        font=("Helvetica", 10),
        height=20,
        padx=10,
        pady=10,
        relief=tk.FLAT,
        bg="#f9f9f9",
        fg="#222222"
    )
    scrollbar = ttk.Scrollbar(frame, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    consent_body = """
1. STUDY PURPOSE
   You are invited to participate in a research study that measures the cognitive cost of computer-based work using behavioral signals from your keyboard and mouse. The goal is to understand how mentally demanding different tasks and tools feel, without interrupting your natural workflow.

2. WHAT DATA IS COLLECTED
   The app captures the following metadata ONLY:
   • Timing between keystrokes (how fast or slow you type)
   • Frequency of backspace / delete key presses
   • Duration of pauses between input events
   • Frequency of mouse clicks
   • A computed "Cognitive Load Index" score (0–10) derived from the above

   All data is stored locally on your computer in a file named clip_data.db.
   No data is transmitted to any remote server or cloud service.

3. WHAT IS NEVER COLLECTED
   The app does NOT and will NEVER record:
   • The actual characters, words, or content you type
   • Passwords, emails, code, messages, or documents
   • Screenshots, screen recordings, or video
   • Browser history, URLs, or visited websites
   • File names, folder names, or application content
   • Audio, camera, or microphone access
   • Your identity, name, or contact information

4. HOW LONG DATA IS KEPT
   Data remains on your local machine only. You may delete it at any time by removing the clip_data.db file in this folder. If you choose to share exported data with the research team, it will be anonymized and used solely for research and publication purposes.

5. RISKS AND BENEFITS
   Risks: Minimal. The app runs passively in the background and does not interfere with your work. The only risk is minor distraction from occasional pop-up surveys (if enabled).
   Benefits: You receive a personalized, real-time cognitive load dashboard. You may gain insight into when you are most productive or most fatigued.

6. VOLUNTARY PARTICIPATION
   Your participation is entirely voluntary. You may:
   • Close the app at any time without penalty
   • Skip any survey question without consequence
   • Delete your local data at any time
   • Withdraw from the study by simply stopping use of the app

7. CONTACT
   If you have questions about this study, contact the researcher at the email provided with this software.

8. AGREEMENT
   By clicking "I Agree" below, you confirm that:
   • You have read and understood this consent form
   • You are at least 15 years of age
   • You agree to participate in this study under the terms described above
"""
    text_widget.insert(tk.END, consent_body)
    text_widget.config(state=tk.DISABLED)
    
    # ========== BUTTONS ==========
    btn_frame = tk.Frame(root, bg="white")
    btn_frame.pack(pady=15)
    
    def on_decline():
        messagebox.showinfo(
            "Consent Declined",
            "You have chosen not to participate.\nThe app will now close.\n\nNo data has been collected."
        )
        root.destroy()
        on_result(False)
    
    def on_agree():
        try:
            with open(CONSENT_MARKER, "w") as f:
                f.write("consent_given\n")
        except Exception:
            pass
        root.destroy()
        on_result(True)
    
    decline_btn = tk.Button(
        btn_frame,
        text="I Decline",
        command=on_decline,
        font=("Helvetica", 11),
        width=12,
        bg="#e0e0e0",
        fg="#333333",
        relief=tk.FLAT,
        cursor="hand2"
    )
    decline_btn.pack(side=tk.LEFT, padx=10)
    
    agree_btn = tk.Button(
        btn_frame,
        text="I Agree",
        command=on_agree,
        font=("Helvetica", 11, "bold"),
        width=12,
        bg="#2e7d32",
        fg="white",
        relief=tk.FLAT,
        cursor="hand2"
    )
    agree_btn.pack(side=tk.LEFT, padx=10)
    
    # Handle window close button as decline
    root.protocol("WM_DELETE_WINDOW", on_decline)
    
    root.mainloop()