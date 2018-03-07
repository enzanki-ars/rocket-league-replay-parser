def data_explorer_cli(data, actor_data, player_info, team_info, frames):
    from pprint import pprint

    print()

    print('Now entering raw data explorer CLI.')
    print("""
    Help:
    
    To see keys for data point:             `keys [key...]`
    To see data for data point:             `data [key...]`
    To see actor data:                      `actor_data`
    To see player info:                     `player_info`
    To see pressure info:                   `pressure_info`
    To see possession info:                 `possession_info`
    To enter source frame loop mode:        `source_loop_mode`
    To enter parsed data frame loop mode:   `data_loop_mode`
    To exit:                                `exit`
    """)

    cont = True

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
            pprint(actor_data)
        elif parsed_input[0] == 'player_info':
            pprint(player_info)
        elif parsed_input[0] == 'team_info':
            pprint(team_info)
        elif parsed_input[0] == 'pressure_info':
            print('Blue:\t', frames[-1]['pressure'][0])
            print('Orange:\t', frames[-1]['pressue'][1])
        elif parsed_input[0] == 'possession_info':
            print('Blue:\t', frames[-1]['possession'][0])
            print('Orange:\t', frames[-1]['possession'][1])
        elif parsed_input[0] == 'source_loop_mode':
            source_loop_mode(data)
        elif parsed_input[0] == 'data_loop_mode':
            data_loop_mode(frames)
        elif parsed_input[0] == 'exit':
            cont = False
        else:
            print('Command Not Recognized.')
            print('User Input:  ', user_input)
            print('Parsed Input:', parsed_input)


def source_loop_mode(data):
    from pprint import pprint

    print('===== Entering Loop Mode =====')
    print('To exit, type exit.')
    user_input2 = input('Press Enter to Continue > ')
    parsed_user_input2 = user_input2.split(' ')

    if parsed_user_input2 != 'exit':
        for i, frame in enumerate(data['Frames']):
            if parsed_user_input2 != 'exit':
                for j, update in enumerate(frame['ActorUpdates']):
                    print('=====')
                    print('Frame:', i)
                    print('Time:', frame['Time'])
                    print('Actor:', update['Id'])

                    print('=====')

                    pprint(update)

                    user_input2 = input('Press Enter to Continue > ')
                    parsed_user_input2 = user_input2.split(' ')

                    if parsed_user_input2 == 'exit':
                        return
            else:
                return
    else:
        return


def data_loop_mode(frames):
    from pprint import pprint

    print('===== Entering Loop Mode =====')
    print('To exit, type exit.')
    user_input2 = input('Press Enter to Continue > ')
    parsed_user_input2 = user_input2.split(' ')

    if parsed_user_input2 != 'exit':
        for i, frame in enumerate(frames):
            if parsed_user_input2 != 'exit':
                print('=====')
                print('Frame:', i)
                print('=====')

                pprint(frame)

                user_input2 = input('Press Enter to Continue > ')
                parsed_user_input2 = user_input2.split(' ')

                if parsed_user_input2 == 'exit':
                    return
            else:
                return
    else:
        return
