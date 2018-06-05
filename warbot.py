import config
import display
import re
import collections
import operator


class WarBot(object):
    def __init__(self, storage):
        self.configs = config.BotConfig()
        self.ops = BotOps(self.configs)
        self.storage = storage
        self.chats = self.storage.read_chats()
        self.start = '20.05.18'

    @staticmethod
    def send_photo(bot, update, fname):
        with open(fname, 'rb') as f:
            bot.send_photo(chat_id=update.message.chat_id, photo=f)

    def create_user_dict(self, first_name):
        k0 = ['first_name', 'title', 'belt', 'total', 'rank']
        k1 = ['level', 'week_victories', 'weightlifting']
        k2 = ['cardio', 'martial_arts', 'calisthenics']

        init_title = self.configs.titles[0]
        init_belt = self.configs.belts[0]
        vals = [first_name, init_title, init_belt, 0, 0, 0, 0, 0, 0, 0, 0]
        return dict(zip(k0 + k1 + k2, vals))

    def add_user(self, chat_id, user_id, first_name):
        self.chats[chat_id][user_id] = self.create_user_dict(first_name)

    def set_user_lvl(self, chat_id, user_id):
        units = self.chats[chat_id][user_id]['total']
        lvlup = self.configs.lvlup
        self.chats[chat_id][user_id]['level'] = units // lvlup

    def set_user_title(self, chat_id, user_id):
        titles = self.configs.titles
        level = self.chats[chat_id][user_id]['level']
        self.chats[chat_id][user_id]['title'] = titles[level]

    def set_user_belt(self, chat_id, user_id):
        level = self.chats[chat_id][user_id]['level']
        nxtbelt = self.configs.beltup
        belt = self.configs.belts[level // nxtbelt]
        self.chats[chat_id][user_id]['belt'] = belt

    def set_ranks(self, users):
        ranks = self.ops.get_ranks(users)
        for user_id, user_dict in users.items():
            user_dict['rank'] = ranks[user_id]

    # bot commands
    def send_help(self, bot, update):
        emoticons = self.configs.emoticons
        help_text = display.generate_help_txt(emoticons)
        bot.send_message(chat_id=update.message.chat_id, text=help_text)

    def send_stats(self, bot, update):
        chat_id = "-251980753"
        # chat_id = str(update.message.chat_id)
        users = self.chats[chat_id]
        ranks = self.ops.get_ranks(users)
        user_id = str(update.message.from_user.id)
        bg = self.ops.get_background_color(user_id, users)
        fname = display.generate_stats_png(self.start, bg, users, ranks)
        self.send_photo(bot, update, fname)

    def send_statsv(self, bot, update):
        chat_id = "-251980753"
        # chat_id = str(update.message.chat_id)
        users = self.chats[chat_id]
        user_id = str(update.message.from_user.id)
        bg = self.ops.get_background_color(user_id, users)
        fname = display.generate_statsv_png(self.start, bg, users)
        self.send_photo(bot, update, fname)

    def end_wargame(self, bot, update):
        pass

    # message handler
    def analyze_msg(self, bot, update):
        msg = update.message.text
        msgutf8 = msg.encode('utf-8')

        chat_id = str(update.message.chat_id)
        # chat_id = "-251980753"
        user_id = str(update.message.from_user.id)
        first_name = update.message.from_user.first_name

        if chat_id not in self.chats.keys():
            self.chats[chat_id] = {}

        if user_id not in self.chats[chat_id].keys():
            self.add_user(chat_id, user_id, first_name)
            ans = self.configs.get_greetings_msg(first_name)
            bot.send_message(chat_id=chat_id, text=ans)

        lvl_before = self.chats[chat_id][user_id]['level']
        check_perf = self.ops.test_training(str(msgutf8))

        # update training units
        for training, result in check_perf.items():
            if result:
                self.chats[chat_id][user_id][training] += 1
                ans = self.configs.get_confirm_msg(first_name, training)
                bot.send_message(chat_id=chat_id, text=ans)

        # check if any training has been done and update stats
        if any(list(check_perf.values())):
            self.chats[chat_id][user_id]['total'] += 1
            self.set_user_lvl(chat_id, user_id)
            self.set_user_title(chat_id, user_id)
            self.set_ranks(self.chats[chat_id])
            self.storage.update_chats(self.chats)

        # check if any level up happened
        if self.chats[chat_id][user_id]['level'] > lvl_before:
            userdict = self.chats[chat_id]
            ans = self.configs.get_level_up_msg(userdict[user_id])
            bot.send_message(chat_id=chat_id, text=ans)


class BotOps(object):
    def __init__(self, configs):
        self.configs = configs
        self.emo_regex_dict = self.emoticons_regex_init()

    # training detection methods
    def emoticons_regex_init(self):
        emoticons = self.configs.emoticons
        keys = list(emoticons.keys())
        vals = [str(emo)[1:].strip('\'') for emo in emoticons.values()]
        return dict(zip(keys, vals))

    def test_training(self, msg_str):
        regex_dict = self.emo_regex_dict
        keys = regex_dict.keys()
        vals0 = regex_dict.values()
        vals1 = [re.search(re.escape(val), msg_str) for val in vals0]
        return dict(zip(keys, vals1))

    @staticmethod
    def get_units(users):
        return {user_id: val['total'] for user_id, val in users.items()}

    @staticmethod
    def get_ranks(users):
        dix0 = collections.defaultdict(list)
        lst0 = [(key, users[key]['total']) for key in users.keys()]
#        ranks = sorted(lst0, reverse=True, key=operator.itemgetter(1))
        ranks = sorted(lst0, key=operator.itemgetter(1))
        for (user_id, units) in ranks:
            dix0[units].append(user_id)
        dix1 = {}
        for i, (units, user_ids) in enumerate(dix0.items()):
            for user_id in user_ids:
                dix1[user_id] = i+1
        return dix1

    def get_background_color(self, user_id, users):
        belts = self.configs.belts
        nxtbelt = self.configs.beltup
        units = users[user_id]['total']
        return belts[units // nxtbelt]

