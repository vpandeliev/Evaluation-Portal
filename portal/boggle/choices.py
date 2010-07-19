'''Enumerated choices for the boggle app.
'''


from alphacabbage.django.choices import ChoiceList


game_states = ChoiceList('''
Waiting for players
In progress
Complete
''')

boggle_modes = ChoiceList('''
Normal
Master
Challenge cube
''')
