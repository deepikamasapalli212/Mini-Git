import hashlib
import time
import uuid


class Commit:
    def __init__(self, message, files, parent=None, branch="main"):
        self.id = self.generate_id(message)
        self.message = message
        self.files = files.copy()
        self.parent = parent
        self.branch = branch
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    def generate_id(self, message):
        return hashlib.sha1((message + str(time.time())).encode()).hexdigest()[:7]


class MiniGit:

    def __init__(self):

        self.working_directory = {}
        self.staging_area = {}

        self.commits = {}
        self.branches = {"main": None}

        self.current_branch = "main"
        self.head = None


    # add file
    def add(self, filename, content):

        self.working_directory[filename] = content
        self.staging_area[filename] = content

        print(f"Added '{filename}' to staging area")


    # commit changes
    def commit(self, message):

        if not self.staging_area:
            print("Nothing to commit")
            return

        parent_commit = self.head

        new_files = {}

        if parent_commit:
            new_files = self.commits[parent_commit].files.copy()

        new_files.update(self.staging_area)

        new_commit = Commit(
            message,
            new_files,
            parent_commit,
            self.current_branch
        )

        self.commits[new_commit.id] = new_commit

        self.head = new_commit.id
        self.branches[self.current_branch] = new_commit.id

        self.staging_area.clear()

        print(f"Committed: {new_commit.id} - {message}")


    # show log
    def log(self):

        commit_id = self.head

        while commit_id:

            commit = self.commits[commit_id]

            print(f"\nCommit: {commit.id}")
            print(f"Branch: {commit.branch}")
            print(f"Message: {commit.message}")
            print(f"Time: {commit.timestamp}")

            commit_id = commit.parent


    # checkout commit
    def checkout(self, commit_id):

        if commit_id not in self.commits:
            print("Commit not found")
            return

        commit = self.commits[commit_id]

        self.working_directory = commit.files.copy()
        self.head = commit_id

        print(f"Checked out commit {commit_id}")


    # create branch
    def create_branch(self, branch_name):

        if branch_name in self.branches:
            print("Branch already exists")
            return

        self.branches[branch_name] = self.head

        print(f"Branch '{branch_name}' created")


    # switch branch
    def switch_branch(self, branch_name):

        if branch_name not in self.branches:
            print("Branch not found")
            return

        self.current_branch = branch_name
        self.head = self.branches[branch_name]

        if self.head:
            self.working_directory = self.commits[self.head].files.copy()

        print(f"Switched to branch '{branch_name}'")


    # show branches
    def show_branches(self):

        print("\nBranches:")

        for branch in self.branches:

            marker = "* " if branch == self.current_branch else "  "

            print(marker + branch)


    # show files
    def show_files(self):

        print("\nWorking Directory Files:")

        for file, content in self.working_directory.items():
            print(f"{file}: {content}")


# Interactive system
git = MiniGit()

print("=== Mini Git Version Control System ===")

while True:

    print("\nCommands:")
    print("1. add")
    print("2. commit")
    print("3. log")
    print("4. checkout")
    print("5. branch")
    print("6. switch")
    print("7. branches")
    print("8. files")
    print("9. exit")

    cmd = input("Enter command: ")

    if cmd == "1":

        filename = input("Filename: ")
        content = input("Content: ")

        git.add(filename, content)


    elif cmd == "2":

        message = input("Commit message: ")
        git.commit(message)


    elif cmd == "3":

        git.log()


    elif cmd == "4":

        commit_id = input("Enter commit id: ")
        git.checkout(commit_id)


    elif cmd == "5":

        branch = input("Branch name: ")
        git.create_branch(branch)


    elif cmd == "6":

        branch = input("Branch name: ")
        git.switch_branch(branch)


    elif cmd == "7":

        git.show_branches()


    elif cmd == "8":

        git.show_files()


    elif cmd == "9":

        break


    else:

        print("Invalid command")