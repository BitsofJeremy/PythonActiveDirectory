#!/usr/local/bin/python

# Gets an AD user via email

import argparse
import ldap
import os
import sys

LDAP_HOST = 'ldap.example.com'
LDAP_user = os.getenv('LDAP_USER')
LDAP_password = os.getenv('LDAP_PASSWORD')


def get(**kwargs):
    connection = ldap.initialize('ldap://' + LDAP_HOST)
    connection.start_tls_s()
    connection.protocol_version = 3
    connection.set_option(ldap.OPT_REFERRALS, 0)
    connection.simple_bind_s(LDAP_user, LDAP_password)

    # Base DN of your directory
    LDAP_BASE_DN = 'ou=All Users,dc=ad,dc=example,dc=com'
    # filter for user
    user_email = kwargs.get('email')
    filter = '(mail={0})'.format(user_email)
    # attrs = ['member']
    try:
        results = connection.search_s(LDAP_BASE_DN, ldap.SCOPE_SUBTREE, filter)
    except ldap.NO_SUCH_OBJECT:
        print("USER NOT FOUND")
        return False
    except ldap.CONNECT_ERROR:
        print("LDAP CONNECTION ERROR")
        sys.exit("LDAP CONNECTION ERROR")

    # print(results)
    if results:
        # print("Found the user")
        user_email = bytes.decode(results[0][1]['mail'][0])
        user_firstname = bytes.decode(results[0][1]['givenName'][0])
        user_lastname = bytes.decode(results[0][1]['sn'][0])

        user_dict = {
            'email': user_email,
            'firstname': user_firstname,
            'lastname': user_lastname
        }
        print(user_dict)
        return True
    else:
        print('USER_NOT_FOUND')
        return False


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-e', action='store', dest='email',
                        help='Enter the user email', required=True)

    args = parser.parse_args()

    # Convert the argparse.Namespace to a dictionary: vars(args)
    arg_dict = vars(args)
    # pass dictionary to delete_sub
    get(**arg_dict)
    sys.exit(0)
