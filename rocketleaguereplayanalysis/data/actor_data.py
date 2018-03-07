def parse_actor_data(data):
    actor_data = {}

    for frame in data['Frames']:
        for update in frame['ActorUpdates']:

            actor_id = update['Id']

            if actor_id not in actor_data.keys():
                actor_data[actor_id] = []

            if 'ClassName' in update.keys():
                if update['ClassName'] not in actor_data[actor_id]:
                    actor_data[actor_id].append(update['ClassName'])

    return actor_data
