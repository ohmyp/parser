import requests
from bs4 import BeautifulSoup

subjects = {'английский':178, 'алгебра':3149, 'химия':199, 'обж':206, 'русский':185, 'литература':187, 'физика':198, 'геометрия':173, 'история':174, 'астрономия':5516,
            'биология':197, 'география':3139, 'информатика':191, 'искусство':34279, 'обществознание':175}

start = 'Для того чтобы получить последнее домашнее задание из электронного дневника, напишите название предмета. \n Список предметов можно вызвать командой /предметы'
help_subjects = 'Английский, Алгебра, Астрономия, Биология, География, Геометрия, История, Информатика, Искусство, Литература, Обществознание, ОБЖ, Русский, Физика, Химия'

def loginbot(login, password, subject):
    s = requests.Session()
    s.get('https://petersburgedu.ru/dnevnik/subject/statistic/student/ХХХ/subject/{}'.format(subject)) # ВСТАВИТЬ СВОЙ АЙДИ ВМЕСТО ХХХ

    data = {
        'Login': login,
        'Password': password,
        'doLogin': '1',
        'authsubmit': 'Войти'
    }
    r = s.post('https://petersburgedu.ru/user/auth/login/', data=data)
    r = s.get('https://petersburgedu.ru/dnevnik/subject/statistic/student/ХХХ/subject/{}'.format(subject)) # ВСТАВИТЬ СВОЙ АЙДИ ВМЕСТО ХХХ
    return r.text

def get_content(html):
    soup = BeautifulSoup(html, features="html.parser")
    items = soup.find('table', class_='subject-stat')
    items = items.find_all_next('td')
    return items

def parser(subject):
    a = loginbot('ХХХ', 'УУУ', subject) # ВСТАВИТЬ ЛОГИН И ПАРОЛЬ ВМЕСТО ХХХ И УУУ СООТВЕТСТВЕННО
    b = get_content(a)
    c = str(b[2]).strip('<td>').strip('</td>').strip()
    try:
        c = c.strip('</a></span>')
        list = c.split('<a href="')
        href = 'https://petersburgedu.ru' + list[1].split('">')[0]
        c = list[0].strip().strip('<span class="attach"><i></i>').strip()
        c = c + "\n Ссылка на скачивание документа: " + href
    except:
        pass

    return c

def user_identify(user_id):
    user_info = requests.get('https://api.vk.com/method/users.get', params={'access_token':group_token, 'user_ids':user_id, 'v':5.103}).json()
    return user_info['response'][0]['last_name']


def element_check(element):
    user_id = element['object']['user_id']
    user_name = user_identify(user_id)
    try:
        user_input = element['object']['body'].lower()
    except:
        pass
    print(user_name,': ', user_input)

    if user_input == 'тест':
        message_send(user_id, 'Готов к работе!')
    elif user_input == '/start':
        message_send(user_id, start)
    elif user_input == '/предметы':
        message_send(user_id, help_subjects)

    else:
        try:
            message_send(user_id, parser(subjects[user_input]))

        except:
            message_send(user_id, 'Не совсем тебя понимаю!')

def vk():
    global group_token
    group_token = 'ХХХ' # ВСТАВИТЬ ТОКЕН ГРУППЫ В ВК ВМЕСТО ХХХ
    data = requests.get('https://api.vk.com/method/groups.getLongPollServer',
                    params={'access_token': group_token, 'v':5.103, 'group_id':ХХХ}).json()['response'] # ВСТАВИТЬ АЙДИ ГРУППЫ ВК ВМЕСТО ХХХ (ЧИСЛО)
    url = '{server}?act=a_check&key={key}&ts={ts}&wait=25'.format(server=data['server'], key=data['key'], ts=data['ts'])
    response = requests.get(url).json()
    updates = response['updates']
    if updates:
        for element in updates:
            element_check(element)

def message_send(user_id, message):
    send = requests.get('https://api.vk.com/method/messages.send',
                                params={'access_token': group_token, 'v': 5.103,
                                        'peer_id': user_id, 'random_id': 0, 'message': message})


while True:
    vk()