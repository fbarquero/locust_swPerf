__author__ = 'mblair'

import pickle
from requests import Session

from configs.config import LocustConfigs as MM
from configs.config import GlobalConfigs as GC
from sw_requests.login import Login
import time
import multiprocessing as mp


def get_user_name(iteration_loop_int):
    """
    Get swPer username All Filters On based on int, i.e:
    swPerfUserAllFiltersOn_00001+QA1@socialware.com
    the - 00001 - section of the username is generated based
    on the param iteration_loop_int
    :param iteration_loop_int:
    :return: username i.e swPerfUserAllFiltersOn_00001+QA1@socialware.com
    """
    iterator_as_string = str(iteration_loop_int)
    padded_number = iterator_as_string.zfill(5)
    name = 'swPerfUserAllFiltersOn_' + padded_number
    email = name + '+QA1@socialware.com'
    return email


def get_user_credentials(x):
    """
    Get username credentials based on login style:
    once = returns a tuple of user, cookie
    all = returns just the username
    :param x: number to generate the username i.e
    - 00001 - will be the 0000x of swPerfUserAllFiltersOn_00001+QA1@socialware.com
    :return:
    """
    try:
        user_login = Login(None)
        if MM.LOGIN_STYLE is "once":
            user = get_user_name(x)
            r = user_login.sw_valid_login(username=user, password=user, url=GC.SOCIAL_NETWORKING_URLs['direct_sowatest'])
            if r.status_code != 200:
                raise Exception("Errors found at the moment of create the user {}, Error Code {}".format(user, r.status_code))
            user = (user, user_login.client.cookies)
        else:
            user = get_user_name(x)
    except Exception, e:
        user = False
        print("Failure:{}".format(e.message))
    finally:
        if user is not False and MM.LOGIN_STYLE is "once":
            print(user[0])
        else:
            print(user)
        # user_login.session.close()
    return user


def get_user_pool(users):
    """
    Creates a user pool to be used in the performance / load tests
    based on the login style, using a pool of 50 processes you speed up
    the username and cookie creation for login once style
    :param users: amount of users that will be added to the pool i.e 250
    :return: returns a list of users, if login style = once, each item of the list
    will be a tuple, the [0] = username, [1] Cookie
    If login style == all, the itmes of the list will be just the username
    """
    GC.GLOBAL_REQUEST_TIMEOUT = 120
    try:
        start = time.time()
        pool = mp.Pool(processes=20)
        results = pool.map(get_user_credentials, xrange(1, users + 1))
    except Exception, e:
        print e.message
        raise Exception(e.message)
    finally:
        pool.close()
        pool.join()
        print("Duration: {}".format(time.time() - start))
    return results if all(results) else None


def save_sessions_pickle(users):
    """
    Saves the users pool in an obj file to be consumed by the tests
    :param users: Number of users to create for the pool that will be saved
    in the obj file
    :return:
    """
    sessions = get_user_pool(users)
    if sessions is not None:
        with open(GC.SESSIONS_FILE_PATH, "wb") as f:
            pickle.dump(sessions, f)
    else:
        raise Exception("One or more users where not created as expected\n"
                        "Try to load the users again ...")


def load_sessions_pickle():
    """
    Loads the pool object saved on the sessions.obj file to use the users pool
    in the transactions.
    :return:
    """
    with open(GC.SESSIONS_FILE_PATH, "rb") as f:
        sessions = pickle.load(f)
    if not isinstance(sessions, list):
        raise Exception("Users were not loaded successfully...")
    return sessions

