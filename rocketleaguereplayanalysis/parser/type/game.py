def update_game_data(update, frames, i):
    if 'TAGame.GameEvent_Soccar_TA:SecondsRemaining' in update['name']:
        frames[i]['time']['game_time'] = \
            update['value']['int']
