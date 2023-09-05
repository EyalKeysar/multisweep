

class RepoAPI():
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def add_account(self, name, password, email):
        # Format the account information
        account_info = f"{name};{password};{email}\n"

        # Append the account information to the text file
        with open(self.repo_path, 'a') as file:
            file.write(account_info)

    def get_account_by_name(self, name):
        # Search for the account by name in the text file
        with open(self.repo_path, 'r') as file:
            for line in file:
                account_info = line.strip().split(';')
                if account_info[0] == name:
                    return {'name': account_info[0], 'password': account_info[1], 'email': account_info[2]}
        return None

    def get_account_by_email(self, email):
        # Search for the account by email in the text file
        with open(self.repo_path, 'r') as file:
            for line in file:
                account_info = line.strip().split(';')
                if account_info[2] == email:
                    return {'name': account_info[0], 'password': account_info[1], 'email': account_info[2]}
        return None

    def list_all_accounts(self):
        # Read all accounts from the text file
        accounts = []
        with open(self.repo_path, 'r') as file:
            for line in file:
                account_info = line.strip().split(';')
                accounts.append({'name': account_info[0], 'password': account_info[1], 'email': account_info[2]})
        return accounts