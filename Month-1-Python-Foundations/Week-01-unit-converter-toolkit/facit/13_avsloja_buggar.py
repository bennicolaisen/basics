# Facit: Övning 1.13 – Avslöja buggarna. Förklaring i FACIT.md.


def check(seconds_to_hms):
    assert seconds_to_hms(0) == "0:00:00"
    assert seconds_to_hms(59) == "0:00:59"
    assert seconds_to_hms(65) == "0:01:05"
    assert seconds_to_hms(2700) == "0:45:00"
    assert seconds_to_hms(3600) == "1:00:00"
    assert seconds_to_hms(3665) == "1:01:05"
    assert seconds_to_hms(90000) == "25:00:00"
