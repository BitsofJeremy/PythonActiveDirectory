# Python Active Directory

Working with Microsoft Active Directory users and groups via Python

## Setup

Clone the repo

    git clone https://gitlab.com/deafmice/pythonactivedirectory.git

Setup Virtualenv

    virtualenv -p python3 venv

Activate the venv

    source venv/bin/activate

Install Requirements

    pip install -r requirements.txt

Edit and copy env-example to .env

[Note: You will need a Active Directory user with correct permissions]

    cp env-example .env

Source .env

    source .env

# Run it

## get_ad_user_by_email.py

Returns a dictionary with email, first name, and last name.  This can be extended to any AD attribute you desire.

    python get_ad_user_by_email.py -e user@example.com

## get_user_by_ad_obj.py

This script grabs a user's info from AD via their NT object. It is meant to be imported into other scripts and run `get_user(member object)` to pull info from AD.


## get_ad_users_in_group.py

Takes a group and spits out a user list of emails. It is meant to be imported into other scripts and run `get_users(ldap_base_dn)` to pull a list of emails from an AD group [Think mail list].

[Requires: `get_user_by_ad_obj.py`]

## add_user_to_ldap_group.py

This one uses the `ldap3` module to add a user to the specified group. It finds the user via email, adds them to a provided group DN.

    python add_user_to_ldap_group.py -e user@example.com -l "cn=MyGroup,ou=All Users,dc=ad,dc=example,dc=com"

[Note: Your user in `.env` needs to be the 'native owner' of the group, not just a admin]

