import numpy as np

def complex_analysis(happy_hist, surprise_hist, neutral_hist, gsr_hist):
    """
    Returns: (Verdict Text, Color Tuple, ID)
    ID Mapping:
    0 = GENUINELY HAPPY
    1 = POLITELY HAPPY
    2 = SECRETLY HAPPY
    3 = UNIMPRESSED
    """
    
    # Safety Check
    if not gsr_hist or len(gsr_hist) < 10:
        return "ANALYZING...", (200, 200, 200), 3 # Default to Unimpressed/Neutral

    # 1. CALCULATE METRICS
    gsr_smooth = np.convolve(gsr_hist, np.ones(5)/5, mode='valid')
    gradient = np.gradient(gsr_smooth)
    reaction_energy = np.sum(-gradient[gradient < 0]) 
    
    avg_happy = np.mean(happy_hist) if happy_hist else 0
    avg_surprise = np.mean(surprise_hist) if surprise_hist else 0

    # 2. THRESHOLDS
    BIO_THRESHOLD = 100   
    
    # WAS: SMILE_THRESHOLD = 50
    SMILE_THRESHOLD = 30 # Lower this to 30. 
    # If they are above 30%, they are trying to look happy. That counts.

    SURPRISE_THRESHOLD = 20

    # --- THE 4 VERDICTS ---

    is_smiling = avg_happy > SMILE_THRESHOLD
    has_reaction = (reaction_energy > BIO_THRESHOLD) or (avg_surprise > SURPRISE_THRESHOLD)

    # CASE 0: GENUINELY HAPPY
    if is_smiling and has_reaction:
        return "GENUINELY HAPPY", (0, 255, 0), 0

    # CASE 1: POLITE HAPPY
    elif is_smiling and not has_reaction:
        return "POLITE HAPPY", (255, 255, 0), 1

    # CASE 2: SECRETLY HAPPY
    elif not is_smiling and (reaction_energy > BIO_THRESHOLD):
        return "SECRETLY HAPPY", (0, 255, 255), 2

    # CASE 3: UNIMPRESSED
    else:
        return "UNIMPRESSED", (255, 0, 0), 3