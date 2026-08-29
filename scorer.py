class Scorer:
    def __init__(self, baseline):
        self.baseline = baseline
        
    def calculate(self, current):
        score = 0.0
        breakdown = {}
        
        baseline_cpm = max(self.baseline.get('cpm', 1), 1)
        current_cpm = current.get('cpm', 0)
        speed_change = abs(current_cpm - baseline_cpm) / baseline_cpm
        speed_contrib = min(2.5, speed_change * 1.5)
        score += speed_contrib
        breakdown['typing'] = round(speed_contrib, 2)
        
        baseline_bs = self.baseline.get('backspace_ratio', 0)
        current_bs = current.get('backspace_ratio', 0)
        if baseline_bs > 0.001:
            bs_ratio = current_bs / baseline_bs
            bs_contrib = min(2.5, max(0, bs_ratio - 1) * 2.5)
        else:
            bs_contrib = min(2.5, current_bs * 10)
        score += bs_contrib
        breakdown['backspace'] = round(bs_contrib, 2)
        
        baseline_pause = self.baseline.get('pause_ratio', 0)
        current_pause = current.get('pause_ratio', 0)
        if baseline_pause > 0.001:
            pause_ratio = current_pause / baseline_pause
            pause_contrib = min(2.5, max(0, pause_ratio - 1) * 2.5)
        else:
            pause_contrib = min(2.5, current_pause * 10)
        score += pause_contrib
        breakdown['pause'] = round(pause_contrib, 2)
        
        baseline_mouse = max(self.baseline.get('mouse_rate', 1), 1)
        current_mouse = current.get('mouse_rate', 0)
        mouse_change = abs(current_mouse - baseline_mouse) / baseline_mouse
        mouse_contrib = min(2.5, mouse_change * 1.5)
        score += mouse_contrib
        breakdown['mouse'] = round(mouse_contrib, 2)
        
        final_score = round(min(10.0, score), 1)
        return final_score, breakdown
    
    def interpret(self, score):
        if score <= 3:
            return "Optimal", "green"
        elif score <= 6:
            return "Normal", "orange"
        elif score <= 8:
            return "Elevated", "red"
        else:
            return "Critical", "darkred"