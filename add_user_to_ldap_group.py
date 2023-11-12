import argparse
from ldap3 import Server, Connection, ALL, NTLM
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups
import os
import sys

# VARS
LDAP_SERVER = 'ldap.example.com'
# The 'native owner' of mail list group, not just admin
LDAP_USER = os.getenv('LDAP_USER')
LDAP_PASSWORD = os.getenv('LDAP_PASSWORD')


def add_user(**kwargs):
    """ Finds user via email, adds them to a email communication group."""
    # User OU to search, generally in All Users OU
    all_users_ou = 'ou=All Users,dc=ad,dc=example,dc=com'
    # Build the connection
    server = Server(
        LDAP_SERVER,
        get_info=ALL
    )
    conn = Connection(
        server,
        user=LDAP_USER,
        password=LDAP_PASSWORD,
        authentication=NTLM
    )
    # Bind to AD, should return True if connected
    my_connection = conn.bind()

    if my_connection:
        # Get the user DN
        conn.search(
            all_users_ou, f"(mail={kwargs.get('email')})")
        # This should only return one user,
        # so we act on the first entry.
        user = conn.entries[0].entry_dn
        # print(user)

        # Add the user to the mail_list group
        try:
            add_users = ad_add_members_to_groups(
                connection=conn,
                members_dn=user,
                groups_dn=kwargs.get('mail_list')
            )
            return True
        except Server as e:
            print(e)
            return False
    else:
        print("Connection to LDAP server failed.")
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-e',
        action='store',
        dest='email',
        help='Enter the users email address',
        required=True
    )

    parser.add_argument(
        '-l',
        action='store',
        dest='mail_list',
        help='Enter the mail list DN',
        required=True
    )

    args = parser.parse_args()

    # Convert the argparse.Namespace to a dictionary: vars(args)
    arg_dict = vars(args)
    # pass dictionary to add_sub
    add_user(**arg_dict)
    sys.exit(0)
