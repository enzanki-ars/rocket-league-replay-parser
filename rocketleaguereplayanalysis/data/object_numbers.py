from rocketleaguereplayanalysis.data.xp import get_xp_level, get_xp_title


def parse_game_event_num(actor_data):
    global game_event_num

    game_event_num = 1

    for obj in actor_data:
        if 'TAGame.GameEvent_Soccar_TA' in actor_data[obj]:
            game_event_num = obj
            return game_event_num


def parse_player_info(data):
    player_info = {}

    team0 = None
    team1 = None

    for i in range(0, len(data)):
        for update in data['Frames'][i]['ActorUpdates']:
            if 'ClassName' in update and update['ClassName'] == \
                    'TAGame.PRI_TA':
                player_id = update['Id']

                if player_id not in player_info:
                    player_info[player_id] = {}
                if 'Engine.PlayerReplicationInfo:PlayerName' in update.keys():
                    player_info[player_id]['name'] = \
                        update['Engine.PlayerReplicationInfo:PlayerName']
                if 'TAGame.PRI_TA:ClientLoadouts' in update.keys():
                    player_info[player_id]['items'] = \
                        update['TAGame.PRI_TA:ClientLoadouts']
                if 'Engine.PlayerReplicationInfo:Team' in update.keys():
                    player_info[player_id]['team_id'] = \
                        update['Engine.PlayerReplicationInfo:Team']['ActorId']
                if 'TAGame.PRI_TA:TotalXP' in update.keys():
                    player_info[player_id]['xp'] = \
                        update['TAGame.PRI_TA:TotalXP']
                    player_info[player_id]['xp_level'] = \
                        get_xp_level(update['TAGame.PRI_TA:TotalXP'])
                    player_info[player_id]['xp_title'] = \
                        get_xp_title(player_info[player_id]['xp_level'])
            elif 'ClassName' in update and update['ClassName'] == \
                    'TAGame.Team_Soccar_TA':
                if update['TypeName'] == 'Archetypes.Teams.Team0':
                    team0 = update['Id']
                elif update['TypeName'] == 'Archetypes.Teams.Team1':
                    team1 = update['Id']
                else:
                    print('wat? Teams don\'t seem to make sense...')
                    print('Found Team 0 (Usually Blue):  ', team0)
                    print('Found Team 1 (Usually Orange):', team1)
                    print('Weird Team:                   ', update['Id'])

    for player_id in player_info:
        if 'team_id' in player_info[player_id]:
            if player_info[player_id]['team_id'] == team0:
                player_info[player_id]['team'] = 0
            elif player_info[player_id]['team_id'] == team1:
                player_info[player_id]['team'] = 1

    team_info = {
        0: {
            'id': team0,
            'name': 'Blue',
            'color': '0x7f7fff'
        },
        1: {
            'id': team1,
            'name': 'Orange',
            'color': '0xffb27f'
        }
    }

    return player_info, team_info
