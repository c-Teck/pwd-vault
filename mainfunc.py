
from secret import get_secret_key
from Menu import menu, create, find, find_accounts, Update
from database-manager import connect

# menu
# 1. create new password for a site
# 2. find password for a site
# 3. Find all sites connected to an email

secret = get_secret_key()

passw = input('[+] Please provide the master password to start using your password vault manager : ')

if passw == secret:
    print('>>>\n>>>\n>>>\n [+] Successfully Authenticated...')

else:
    print('no luck')
    exit()

choice = menu()
while choice != 'Q':
    if choice == '1':
        create()
    if choice == '2':
        find_accounts()
    if choice == '3':
        find()
    if choice == '4' :
        Update()
    if choice == '6' :
        print('[+] Relax we are working on this update soon...')
    if choice == '7' :
        print(' [+] This update will be rolled over soon....')
    else:
        choice = menu()
exit()
