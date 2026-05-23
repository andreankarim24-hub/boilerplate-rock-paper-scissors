# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[], my_history=[], state=[None]):
 
    counter = {'R': 'P', 'P': 'S', 'S': 'R'}
 
    # Detect start of a new match and reset all state
    if prev_play == "":
        opponent_history.clear()
        my_history.clear()
        state.clear()
        state.append({
            'scores': [0, 0, 0, 0],
            'last_suggestions': ['R', 'R', 'R', 'R']
        })
 
    s = state[0]
    prev_play = prev_play or 'R'
    opponent_history.append(prev_play)
    n = len(opponent_history)
 
    # Score last round's suggestions
    if my_history:
        for i, suggestion in enumerate(s['last_suggestions']):
            if suggestion == counter[prev_play]:
                s['scores'][i] += 1
            elif suggestion != prev_play:
                s['scores'][i] -= 1
 
    # --- Strategy 0: Beat Quincy (fixed cycle R,R,P,P,S) ---
    quincy_seq = ["R", "R", "P", "P", "S"]
    s0 = counter[quincy_seq[n % 5]]
 
    # --- Strategy 1: Beat Kris (counters your last move) ---
    s1 = counter[counter[my_history[-1]]] if my_history else 'P'
 
    # --- Strategy 2: Beat Mrugesh (counters your most frequent in last 10) ---
    if my_history:
        last10 = my_history[-10:]
        most_freq = max(['R', 'P', 'S'], key=last10.count)
        s2 = counter[counter[most_freq]]
    else:
        s2 = 'P'
 
    # --- Strategy 3: Beat Abbey (Markov chain on your move pairs) ---
    if len(my_history) >= 2:
        pairs = {}
        for i in range(len(my_history) - 1):
            pair = my_history[i] + my_history[i + 1]
            pairs[pair] = pairs.get(pair, 0) + 1
        last_mine = my_history[-1]
        abbey_pred = max(['R', 'P', 'S'],
                         key=lambda m: pairs.get(last_mine + m, 0))
        s3 = counter[counter[abbey_pred]]
    else:
        s3 = 'P'
 
    suggestions = [s0, s1, s2, s3]
    s['last_suggestions'] = suggestions[:]
 
    best = s['scores'].index(max(s['scores']))
    my_play = suggestions[best]
 
    my_history.append(my_play)
    return my_play