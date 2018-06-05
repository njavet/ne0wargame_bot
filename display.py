import jinja2
import datetime
import subprocess
import operator


def generate_help_txt(emoticons):
    keys = list(emoticons.keys())
    vals = list(map(lambda v: v.decode('utf-8'), emoticons.values()))

    template_loader = jinja2.FileSystemLoader(searchpath='./')
    template_env = jinja2.Environment(loader=template_loader)
    template_env.trim_blocks = True
    template_env.lstrip_blocks = True
    template_file = 'templates/help.template'
    template = template_env.get_template(template_file)

    output_text = template.render(emoticons=dict(zip(keys, vals)))
    return output_text


def generate_png(template_file, start, bg, args):
    begin = datetime.datetime.strptime(start, '%d.%m.%y')
    now = datetime.datetime.today()
    day = (now - begin).days
    png = template_file.replace('.template', '.png')

    template_loader = jinja2.FileSystemLoader(searchpath='./')
    template_env = jinja2.Environment(loader=template_loader)
    template_env.trim_blocks = True
    template_env.lstrip_blocks = True
    template = template_env.get_template(template_file)

    output_text = template.render(day=str(day).zfill(2), start=start, end='14.07.18', args=args)
    txt2png(output_text, png, bg=bg)
    return png


# TODO: ugly and dependent of an external command
def txt2png(in_txt, out_fname, font='DejaVu-Sans-Mono-Oblique', bg='lightblue'):
    tmp = 'label:' + in_txt
    # cmd = ['convert', '-font', font, '-size', '320x160', tmp, out_fname]
    cmd = ['convert', '-font', font, '-background', bg, tmp, out_fname]
    subprocess.call(cmd)


# stats
def format_stats_args(ranks, users):
    # lst: [rank, name, title, units, level]
    lst0 = []
    for user_id, user_dict in users.items():
        r0 = str(ranks[user_id])
        n0 = user_dict['first_name'].ljust(9)
        t0 = user_dict['title'].ljust(11)
        u0 = str(user_dict['total']).ljust(2)
        l0 = str(user_dict['level']).ljust(2)
        v0 = str(user_dict['week_victories']).ljust(2)
        lst0.append((r0, n0, t0, u0, l0, v0))
    return sorted(lst0, key=operator.itemgetter(0))


def generate_stats_png(start, bg, users, ranks):
    lst1 = format_stats_args(ranks, users)
    fname = generate_png('templates/stats.template', start, bg, lst1)
    return fname


# statsv
def format_statsv_args(users):
    lst0 = []
    for user_id, user_dict in users.items():
        lst1 = [('Name:', user_dict['first_name']),
                ('Title:', user_dict['title']),
                ('Belt:', user_dict['belt']),
                ('Rank:', user_dict['rank']),
                ('Total:', user_dict['total']),
                ('Level:', user_dict['level']),
                ('Week Victories:', user_dict['week_victories']),
                ('Weightlifting:', user_dict['weightlifting']),
                ('Martial-arts:', user_dict['martial_arts']),
                ('Cardio:', user_dict['cardio']),
                ('Calisthenics', user_dict['calisthenics'])]
        lst0.append(lst1)
    return sorted(lst0, key=operator.itemgetter(3))


def generate_statsv_png(start, bg, users):
    users0 = format_statsv_args(users)
    fname = generate_png('templates/statsv.template', start, bg, users0)
    return fname
