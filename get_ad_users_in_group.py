#!/usr/bin/env python

# Gets all users in a group and return a list of user emails

# imports
from ldap3 import Connection, SUBTREE
import os
from get_user_by_ad_obj import get_user

LDAP_HOST = 'ldap.example.com'
LDAP_user = os.getenv('LDAP_USER')
LDAP_password = os.getenv('LDAP_PASSWORD')


def get_users(ldap_base_dn):
    """ Takes a group and spits out a user list of emails. """

    conn = Connection(
        LDAP_HOST,
        user=LDAP_user,
        password=LDAP_password,
        auto_bind=True,
        auto_range=True,
    )
    conn.start_tls()
    _filter = '(cn=*)'
    conn.search(
        ldap_base_dn,
        _filter,
        SUBTREE,
        attributes='member'
    )
    # print(conn.response)
    users = conn.response[0]['raw_attributes']['member']
    # print(len(users))
    # Make a list of emails
    user_list = []
    print("Converting user DNs to emails via AD. Please be patient.")
    for user in users:
        u = get_user(_member=user.decode("utf-8"))
        if u:
            user_list.append(u)

    print(f"Pulled {len(user_list)} users from list.")
    return user_list
