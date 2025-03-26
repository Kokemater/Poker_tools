def analyze_opponent(model_info):
    vpip = model_info["VPIP"]
    if vpip > 40:
        print("Opponent plays too loose -> Make more value bets and increase postflop pressure.")
    elif vpip < 15:
        print("Opponent plays too tight -> Be more aggressive preflop.")

    pfr = model_info["PFR"]
    if pfr < 8:
        print("Opponent raises too little -> Exploit by stealing blinds aggressively.")
    elif pfr > 30:
        print("Opponent raises too much -> 3-bet more and defend wider.")

    three_bet = model_info["3Bet"]
    if three_bet < 5:
        print("Opponent 3-bets too little -> Fold to their 3-bets unless you have a strong hand.")
    elif three_bet > 10:
        print("Opponent 3-bets too much -> 4-bet lighter and call wider in position.")

    fold_to_3bet = model_info["Fold to 3Bet"]
    if fold_to_3bet > 70:
        print("Opponent folds too much to 3-bets -> Bluff 3-bet more.")
    elif fold_to_3bet < 40:
        print("Opponent calls too much vs 3-bets -> 3-bet mainly for value.")

    cold_call = model_info["Cold Call"]
    if cold_call > 30:
        print("Opponent cold calls too much -> Value bet bigger postflop.")
    elif cold_call < 10:
        print("Opponent rarely cold calls -> Bluff less and respect their calls.")

    cbet = model_info["CBet"]
    if cbet > 80:
        print("Opponent c-bets too much -> Float more and attack on later streets.")
    elif cbet < 40:
        print("Opponent c-bets too little -> Bet when they check.")

    fold_to_cbet = model_info["Fold to CBet"]
    if fold_to_cbet > 70:
        print("Opponent folds too much to c-bets -> C-bet with any hand.")
    elif fold_to_cbet < 30:
        print("Opponent calls too much vs c-bets -> C-bet for value only.")

    check_raise = model_info["Check-Raise"]
    if check_raise > 15:
        print("Opponent check-raises too much -> Call down lighter.")
    elif check_raise < 5:
        print("Opponent rarely check-raises -> Bet more frequently.")

    af = model_info["AF"]
    if af > 4.0:
        print("Opponent is overly aggressive -> Call down and let them bluff.")
    elif af < 1.5:
        print("Opponent is too passive -> Bet more often and exploit their calls.")

    steal = model_info["Steal"]
    if steal < 25:
        print("Opponent does not steal enough -> Don't over-defend blinds.")
    elif steal > 50:
        print("Opponent steals too much -> 3-bet and call more from the blinds.")

    fold_to_steal = model_info["Fold to Steal"]
    if fold_to_steal > 70:
        print("Opponent folds too much to steals -> Steal wide.")
    elif fold_to_steal < 40:
        print("Opponent defends too much vs steals -> Steal only with strong hands.")

    three_bet_vs_steal = model_info["3-Bet vs Steal"]
    if three_bet_vs_steal < 5:
        print("Opponent does not 3-bet vs steals -> Steal aggressively.")
    elif three_bet_vs_steal > 15:
        print("Opponent 3-bets too much vs steals -> 4-bet lighter and call wider.")

    wtsd = model_info["WTSD"]
    if wtsd > 35:
        print("Opponent goes to showdown too often -> Bet big for value.")
    elif wtsd < 20:
        print("Opponent avoids showdowns -> Bluff more.")

    wsd = model_info["W$SD"]
    if wsd > 55:
        print("Opponent only goes to showdown with strong hands -> Bluff more.")
    elif wsd < 45:
        print("Opponent goes to showdown with weak hands -> Value bet bigger.")

    afq = model_info["AFq"]
    if afq > 60:
        print("Opponent is overly aggressive -> Trap them by calling more.")
    elif afq < 40:
        print("Opponent is too passive -> Bet and raise more for value.")

    limp = model_info["Limp"]
    if limp > 20:
        print("Opponent limps too much -> Raise bigger and isolate them.")
    elif limp < 5:
        print("Opponent rarely limps -> Respect their limps.")

    limp_fold = model_info["Limp-Fold"]
    if limp_fold > 50:
        print("Opponent limps and folds too much -> Attack limpers aggressively.")

    limp_call = model_info["Limp-Call"]
    if limp_call > 50:
        print("Opponent limps and calls too much -> Value bet heavily postflop.")

    limp_raise = model_info["Limp-Raise"]
    if limp_raise > 10:
        print("Opponent limp-raises too much -> Be cautious when they do it.")


# Ejemplo de uso:
model_info = {
    "VPIP": 45, "PFR": 12, "3Bet": 8, "Fold to 3Bet": 75,
    "Cold Call": 35, "CBet": 85, "Fold to CBet": 25,
    "Check-Raise": 18, "AF": 5, "Steal": 55,
    "Fold to Steal": 80, "3-Bet vs Steal": 3, "WTSD": 40,
    "W$SD": 50, "WWSF": 40, "4-Bet": 12,
    "Donk Bet": 8, "AFq": 70, "Limp": 30,
    "Limp-Fold": 60, "Limp-Call": 40, "Limp-Raise": 15
}

analyze_opponent(model_info)

