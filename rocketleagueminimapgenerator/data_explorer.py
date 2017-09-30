def data_explorer_cli():
    from pprint import pprint
    from rocketleagueminimapgenerator.data import get_data
    from rocketleagueminimapgenerator.actor_data import get_actor_data
    from rocketleagueminimapgenerator.object_numbers import \
        get_ball_obj_nums, get_car_obj_nums, get_player_info

    print()

    print('Now entering raw data explorer CLI.')
    print("""
    Help:
    
    To see keys for data point: `keys [key...]`
    To see data for data point: `data [key...]`
    To see actor data:          `actor_data`
    To see ball object numbers: `ball_obj_nums`
    To see car object numbers:  `car_obj_nums`
    To see player info:         `player_info`
    To enter frame loop mode:   `loop_mode`
    To exit:                    `exit`
    """)

    cont = True

    data = get_data()

    while cont:
        user_input = input('> ').split(' ')

        parsed_input = []
        for in_string in user_input:
            try:
                parsed_input.append(int(in_string))
            except:
                parsed_input.append(in_string)

        if parsed_input[0] == 'keys':
            try:
                show_data = data
                for key in parsed_input[1:]:
                    if key != '':
                        show_data = show_data[key]
                pprint(show_data.keys())
            except KeyError:
                print('Key is not in data')
            except AttributeError:
                print('Key does not have any subkeys')
        elif parsed_input[0] == 'data':
            try:
                show_data = data
                for key in parsed_input[1:]:
                    if key != '':
                        show_data = show_data[key]
                pprint(show_data)
            except KeyError:
                print('Key is not in data')
            except AttributeError:
                print('Key does not have any subkeys')
        elif parsed_input[0] == 'actor_data':
            pprint(get_actor_data())
        elif parsed_input[0] == 'ball_obj_nums':
            pprint(get_ball_obj_nums())
        elif parsed_input[0] == 'car_obj_nums':
            pprint(get_car_obj_nums())
        elif parsed_input[0] == 'player_info':
            pprint(get_player_info())
        elif parsed_input[0] == 'loop_mode':
            loop_mode()
        elif parsed_input[0] == 'exit':
            cont = False
        else:
            print('Command Not Recognized.')
            print('User Input:  ', user_input)
            print('Parsed Input:', parsed_input)


def loop_mode():
    from pprint import pprint
    from rocketleagueminimapgenerator.data import get_data
    from rocketleagueminimapgenerator.object_numbers import \
        get_ball_obj_nums, get_car_obj_nums, get_player_info

    print('===== Entering Loop Mode =====')
    print('To exit, type exit.')
    user_input2 = input('Press Enter to Continue > ')
    parsed_user_input2 = user_input2.split(' ')

    data = get_data()

    if parsed_user_input2 != 'exit':
        for i, frame in enumerate(data['content']['frames']):
            if parsed_user_input2 != 'exit':
                for j, replication in enumerate(frame['replications']):
                    print('=====')
                    print('Frame:', i)
                    print('Time:', frame['time'])
                    print('Delta:', frame['delta'])
                    print('-----')
                    print('Replication:', j)
                    print('-----')

                    actor_id = replication['actor_id']['value']

                    if actor_id in get_ball_obj_nums():
                        print('Known Ball')
                    elif actor_id in get_car_obj_nums().keys():
                        car_id = get_car_obj_nums()[actor_id]
                        print('Known Car for Player #', car_id)
                        print('\tName:', get_player_info()[car_id]['name'])
                        print('\tTeam:', get_player_info()[car_id]['team'])
                    elif actor_id in get_player_info().keys():
                        print('Known Player:')
                        print('\tName:', get_player_info()[actor_id]['name'])
                        print('\tTeam:', get_player_info()[actor_id]['team'])

                    print('=====')

                    pprint(replication)

                    user_input2 = input('Press Enter to Continue > ')
                    parsed_user_input2 = user_input2.split(' ')

                    if parsed_user_input2 == 'exit':
                        return
            else:
                return
    else:
        return
