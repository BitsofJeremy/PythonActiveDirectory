#!/usr/bin/env python

# Gets a AD user displayName and email

import ldap
import os

LDAP_HOST = 'ldap.example.com'
LDAP_user = os.getenv('LDAP_USER')
LDAP_password = os.getenv('LDAP_PASSWORD')


def get_user(_member):
    connection = ldap.initialize('ldap://' + LDAP_HOST)
    connection.start_tls_s()
    connection.protocol_version = 3
    connection.set_option(ldap.OPT_REFERRALS, 0)
    connection.simple_bind_s(LDAP_user, LDAP_password)

    filter = '(cn=*)'
    attrs = ['displayName', 'mail']

    results = connection.search_s(
        _member,
        ldap.SCOPE_SUBTREE,
        filter,
        attrs
    )
    # print(results)
    user_data = results[0][1]
    # Check to make sure the user has an email address
    if 'mail' in user_data.keys():
        displayName = results[0][1]['displayName'][0]
        mail = results[0][1]['mail'][0]
        user = {
            'displayName': displayName.decode("utf-8"),
            'mail': mail.decode("utf-8")
        }
        # print(user)
        return user
    else:
        # No mail no cry
        return False


if __name__ == '__main__':
    get_user()
