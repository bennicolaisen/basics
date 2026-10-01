# Facit: Övning 1.16 – Minuter som text

def minutes_to_text(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours} h {minutes} min"
