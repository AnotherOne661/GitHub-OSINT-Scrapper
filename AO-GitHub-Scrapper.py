import requests
from bs4 import BeautifulSoup

BASE_URL = "https://github.com/{}"

final_array = []


# Function to separate
def separator():
    print("-" * 51)


# Function to get the user info
def usr_info(username):
    final_url = BASE_URL.format(username)
    response = requests.get(final_url)
    if not response.ok:
        print("Something went wrong")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    bio = soup.find(
        "div", {"class": "p-note user-profile-bio mb-3 js-user-profile-bio f4"}
    )
    print("Bio: ")
    print(bio.text.strip())

    separator()


def get_repos(username):
    follower_repo_url = BASE_URL.format(username) + "?tab=repositories"
    
    repo_array = []
    

    repos_response = requests.get(follower_repo_url)
    if not repos_response.ok:
        print("Something went wrong getting the repositories of " + username)
        return

    repo_soup = BeautifulSoup(repos_response.text, "html.parser")

    all_repos = repo_soup.find_all("a", {"itemprop": "name codeRepository"})
    if not all_repos:
        print(f"No repositories found for {username}")
        return

    for repo in all_repos:
        print("Public repositories: ")
        print(repo.text.strip())
        separator()
        
        repo_array.append(repo.text.strip())
        final_array.append(repo.text.strip())
    



def followers(username):

    followers_url = BASE_URL.format(username) + "?tab=followers"

    followers_response = requests.get(followers_url)

    followers_array = []

    if not followers_response.ok:
        print("Something went wrong while getting the followers")
        return

    followers_soup = BeautifulSoup(followers_response.text, "html.parser")

    followers_all = followers_soup.find_all(
        "a", {"class": "d-inline-block no-underline mb-1"}
    )

    if not followers_all:
        print("No followers found")
        return

    for follower in followers_all:
        print("Follower:")
        print(follower.text)

        follower_href = follower.get("href")
        follower_username = follower_href.strip("/")

        separator()

        followers_array.append(follower.text.strip())
        final_array.append(follower.text.strip())
        
        get_repos(follower_username)

        

   # writefile("".join(followers_array), "Users")


def writefile(cont, name):
    with open(name, "w", encoding="utf-8") as f:
        f.write(cont)
        


def menu():
    
    flag = False
    ans = 0
    
    while not flag:
        print("Please, select the option you want to run")    
        print("1. Enter username to search repository information")
        print("2. Enter username to search information about the target")
        print("3. To leave")
        ans = int(input("Select your answer: "))
        match ans:
            case 1:
                username = input("Introduce the victim's username: ")
                usr_info(username)
                followers(username)
                filename = input("If you want to save this into a file, give it a name, if you don't, press Enter")
                if filename:
                    writefile("\n".join(final_array),filename)
                input("Press enter to continue")
            case 2:
                print("ta")
                input("Press enter to continue")
            case 3:
                print("See you soon")
                flag = True
            case _:
                print("An unrecognised option was given, please, select a valid one")
                menu()


def main():
   menu()
    # writefile()


if __name__ == "__main__":
    main()
