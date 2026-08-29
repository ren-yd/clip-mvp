import time
import threading
from collections import deque
from pynput import keyboard, mouse

class ActivityCollector:
    def __init__(self, max_age_seconds=600):
        self.events = deque()
        self.lock = threading.Lock()
        self.last_event_time = time.time()
        self.max_age = max_age_seconds
        self.baseline = None
        self.baseline_ready = False
        
    def _prune_old_events(self):
        cutoff = time.time() - self.max_age
        while self.events and self.events[0]['time'] < cutoff:
            self.events.popleft()
    
    def on_key_press(self, key):
        with self.lock:
            now = time.time()
            key_str = str(key)
            is_backspace = 'backspace' in key_str.lower() or 'delete' in key_str.lower()
            gap = now - self.last_event_time
            self.events.append({
                'time': now,
                'type': 'key',
                'is_backspace': is_backspace,
                'gap': gap
            })
            self.last_event_time = now
            self._prune_old_events()
    
    def on_click(self, x, y, button, pressed):
        if pressed:
            with self.lock:
                now = time.time()
                gap = now - self.last_event_time
                self.events.append({
                    'time': now,
                    'type': 'mouse',
                    'gap': gap
                })
                self.last_event_time = now
                self._prune_old_events()
    
    def start(self):
        k_listener = keyboard.Listener(on_press=self.on_key_press)
        m_listener = mouse.Listener(on_click=self.on_click)
        k_listener.start()
        m_listener.start()
        print("[Collector] Started listening to keyboard & mouse...")
        return k_listener, m_listener
    
    def compute_features(self, duration_seconds=300):
        cutoff = time.time() - duration_seconds
        with self.lock:
            self._prune_old_events()
            recent = [e for e in self.events if e['time'] > cutoff]
        
        if not recent:
            return {
                'cpm': 0.0,
                'backspace_ratio': 0.0,
                'pause_ratio': 0.0,
                'mouse_rate': 0.0
            }
        
        total_keys = sum(1 for e in recent if e['type'] == 'key')
        backspaces = sum(1 for e in recent if e.get('is_backspace'))
        mouse_clicks = sum(1 for e in recent if e['type'] == 'mouse')
        
        cpm = (total_keys / duration_seconds) * 60
        bs_ratio = backspaces / max(total_keys, 1)
        long_gaps = [e['gap'] for e in recent if e['gap'] > 2.0]
        pause_time = sum(long_gaps)
        pause_ratio = min(1.0, pause_time / duration_seconds)
        mouse_rate = (mouse_clicks / duration_seconds) * 60
        
        return {
            'cpm': round(cpm, 1),
            'backspace_ratio': round(bs_ratio, 3),
            'pause_ratio': round(pause_ratio, 3),
            'mouse_rate': round(mouse_rate, 1)
        }
    
    def set_baseline(self, duration_seconds=900):
        print(f"[Collector] Computing baseline from last {duration_seconds}s...")
        self.baseline = self.compute_features(duration_seconds)
        self.baseline_ready = True
        print(f"[Collector] Baseline set: {self.baseline}")
        return self.baseline