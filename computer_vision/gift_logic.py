import numpy as np

def complex_analysis(happy_hist, surprise_hist, neutral_hist, gsr_hist):
    # 1. SAFETY CHECK
    if len(gsr_hist) < 40: # Wait slightly longer for data stability
        return "STABILIZING SENSORS...", (150, 150, 150), 4

    # 2. CALCULATE BIO-METRICS (Tougher Filter)
    gsr_smooth = np.convolve(gsr_hist, np.ones(5)/5, mode='valid')
    gradient = np.gradient(gsr_smooth)
    # Cumulative Energy
    reaction_energy = np.sum(-gradient[gradient < 0]) 
    
    # 3. CALCULATE EMOTION METRICS (Switching from MAX to MEAN)
    # Using the mean makes it "tougher" because you must maintain the face
    avg_happy = np.mean(happy_hist) if happy_hist else 0
    avg_surprise = np.mean(surprise_hist) if surprise_hist else 0
    avg_neutral = np.mean(neutral_hist) if neutral_hist else 0

    # 4. STRICT THRESHOLDS
    # Raised BIO from 100 to 200: Requires a very sharp, distinct sweat spike
    BIO_THRESHOLD = 150   
    # Raised SMILE from 40 to 60: Requires a clear, wide grin
    SMILE_THRESHOLD = 50
    SURPRISE_THRESHOLD = 35

    # 5. CLASSIFICATION WITH "NEUTRAL" PENALTY
    # If the user is >70% neutral on average, we disqualify 'is_smiling'
    is_smiling = (avg_happy > SMILE_THRESHOLD) and (avg_neutral < 70)
    has_reaction = (reaction_energy > BIO_THRESHOLD) or (avg_surprise > SURPRISE_THRESHOLD)

    # --- THE VERDICTS ---
    if is_smiling and has_reaction:
        return "GENUINELY HAPPY", (0, 255, 0), 0
    elif is_smiling and not has_reaction:
        return "POLITE HAPPY", (255, 255, 0), 1
    elif not is_smiling and has_reaction:
        return "SECRETLY HAPPY", (0, 255, 255), 2
    else:
        # Default fallback is now much more likely
        return "UNIMPRESSED", (255, 0, 0), 3