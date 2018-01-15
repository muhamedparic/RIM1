import hashlib
import time
import random
import string
import json

import MySQLdb
from werkzeug.utils import secure_filename
from flask import send_from_directory

import utils

conn = MySQLdb.connect(host='localhost', user='admin', password='root', db='TEST')
secret_key = '7725b1b3d5aa1b7af2f102463e12740519c50112a370e74fce3340c96e54b979'
upload_folder = '/home/fajik/Desktop/ETFOCS/src/static/task_files'

def login(username, password):
    with conn.cursor() as cur:
        cur.execute('SELECT role FROM users WHERE username=%s AND password_hash=%s', (username, hashlib.sha256(password.encode('utf-8')).hexdigest()))
        result = cur.fetchone()
        if result is None:
            return None, False
        else:
            role = result[0]
            exp_at = str(int(time.time()) + 24 * 60 * 60)
            token = username + '.' + exp_at
            token_hash = hashlib.sha256((token + secret_key).encode('utf-8')).hexdigest()
            return {'token': token, 'role': role, 'hash': token_hash}, True

def register(username, password):
    with conn.cursor() as cur:
        cur.execute('INSERT INTO users(username, password_hash) VALUES (%s, %s)', (username, hashlib.sha256(password.encode('utf-8')).hexdigest()))
    conn.commit()
    return 'yos'

def user_exists(username):
    with conn.cursor() as cur:
        cur.execute('SELECT id FROM users WHERE username=%s', (username,))
        return cur.fetchone() is not None

def is_admin_user(username):
	with conn.cursor() as cur:
		cur.execute('SELECT id FROM users WHERE username=%s AND admin=1', (username,))
		return cur.fetchone() is not None

def get_role(username):
    with conn.cursor() as cur:
        cur.execute('SELECT role FROM users WHERE username=%s', (username,))
        return cur.fetchone()[0]

def token_valid(token):
    token = json.loads(token)
    token_string = token['token']
    token_hash = token['hash']
    if hashlib.sha256((token_string + secret_key).encode('utf-8')).hexdigest() != token_hash:
        return False
    user, exp_at = token_string.split('.')
    exp_at = int(exp_at)
    if not user_exists(user):
        return False
    return exp_at > time.time()

# Returns valid (bool), user (str), role (str, "admin" or "user")
def get_token_info(token):
    if type(token) == str:
        try:
            token = json.loads(token)
        except:
            return False, None, None
    if type(token) != dict:
        return False, None, None
    if not all(key in token for key in ('token', 'hash', 'role')):
        return False, None, None
    token_string = token['token']
    token_hash = token['hash']
    if type(token_string) != str:
        return False, None, None
    if hashlib.sha256((token_string + secret_key).encode('utf-8')).hexdigest() != token_hash:
        return False, None, None
    user, exp_at = None, None
    try:
        user, exp_at = token_string.split('.')
        exp_at = int(exp_at)
    except:
        return False, None, None
    token_role = get_role(user)
    if token_role not in ('user', 'admin'):
        return False, None, None
    if not user_exists(user) or exp_at <= time.time():
        return False, None, None
    return True, user, token_role

def valid_competition(comp_type, comp_name):
    with conn.cursor() as cur:
        cur.execute("""SELECT COUNT(*) FROM competition_types AS ct
                       INNER JOIN competitions AS c ON ct.id=c.type_fk
                       WHERE ct.description=%s and c.name=%s
                       """, (comp_type, comp_name))
        result = cur.fetchone()[0]
        return result == 1

def add_competition(token, comp_type, comp_name):
    token_info = get_token_info(token)
    if token_info[2] != 'admin':
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    if len(comp_name) == 0:
        return json.dumps({'success': False, 'reason': 'Invalid competition'})
    if comp_type not in ('fill', 'multiple_choice', 'code'):
        return json.dumps({'success': False, 'reason': 'Invalid competition type'})
    with conn.cursor() as cur:
        try:
            cur.execute("""INSERT INTO
                           competitions(name, type_fk, created_by_fk)
                           VALUES
                           (%s,
                           (SELECT id FROM competition_types WHERE description=%s),
                           (SELECT id FROM users WHERE username=%s))
                           """, (comp_name, comp_type, token_info[1]))
            conn.commit()
        except:
            return json.dumps({'success': False, 'reason': 'Invalid competition'})
    return json.dumps({'success': True})

def get_next_question_index(comp_name):
    with conn.cursor() as cur:
        cur.execute("""SELECT MAX(q.question_index)
                       FROM questions AS q
                       JOIN
                       competitions AS c
                       ON
                       q.competition_fk=c.id
                       WHERE
                       c.name=%s
                       """, (comp_name,))
        result = cur.fetchone()[0]
        if result is None:
            return 1
        else:
            return result + 1

def add_question(token, comp_type, comp_name, question_data, answer_data):
    token_info = get_token_info(token)
    if token_info[2] != 'admin':
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    if not valid_competition(comp_type, comp_name):
        return json.dumps({'success': False, 'reason': 'Invalid competition'})
    if comp_type == 'multiple_choice':
        question_text = None
        answer_list = None
        try:
            question_data = json.loads(question_data)
            question_text = question_data['question']
            answer_list = question_data['answers']
        except:
            return json.dumps({'success': False, 'reason': 'Invalid question data'})
        question_index = get_next_question_index(comp_name)
        if answer_data not in ('1', '2', '3', '4'):
            return json.dumps({'success': False, 'reason': 'Invalid answer'})
        answer_text = answer_data
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO
                           questions(competition_fk, question_index, question_text)
                           VALUES
                           ((SELECT id
                           FROM competitions
                           WHERE
                           name=%s),
                           %s,
                           %s)
                           """, (comp_name, question_index, question_text))
            cur.execute("SELECT LAST_INSERT_ID()")
            question_id = cur.fetchone()[0]
            for answer_index in range(4):
                cur.execute("""INSERT INTO
                               multiple_choice_answers(question_fk, answer_index, answer_text)
                               VALUES
                               (%s,
                               %s,
                               %s)
                               """, (question_id, answer_index + 1, answer_list[answer_index]))
            cur.execute("""INSERT INTO
                           correct_answers(question_fk, answer_text)
                           VALUES
                           (%s,
                           %s)
                           """, (question_id, answer_text))
            conn.commit()
    elif comp_type == 'fill':
        question_text = question_data
        answer_text = answer_data
        question_index = get_next_question_index(comp_name)
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO
                           questions(competition_fk, question_index, question_text)
                           VALUES
                           ((SELECT id
                           FROM competitions
                           WHERE
                           name=%s),
                           %s,
                           %s)
                           """, (comp_name, question_index, question_text))
            cur.execute("SELECT LAST_INSERT_ID()")
            question_id = cur.fetchone()[0]
            cur.execute("""INSERT INTO
                           correct_answers(question_fk, answer_text)
                           VALUES
                           (%s,
                           %s)
                           """, (question_id, answer_text))
            conn.commit()
    else:
        question_text = question_data
        question_index = get_next_question_index(comp_name)
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO
                           questions(competition_fk, question_index, question_text)
                           VALUES
                           ((SELECT id
                           FROM competitions
                           WHERE
                           name=%s),
                           %s,
                           %s)
                           """, (comp_name, question_index, question_text))
        conn.commit()
    return json.dumps({'success': True})


def get_competition_list(token):
    if get_token_info(token)[2] == None:
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    with conn.cursor() as cur:
        cur.execute("""SELECT c.name, ct.description FROM
                       competitions AS c INNER JOIN
                       competition_types AS ct
                       ON c.type_fk=ct.id
                       ORDER BY c.id
                       """)
        return json.dumps(cur.fetchall())

def remove_question(token, competition, question):
    return json.dumps({'success': False, 'reason': 'Function not usable'})
    if get_token_info(token)[2] != 'admin':
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM questions
                       WHERE
                       competition_fk=
                       (SELECT id FROM competitions WHERE name=%s)
                       AND
                       question_data=%s
                       """, (competition, question))
        if cur.rowcount == 0:
            return json.dumps({'success': False, 'reason': 'Invalid question'})
        conn.commit()
    return json.dumps({'success': True})

def competition_exists(competition):
    with conn.cursor() as cur:
        cur.execute("""SELECT COUNT(*)
                       FROM competitions
                       WHERE name=%s
                       """, (competition,))
        return int(cur.fetchone()[0]) == 1

def add_competitor(token, competition, user):
    token_info = get_token_info(token)
    if token_info[2] != 'admin':
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    if not user_exists(token_info[1]):
        return json.dumps({'success': False, 'reason': 'Invalid user'})
    if not competition_exists(competition):
        return json.dumps({'success': False, 'reason': 'Invalid competition'})
    with conn.cursor() as cur:
        try:
            cur.execute("""INSERT INTO
                           participations(competition_fk, user_fk)
                           VALUES
                           ((SELECT id FROM competitions WHERE name=%s),
                           (SELECT id FROM users WHERE username=%s))
                           """, (competition, user))
        except:
            return json.dumps({'success': False, 'reason': 'User already added'})
        cur.execute("""DELETE FROM applications
                       WHERE
                       user_fk=(SELECT id FROM users WHERE username=%s),
                       competition_fk=(SELECT id FROM competitions WHERE name=%s)
                       """, (user, competition))
        conn.commit()
    return json.dumps({'success': True})

def is_participant(competition, user):
    with conn.cursor() as cur:
        cur.execute("""SELECT COUNT(id)
                       FROM
                       participations
                       WHERE
                       user_fk=(SELECT id FROM users WHERE username=%s)
                       AND
                       competition_fk=(SELECT id FROM competitions WHERE name=%s)
                       """, (user, competition))
        return cur.rowcount == 1

def get_competition_questions_admin(comp_name):
    comp_type = get_competition_type(comp_name)
    with conn.cursor() as cur:
        if comp_type == 'fill':
            cur.execute("""SELECT q.question_text, ca.answer_text
                           FROM
                           questions AS q
                           JOIN
                           correct_answers AS ca
                           ON
                           q.id=ca.question_fk
                           JOIN
                           competitions AS c
                           ON
                           q.competition_fk=c.id
                           WHERE
                           c.name=%s
                           ORDER BY
                           q.question_index ASC
                           """, (comp_name,))
            result_list = [{'question_data': row[0], 'answer_data': row[1]}
                           for row in cur.fetchall()]
            return result_list
        elif comp_type == 'code':
            cur.execute("""SELECT q.question_text
                           FROM
                           questions AS q
                           JOIN
                           competitions AS c
                           ON
                           q.competition_fk=c.id
                           WHERE
                           c.name=%s
                           ORDER BY
                           q.question_index ASC
                           """, (comp_name,))
        elif comp_type == 'multiple_choice':
            question_ids = []
            question_texts = []
            answer_texts = [] # List of tuples
            correct_answers = []
            cur.execute("""SELECT q.id, q.question_text
                           FROM
                           questions AS q
                           JOIN
                           competitions AS c
                           ON
                           q.competition_fk=c.id
                           WHERE
                           c.name=%s
                           ORDER BY
                           q.question_index ASC
                           """, (comp_name,))
            for question_id, question_text in cur.fetchall():
                question_ids.append(question_id)
                question_texts.append(question_text)
            for question_id in question_ids:
                cur.execute("""SELECT mca.answer_text
                               FROM multiple_choice_answers AS mca
                               JOIN
                               questions AS q
                               ON
                               mca.question_fk=q.id
                               WHERE
                               q.id=%s
                               ORDER BY
                               mca.answer_index ASC
                               """, (question_id,))
                answer_texts.append(tuple(answer for answer in cur.fetchall()))
            for question_id in question_ids:
                cur.execute("""SELECT ca.answer_text
                               FROM
                               correct_answers AS ca
                               JOIN
                               questions AS q
                               ON
                               ca.question_fk=q.id
                               WHERE
                               q.id=%s
                               """, (question_id,))
                correct_answers.append(str(cur.fetchone()[0]))
            result_list = [{'question_data': {'question': question_texts[i], 'answers': answer_texts[i]},\
                           'answer_data': correct_answers[i]} for i in range(len(question_texts))]
            return result_list

def get_competition_questions(token, competition):
    token_info = get_token_info(token)
    if token_info[2] == 'admin':
        return json.dumps(get_competition_questions_admin(competition))
    elif token_info[2] == 'user':
        result_list = get_competition_questions_admin(competition)
        user_result_list = [{'question_data': result['question_data']} for result in result_list]
        return json.dumps(user_result_list)

def get_competition_type(comp_name):
    with conn.cursor() as cur:
        cur.execute("""SELECT ct.description
                       FROM competitions AS c
                       JOIN
                       competition_types AS ct
                       ON
                       c.type_fk=ct.id
                       WHERE
                       c.name=%s
                       """, (comp_name,))
        return cur.fetchone()[0]

def get_question_id(comp_name, question):
    with conn.cursor() as cur:
        cur.execute("""SELECT q.id
                       FROM
                       questions AS q
                       JOIN
                       competitions AS c
                       ON
                       q.competition_fk=c.id
                       WHERE
                       q.question_text=%s
                       AND
                       c.name=%s
                       """, (question, comp_name))
        return cur.fetchone()[0]

def is_correct_answer(comp_name, question, answer, question_index = None):
    with conn.cursor() as cur:
        if question_index is None:
            question_id = get_question_id(comp_name, question)
            cur.execute("""SELECT ca.answer_text
                           FROM
                           questions AS q
                           JOIN
                           correct_answers AS ca
                           ON
                           q.id=ca.question_fk
                           JOIN
                           competitions AS c
                           ON
                           q.competition_fk=c.id
                           WHERE
                           q.id=%s
                           AND
                           c.name=%s
                           """, (question_id, comp_name))
        else:
            cur.execute("""SELECT ca.answer_text
                           FROM
                           questions AS q
                           JOIN
                           correct_answers AS ca
                           ON
                           q.id=ca.question_fk
                           JOIN
                           competitions AS c
                           ON
                           q.competition_fk=c.id
                           WHERE
                           q.question_index=%s
                           AND
                           c.name=%s
                           """, (question_index, comp_name))
        return cur.fetchone()[0] == answer

def submit_answers(token, comp_name, answers):
    token_info = get_token_info(token)
    username = token_info[1]
    if not is_participant(comp_name, username):
        return json.dumps({'success': False, 'reason': 'User not participating'})
    answers = json.loads(answers)
    for i, answer_text in enumerate(answers):
        submit_answer(comp_name, username, i + 1, answer_text)
    return json.dumps({'success': True})

def submit_answer(comp_name, username, question_index, answer_text):
    with conn.cursor() as cur:
        cur.execute("""REPLACE INTO
                       user_answers(user_fk, question_fk, answer_text, correct)
                       VALUES
                       ((SELECT id FROM users WHERE username=%s),
                       (SELECT q.id
                       FROM questions AS q
                       JOIN
                       competitions AS c
                       ON
                       q.competition_fk=c.id
                       WHERE question_index=%s
                       AND
                       c.name=%s),
                       %s,
                       %s)
                       """, (username, question_index, comp_name, answer_text,
                             is_correct_answer(comp_name, None, answer_text, question_index)))
        conn.commit()
        if cur.rowcount == 0:
            return {'success': False}
        else:
            return {'success': True}

def get_competition_type(comp_name):
    with conn.cursor() as cur:
        cur.execute("""SELECT ct.description
                       FROM
                       competitions AS c
                       INNER JOIN
                       competition_types AS ct
                       ON c.type_fk=ct.id
                       WHERE c.name=%s
                       """, (comp_name,))
        return cur.fetchone()[0]

def add_task_file(token, competition, task_name, file_data, filename):
    token_info = get_token_info(token)
    if token_info[2] != 'admin':
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    if get_competition_type(competition) != 'code':
        return json.dumps({'success': False, 'reason': 'Invalid competition'})
    user = token_info[1]
    filename = secure_filename(filename)
    filepath = upload_folder + '/' + filename
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO
                       tasks(competition_fk, name, filepath, added_by_fk)
                       VALUES
                       ((SELECT id FROM competitions WHERE name=%s),
                       %s,
                       %s,
                       (SELECT id FROM users WHERE username=%s))
                       """, (competition, task_name, filename, user))
        if cur.rowcount == 1:
            conn.commit()
            with open(filepath, 'wb') as fout:
                fout.write(file_data.encode('ascii'))
            return json.dumps({'success': True})
        else:
            return json.dumps({'success': False})

def download_task_file(token, competition, task_name):
    token_info = get_token_info(token)
    if token_info[2] not in ('admin', 'user'):
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    with conn.cursor() as cur:
        cur.execute("""SELECT filepath
                       FROM tasks
                       WHERE
                       competition_fk=
                       (SELECT id FROM competitions WHERE name=%s)
                       AND
                       name=%s
                       """, (competition, task_name))
        result = cur.fetchone()
        if result is None:
            return json.dumps({'success': False, 'reason': 'Invalid competition or task name'})
        filepath = result[0]
        return send_from_directory('static/task_files', filepath)

def get_task_list(token, comp_name):
    token_info = get_token_info(token)
    if token_info[0] is False:
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    elif token_info[2] == 'admin' or is_participant(token_info[1]):
        with conn.cursor() as cur:
            cur.execute("""SELECT name
                           FROM tasks
                           WHERE
                           competition_fk=
                           (SELECT id FROM competitions WHERE name=%s)
                           """, (comp_name,))
            result = [row[0] for row in cur.fetchall()]
            return json.dumps(result)

def get_competition_results(token, comp_name):
    token_info = get_token_info(token)
    if token_info[2] != 'admin':
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    with conn.cursor() as cur:
        user_list = []
        cur.execute("""SELECT u.username
                       FROM users AS u
                       JOIN
                       participations AS p
                       ON
                       u.id=p.user_fk
                       JOIN
                       competitions AS c
                       ON
                       p.competition_fk=c.id
                       WHERE
                       c.name=%s
                       """, (comp_name,))
        user_list = [row[0] for row in cur.fetchall()]
        points_list = []
        for username in user_list:
            cur.execute("""SELECT CAST(SUM(ua.correct) AS SIGNED)
                           FROM user_answers AS ua
                           JOIN
                           users AS u
                           ON
                           ua.user_fk=u.id
                           JOIN
                           questions AS q
                           ON
                           ua.question_fk=q.id
                           JOIN
                           competitions AS c
                           ON
                           q.competition_fk=c.id
                           WHERE
                           u.username=%s
                           AND
                           c.name=%s
                           """, (username, comp_name))
            points = cur.fetchone()[0]
            if points is None:
                points = '0'
            points_list.append(points)
        return json.dumps(list(zip(user_list, points_list)))

def search_users(token, username):
    if get_token_info(token)[2] != 'admin':
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    with conn.cursor() as cur:
        cur.execute("""SELECT username
                       FROM users
                       WHERE
                       username LIKE %s
                       AND
                       role='user'
                       """, ('%' + username + '%',))
        results = [row[0] for row in cur.fetchall()]
        return json.dumps(results)

def get_user_competitions(token, username):
    token_info = get_token_info(token)
    if token_info[2] == 'admin' or token_info[1] == username:
        with conn.cursor() as cur:
            cur.execute("""SELECT c.name, ct.description
                           FROM
                           competitions AS c
                           JOIN participations AS p
                           ON
                           c.id=p.competition_fk
                           JOIN users AS u
                           ON
                           p.user_fk=u.id
                           JOIN competition_types AS ct
                           ON c.type_fk=ct.id
                           WHERE
                           u.username=%s
                           """, (username,))
            results = [(row[0], row[1]) for row in cur.fetchall()]
            return json.dumps(results)
    else:
        return json.dumps({'success': False, 'reason': 'Invalid token'})

def get_competition_participants(token, competition):
    token_info = get_token_info(token)
    if token_info[2] != 'admin':
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    with conn.cursor() as cur:
        cur.execute("""SELECT u.username
                       FROM
                       users AS u
                       JOIN participations AS p
                       ON
                       u.id=p.user_fk
                       JOIN competitions AS c
                       ON
                       p.competition_fk=c.id
                       WHERE
                       c.name=%s
                       """, (competition,))
        results = [row[0] for row in cur.fetchall()]
        return json.dumps(results)

def get_available_competition_list(token):
    token_info = get_token_info(token)
    username = token_info[1]
    if username is None:
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    with conn.cursor() as cur:
        cur.execute("""SELECT c.name, ct.description
                       FROM
                       competitions AS c
                       JOIN competition_types AS ct
                       ON
                       c.type_fk=ct.id
                       WHERE
                       (SELECT COUNT(*)
                       FROM participations AS p
                       WHERE
                       p.user_fk=(SELECT id FROM users WHERE username=%s)
                       AND
                       p.competition_fk=c.id)=0
                       """, (username,))
        results = [(row[0], row[1]) for row in cur.fetchall()]
        return json.dumps(results)

def user_applied(username, competition):
    with conn.cursor() as cur:
        cur.execute("""SELECT COUNT(*)
                       FROM applications AS a
                       JOIN users AS u
                       ON a.user_fk=u.id
                       JOIN competitions AS c
                       ON a.competition_fk=c.id
                       WHERE
                       u.username=%s
                       AND
                       c.name=%s
                       """, (username, competition))
        return str(cur.fetchone()[0]) == '1'

def apply_for_competition(token, competition):
    token_info = get_token_info(token)
    username = token_info[1]
    if username is None:
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    if user_applied(username, competition):
        return json.dumps({'success': False, 'reason': 'User already applied'})
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO
                       applications(user_fk, competition_fk)
                       VALUES
                       ((SELECT id FROM users WHERE username=%s),
                       (SELECT id FROM competitions WHERE name=%s))
                       """, (username, competition))
        conn.commit()
        return json.dumps({'success': True})

def application_list_admin(token, competition):
    token_info = get_token_info(token)
    if token_info[2] != 'admin':
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    with conn.cursor() as cur:
        cur.execute("""SELECT u.username
                       FROM users AS u
                       JOIN applications AS a
                       ON
                       u.id=a.user_fk
                       JOIN competitions AS c
                       ON
                       a.competition_fk=c.id
                       WHERE
                       c.name=%s
                       """, (competition,))
        results = [row[0] for row in cur.fetchall()]
        return json.dumps(results)

def application_list_all(token):
    token_info = get_token_info(token)
    if token_info[2] != 'admin':
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    with conn.cursor() as cur:
        cur.execute("""SELECT c.name, u.username
                       FROM users AS u
                       JOIN applications AS a
                       ON
                       u.id=a.user_fk
                       JOIN competitions AS c
                       ON
                       a.competition_fk=c.id
                       """)
        results = [(row[0], row[1]) for row in cur.fetchall()]
        return json.dumps(results)

def number_of_competitors(token):
    token_info = get_token_info(token)
    if token_info[2] != 'admin':
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    with conn.cursor() as cur:
        cur.execute("""SELECT c.name, CAST(COUNT(u.id) AS SIGNED)
                       FROM competitions AS c
                       JOIN participations AS p
                       ON
                       c.id=p.competition_fk
                       JOIN users AS u
                       ON
                       p.user_fk=u.id
                       GROUP BY c.id
                       """)
        results = [(row[0], int(row[1])) for row in cur.fetchall()]
        return json.dumps(results)

def competition_points(token, competition):
    token_info = get_token_info(token)
    username = token_info[1]
    if username is None:
        return json.dumps({'success': False, 'reason': 'Invalid token'})
    with conn.cursor() as cur:
        cur.execute("""SELECT CAST(SUM(ua.correct) AS SIGNED)
                       FROM user_answers AS ua
                       JOIN
                       users AS u
                       ON
                       ua.user_fk=u.id
                       JOIN
                       questions AS q
                       ON
                       ua.question_fk=q.id
                       JOIN
                       competitions AS c
                       ON
                       q.competition_fk=c.id
                       WHERE
                       u.username=%s
                       AND
                       c.name=%s
                       """, (username, competition))
        points = cur.fetchone()[0]
        return str(points) if points is not None else '0'
