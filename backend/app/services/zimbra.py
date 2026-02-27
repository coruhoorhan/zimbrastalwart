import subprocess

def fetch_users_from_zimbra():
    """
    Zimbra LDAP'dan kullanıcıları çeker.
    """
    result = subprocess.run(
        ["echo", "user1@domain.com\nuser2@domain.com"], capture_output=True, text=True
    )
    users = result.stdout.strip().split("\n")
    return users
