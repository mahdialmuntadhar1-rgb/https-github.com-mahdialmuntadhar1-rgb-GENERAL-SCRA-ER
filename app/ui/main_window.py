import customtkinter as ctk
from typing import List, Dict, Any
from app.services.supabase_service import SupabaseService
from app.services.import_service import ImportService
from app.services.scraper_service import ScraperService
from app.validators.data_validator import DataValidator
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import threading
import queue

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Iraq University Data Platform - Admin")
        self.geometry("1100x700")
        
        # Services
        self.supabase = SupabaseService()
        self.importer = ImportService(self.supabase)
        self.scraper = ScraperService(self.supabase)
        self.validator = DataValidator()
        
        # Queue for thread-safe UI updates
        self.log_queue = queue.Queue()

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="IraqEdu Admin", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20, padx=20)

        self.btn_dashboard = ctk.CTkButton(self.sidebar, text="Dashboard", command=self.show_dashboard)
        self.btn_dashboard.pack(pady=10, padx=20)

        self.btn_import = ctk.CTkButton(self.sidebar, text="Import Center", command=self.show_import)
        self.btn_import.pack(pady=10, padx=20)

        self.btn_scraper = ctk.CTkButton(self.sidebar, text="Scraper Center", command=self.show_scraper)
        self.btn_scraper.pack(pady=10, padx=20)

        self.btn_review = ctk.CTkButton(self.sidebar, text="Review Queue", command=self.show_review)
        self.btn_review.pack(pady=10, padx=20)

        self.btn_universities = ctk.CTkButton(self.sidebar, text="Universities", command=self.show_universities)
        self.btn_universities.pack(pady=10, padx=20)

        # Main Content Area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.show_dashboard()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=20)
        
        try:
            univs = self.supabase.get_universities()
            staging = self.supabase.get_staging_records()
            
            stats_frame = ctk.CTkFrame(self.main_frame)
            stats_frame.pack(pady=20, padx=20, fill="x")
            
            ctk.CTkLabel(stats_frame, text=f"Total Universities: {len(univs)}", font=ctk.CTkFont(size=16)).pack(side="left", padx=20, pady=20)
            ctk.CTkLabel(stats_frame, text=f"Pending Reviews: {len(staging)}", font=ctk.CTkFont(size=16)).pack(side="left", padx=20, pady=20)
        except Exception as e:
            ctk.CTkLabel(self.main_frame, text=f"Error loading stats: {e}", text_color="red").pack()

    def show_import(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Import Center", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=20)

        btn_csv = ctk.CTkButton(self.main_frame, text="Import CSV", command=lambda: self.handle_import("csv"))
        btn_csv.pack(pady=10)

        btn_excel = ctk.CTkButton(self.main_frame, text="Import Excel", command=lambda: self.handle_import("excel"))
        btn_excel.pack(pady=10)

        btn_json = ctk.CTkButton(self.main_frame, text="Import JSON", command=lambda: self.handle_import("json"))
        btn_json.pack(pady=10)

    def show_scraper(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Scraper Center", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=20)

        controls = ctk.CTkFrame(self.main_frame)
        controls.pack(pady=10, padx=20, fill="x")

        self.btn_start = ctk.CTkButton(controls, text="▶ Start Scraping", fg_color="green", command=self.start_scraping_thread)
        self.btn_start.pack(side="left", padx=10, pady=10)

        self.btn_stop = ctk.CTkButton(controls, text="⏹ Stop Scraping", fg_color="red", command=self.stop_scraping_thread)
        self.btn_stop.pack(side="left", padx=10, pady=10)

        self.log_text = ctk.CTkTextbox(self.main_frame, width=800, height=400)
        self.log_text.pack(pady=20, padx=20, fill="both", expand=True)
        self.log_text.insert("end", "--- Scraper Logs ---\n")

        # Start checking queue for updates
        self.check_log_queue()

    def start_scraping_thread(self):
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.scraper.start_scraping(
            on_progress=lambda msg: self.log_queue.put(msg),
            on_complete=lambda count: self.log_queue.put(f"--- FINISHED: {count} records found ---")
        )

    def stop_scraping_thread(self):
        self.scraper.stop_scraping()
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")

    def check_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_text.insert("end", f"{msg}\n")
                self.log_text.see("end")
                if "FINISHED" in msg:
                    self.btn_start.configure(state="normal")
                    self.btn_stop.configure(state="disabled")
        except queue.Empty:
            pass
        self.after(100, self.check_log_queue)

    def handle_import(self, file_type: str):
        file_path = fd.askopenfilename(title=f"Select {file_type.upper()} file")
        if not file_path: return
        
        try:
            count = 0
            if file_type == "csv": count = self.importer.import_csv(file_path)
            elif file_type == "excel": count = self.importer.import_excel(file_path)
            elif file_type == "json": count = self.importer.import_json(file_path)
            
            mb.showinfo("Import Success", f"Successfully imported {count} records to staging.")
        except Exception as e:
            mb.showerror("Import Error", f"Failed to import: {e}")

    def show_review(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Review Queue", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=20)
        
        records = self.supabase.get_staging_records()
        if not records:
            ctk.CTkLabel(self.main_frame, text="No records pending review.").pack(pady=20)
            return

        scroll_frame = ctk.CTkScrollableFrame(self.main_frame, width=800, height=500)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        for record in records:
            row = ctk.CTkFrame(scroll_frame)
            row.pack(pady=5, padx=5, fill="x")
            
            data = record.get("raw_data", {})
            name = data.get("name_ar") or data.get("name_en") or "Unnamed"
            
            ctk.CTkLabel(row, text=name, width=300, anchor="w").pack(side="left", padx=10)
            
            ctk.CTkButton(row, text="Approve", width=80, fg_color="green", 
                          command=lambda r=record: self.approve_record(r)).pack(side="right", padx=5)
            ctk.CTkButton(row, text="Reject", width=80, fg_color="red",
                          command=lambda r=record: self.reject_record(r)).pack(side="right", padx=5)

    def approve_record(self, record: Dict[str, Any]):
        data = record.get("raw_data", {})
        # Simple mapping
        univ_data = {
            "name_ar": data.get("name_ar", "NOT VERIFIED"),
            "name_en": data.get("name_en"),
            "type": data.get("type", "private"),
            "website_url": data.get("website_url"),
            "is_verified": True
        }
        
        try:
            self.supabase.create_university(univ_data)
            self.supabase.update_staging_status(record["id"], "approved")
            mb.showinfo("Success", "Record approved and pushed to Supabase.")
            self.show_review()
        except Exception as e:
            mb.showerror("Error", f"Failed to approve: {e}")

    def reject_record(self, record: Dict[str, Any]):
        try:
            self.supabase.update_staging_status(record["id"], "rejected")
            self.show_review()
        except Exception as e:
            mb.showerror("Error", f"Failed to reject: {e}")

    def show_universities(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Approved Universities", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=20)
        
        univs = self.supabase.get_universities()
        scroll_frame = ctk.CTkScrollableFrame(self.main_frame, width=800, height=500)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        for u in univs:
            row = ctk.CTkFrame(scroll_frame)
            row.pack(pady=2, padx=5, fill="x")
            ctk.CTkLabel(row, text=u["name_ar"], width=300, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=u.get("type", ""), width=100).pack(side="left", padx=10)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
