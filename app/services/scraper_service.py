import threading
import time
import random
from typing import Callable, Optional
from .supabase_service import SupabaseService
from ..validators.data_validator import DataValidator

class ScraperService:
    def __init__(self, supabase_service: SupabaseService):
        self.supabase = supabase_service
        self.validator = DataValidator()
        self.stop_event = threading.Event()
        self.is_running = False
        self.thread: Optional[threading.Thread] = None

    def start_scraping(self, on_progress: Callable[[str], None], on_complete: Callable[[int], None]):
        if self.is_running:
            return
        
        self.stop_event.clear()
        self.is_running = True
        self.thread = threading.Thread(
            target=self._run_scraper, 
            args=(on_progress, on_complete),
            daemon=True
        )
        self.thread.start()

    def stop_scraping(self):
        self.stop_event.set()
        self.is_running = False

    def _run_scraper(self, on_progress: Callable[[str], None], on_complete: Callable[[int], None]):
        sources = [
            "Ministry of Higher Education Website",
            "University of Baghdad News Feed",
            "Iraq Education Portal",
            "Social Media - University Announcements"
        ]
        
        count = 0
        try:
            for source in sources:
                if self.stop_event.is_set():
                    on_progress(f"🛑 Scraping stopped by user.")
                    break
                
                on_progress(f"🔍 Scraping source: {source}...")
                time.sleep(2) # Simulate network latency
                
                # Simulate finding 2-3 records per source
                for i in range(random.randint(1, 3)):
                    if self.stop_event.is_set(): break
                    
                    raw_record = {
                        "name_ar": f"جامعة تجريبية {random.randint(100, 999)}",
                        "name_en": f"Experimental University {random.randint(100, 999)}",
                        "website_url": f"https://example{random.randint(1, 100)}.edu.iq",
                        "type": random.choice(["public", "private", "college"]),
                        "source": source
                    }
                    
                    # Validation step
                    errors = self.validator.check_university(raw_record)
                    status = "pending"
                    
                    # Store in staging
                    self.supabase.create_staging_record(raw_record, source_file=f"Scraper: {source}")
                    count += 1
                    on_progress(f"✅ Found: {raw_record['name_ar']}")
                    time.sleep(1)

            on_progress(f"✨ Scraping session finished. {count} records added to staging.")
        except Exception as e:
            on_progress(f"❌ Error during scraping: {e}")
        finally:
            self.is_running = False
            on_complete(count)
