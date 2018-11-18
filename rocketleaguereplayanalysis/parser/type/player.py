def update_player_data(update, frames, i, actor_id):
    if 'Engine.PlayerReplicationInfo:Ping' in update['name']:
        frames[i]['cars'][actor_id]['ping'] = \
            update['value']['byte']
    if 'TAGame.PRI_TA:MatchScore' in update['name']:
        frames[i]['cars'][actor_id]['scoreboard']['score'] = \
            update['value']['int']
    if 'TAGame.PRI_TA:MatchGoals' in update['name']:
        frames[i]['cars'][actor_id]['scoreboard']['goals'] = \
            update['value']['int']
        frames[i]['ball']['last_hit'] = None
    if 'TAGame.PRI_TA:MatchAssists' in update['name']:
        frames[i]['cars'][actor_id]['scoreboard']['assists'] = \
            update['value']['int']
    if 'TAGame.PRI_TA:MatchSaves' in update['name']:
        frames[i]['cars'][actor_id]['scoreboard']['saves'] = \
            update['value']['int']
    if 'TAGame.PRI_TA:MatchShots' in update['name']:
        frames[i]['cars'][actor_id]['scoreboard']['shots'] = \
            update['value']['int']
