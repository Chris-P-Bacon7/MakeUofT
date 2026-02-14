def calculate_gift_score(happiness, pulse, gsr):
    """
    Returns a score (0-100) and a string verdict.
    """
    # Normalize inputs (assuming gsr is 0-1023, pulse is 0-20, happy is 0-100)
    
    # 1. THE FAKE SMILE DETECTOR
    # If they are smiling but their body is completely calm...
    if happiness > 70 and gsr < 300 and pulse < 5:
        return 45, "POLITE SMILE (FAKE?)"

    # 2. THE GENUINE EXCITEMENT
    # High smile + any physiological spike
    if happiness > 60 and (gsr > 500 or pulse > 10):
        return 95, "GENUINE JOY!"

    # 3. THE "SHY" LIKING
    # They aren't smiling much, but their heart/sweat is spiking!
    if happiness < 40 and (gsr > 600 or pulse > 12):
        return 75, "INTERNALLY EXCITED"

    # 4. THE DISAPPOINTMENT
    if happiness < 30 and gsr < 400:
        return 15, "NOT THEIR STYLE"

    return 50, "ANALYZING..."