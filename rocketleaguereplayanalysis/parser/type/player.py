def update_player_data(update, frames, i, actor_id):
    if 'Engine.PlayerReplicationInfo:Ping' in update.keys():
        frames[i]['cars'][actor_id]['ping'] = \
            update['Engine.PlayerReplicationInfo:Ping']
    if 'TAGame.PRI_TA:MatchScore' in update.keys():
        frames[i]['cars'][actor_id]['scoreboard']['score'] = \
            update['TAGame.PRI_TA:MatchScore']
    if 'TAGame.PRI_TA:MatchGoals' in update.keys():
        frames[i]['cars'][actor_id]['scoreboard']['goals'] = \
            update['TAGame.PRI_TA:MatchGoals']
        frames[i]['ball']['last_hit'] = None
    if 'TAGame.PRI_TA:MatchAssists' in update.keys():
        frames[i]['cars'][actor_id]['scoreboard']['assists'] = \
            update['TAGame.PRI_TA:MatchAssists']
    if 'TAGame.PRI_TA:MatchSaves' in update.keys():
        frames[i]['cars'][actor_id]['scoreboard']['saves'] = \
            update['TAGame.PRI_TA:MatchSaves']
    if 'TAGame.PRI_TA:MatchShots' in update.keys():
        frames[i]['cars'][actor_id]['scoreboard']['shots'] = \
            update['TAGame.PRI_TA:MatchShots']
