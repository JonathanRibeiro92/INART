enviroments_tests = {1: {'initial_location':'A', 'A':'dirty', 'B':'dirty'},
2: {'initial_location':'A', 'A':'dirty', 'B':'clean'},
3: {'initial_location':'A', 'A':'clean', 'B':'dirty'},
4: {'initial_location':'A', 'A':'clean', 'B':'clean'},
5: {'initial_location':'B', 'A':'dirty', 'B':'dirty'},
6: {'initial_location':'B', 'A':'dirty', 'B':'clean'},
7: {'initial_location':'B', 'A':'clean', 'B':'dirty'},
8: {'initial_location':'B', 'A':'clean', 'B':'clean'}}


def agent_reflex(dic_environment):
    location = dic_environment['initial_location']
    status = dic_environment[location]
    if status == 'dirty':
        clean(location, dic_environment)
    switch_side(location, dic_environment)


def clean(location,dic_environment):
    print(f'Cleaning {location}...')
    dic_environment[location] = 'clean'
    print(f'{location} is clean!')


def switch_side(location, dic_environment):
    previous_position = location
    if location == 'A':
        dic_environment['initial_location'] = location = 'B'
    else:
        dic_environment['initial_location'] = location = 'A'
    print(f'Moved from {previous_position} to {location}')


if __name__ == '__main__':
    for key in enviroments_tests:
        print(f'Running test {key}')
        print(f'Environment : {enviroments_tests[key]}')
        agent_reflex(enviroments_tests[key])
        agent_reflex(enviroments_tests[key])
        print('------------------------------------------')