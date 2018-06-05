"""
basic configs like which emoticons to use for which training unit,
which titles a user has depending on his level, etc...
seems ugly, but I think it's better to hardcode this into the app
"""


class BotConfig(object):
    def __init__(self):
        # depending on your level, you have a different title
        self.titles = {0: "Hübi",
                       1: "GommerPyle",
                       2: "n00b",
                       3: "HotBoy",
                       4: "Nitōhei",
                       5: "Soldier",
                       6: "Gunsō",
                       7: "Captain",
                       8: "Major",
                       9: "General",
                       10: "Shōgun",
                       11: "IvanDrago",
                       12: "JohnRambo",
                       13: "Cyborg",
                       14: "Terminator"}
        # after every 4 units you reach the next level
        self.lvlup = 4
        # after every 16 units you reach the next belt
        self.beltup = 16
        # emoticons for determining the training unit
        self.emoticons = {'weightlifting': b'\xf0\x9f\xa6\x8d',
                          'cardio': b'\xf0\x9f\x90\x8e',
                          'calisthenics': b'\xf0\x9f\x90\x92',
                          'martial_arts': b'\xf0\x9f\xa5\x8b'}

        # pink, yellow, orange, red
        self.belts = ['#FF75DF', '#FEFB8F', '#E0792E', '#D83333']

    # get reply messages
    @staticmethod
    def get_greetings_msg(first_name):
        return ''.join(['@', first_name, ' Welcome to the Wargame!!'])

    @staticmethod
    def get_confirm_msg(first_name, key):
        a0 = ''.join([key, ' unit confirmed...'])
        return ''.join(['@', first_name, ' ', a0])

    @staticmethod
    def get_level_up_msg(userdata):
        first_name = userdata['first_name']
        level = userdata['level']
        title = userdata['title']
        a0 = 'Congrats for the level up!!\n'
        a1 = 'You reached level {}!!\n'.format(level)
        a2 = 'Your new Title is: {} ...'.format(title)
        return ''.join(['@', first_name, ' ', a0, a1, a2])
