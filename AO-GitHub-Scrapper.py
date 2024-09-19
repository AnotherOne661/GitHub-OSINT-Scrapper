import requests
from bs4 import BeautifulSoup

BASE_URL = "https://github.com/{}"


# Function to separate
def separator():
  print("-" * 51)

#Function to get the user info
def usr_info(username):
  final_url = BASE_URL.format(username)
  response = requests.get(final_url)
  if not response.ok:
    print("Something went wrong")
    return

  soup = BeautifulSoup(response.text, "html.parser")

  bio = soup.find("div", {"class" : "p-note user-profile-bio mb-3 js-user-profile-bio f4"})
  print("Bio: ")
  print(bio.text.strip())

  separator()

def get_repos(username):
  follower_repo_url = BASE_URL.format(username) + "?tab=repositories"

  repos_response = requests.get(follower_repo_url)
  if not repos_response.ok:
    print("Something went wrong getting the repositories of " + username)
    return
  
  repo_soup = BeautifulSoup(repos_response.text, "html.parser")

  all_repos = repo_soup.find_all("a", {"itemprop" : "name codeRepository"})
  if not all_repos:
        print(f"No repositories found for {username}")
        return

  for repo in all_repos:
      print("Public repositories: ")
      print(repo.text.strip())
      separator()





def followers(username) :

  followers_url = BASE_URL.format(username) + "?tab=followers"
  
  followers_response = requests.get(followers_url)

  if not followers_response.ok:
    print("Something went wrong while getting the followers")
    return
  
  followers_soup = BeautifulSoup(followers_response.text, "html.parser")

  followers_all = followers_soup.find_all("a", {"class" : "d-inline-block no-underline mb-1"})

  if not followers_all:
    print("No followers found")
    return

  for follower in followers_all:
    print("Follower:")
    print(follower.text)

    follower_href = follower.get("href")
    follower_username = follower_href.strip("/")
    

    separator()
    separator()
    get_repos(follower_username)





def main():
  username = input("Introduce the victim's username: ")
  usr_info(username)
  followers(username)
  

if __name__ == "__main__" :
  main()


