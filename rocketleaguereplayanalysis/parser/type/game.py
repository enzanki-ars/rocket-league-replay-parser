def update_game_data(update, frames, i):
    if 'TAGame.GameEvent_Soccar_TA:SecondsRemaining' in update.keys():
        frames[i]['time']['game_time'] = \
            update['TAGame.GameEvent_Soccar_TA:SecondsRemaining']
