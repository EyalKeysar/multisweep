REPO_PATH = './Server/accounts_repo.txt'

class RepoAPI():
    def __init__(self, repo_path=REPO_PATH):
        self.repo_path = repo_path

    def add_account(self, name, password, email):

        if(self.get_account_by_name(name) != None):
            return False

        # Format the account information
        account_info = f"\n{name};{password};{email}"

        # Append the account information to the text file
        with open(self.repo_path, 'a') as file:
            file.write(account_info)

        file.close()
        return True

    def get_account_by_name(self, name):
        # Search for the account by name in the text file
        with open(self.repo_path, 'r') as file:
            for line in file:
                account_info = line.strip().split(';')
                if account_info[0] == name:
                    file.close()
                    return {'name': account_info[0], 'password': account_info[1], 'email': account_info[2]}
        file.close()
        return None

    def check_account_password(self, name, password):
        # Search for the account by name in the text file
        with open(self.repo_path, 'r') as file:
            for line in file:
                account_info = line.strip().split(';')
                if account_info[0] == name:
                    file.close()
                    return account_info[1] == password
        file.close()
        return False

    def get_account_by_email(self, email):
        # Search for the account by email in the text file
        with open(self.repo_path, 'r') as file:
            for line in file:
                account_info = line.strip().split(';')
                if account_info[2] == email:
                    file.close()
                    return {'name': account_info[0], 'password': account_info[1], 'email': account_info[2]}
        file.close()
        return None

    def list_all_accounts(self):
        # Read all accounts from the text file
        accounts = []
        with open(self.repo_path, 'r') as file:
            for line in file:
                account_info = line.strip().split(';')
                accounts.append({'name': account_info[0], 'password': account_info[1], 'email': account_info[2]})
        file.close()
        return accounts