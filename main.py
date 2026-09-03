import time
import threading
import sys
import os

# ========== CONSENT CHECK (FIRST THING) ==========
from consent import has_consented, show_consent_form

def launch_app():
    from collector import ActivityCollector
    from scorer import Scorer
    from database import Database
    from dashboard import CLiPDashboard

    BASELINE_SECONDS = 60
    SCORING_INTERVAL = 10
    FEATURE_WINDOW = 60

    class CLiPApp:
        def __init__(self):
            self.collector = ActivityCollector()
            self.db = Database()
            self.scorer = None
            self.dashboard = None
            self.running = True

        def scoring_loop(self):
            print(f"[App] Collecting baseline for {BASELINE_SECONDS} seconds...")
            print("[App] Type normally. Do your usual work.")
            time.sleep(BASELINE_SECONDS)

            baseline = self.collector.set_baseline(duration_seconds=BASELINE_SECONDS)
            self.scorer = Scorer(baseline)
            print("[App] Baseline captured! Scoring begins.")

            while self.running:
                time.sleep(SCORING_INTERVAL)
                if not self.running:
                    break

                features = self.collector.compute_features(duration_seconds=FEATURE_WINDOW)
                score, breakdown = self.scorer.calculate(features)
                interpretation, color = self.scorer.interpret(score)

                self.db.insert(score, interpretation, features, breakdown)

                if self.dashboard:
                    self.dashboard.update(score, interpretation, color, breakdown, features)

                print(f"[App] CLI: {score} ({interpretation}) | Features: {features}")

        def run(self):
            k_listener, m_listener = self.collector.start()
            scorer_thread = threading.Thread(target=self.scoring_loop, daemon=True)
            scorer_thread.start()
            self.dashboard = CLiPDashboard(on_close_callback=self.stop)
            self.dashboard.run()
            k_listener.stop()
            m_listener.stop()
            print("[App] Shut down.")

        def stop(self):
            self.running = False

    print("=" * 50)
    print("  CLiP MVP - Cognitive Load Intelligence Platform")
    print("  Privacy-first. Local-only. No content recorded.")
    print("=" * 50)
    app = CLiPApp()
    app.run()


def on_consent_result(agreed):
    if not agreed:
        print("[App] Consent not given. Exiting.")
        sys.exit(0)
    launch_app()


# ========== ENTRY POINT ==========
if __name__ == "__main__":
    if has_consented():
        launch_app()
    else:
        show_consent_form(on_consent_result)