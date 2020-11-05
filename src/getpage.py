from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import json

userhandle = "vivekshah1801"
useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"

profile_url = f"https://www.codechef.com/users/{userhandle}"

session = requests.session()
session.headers.update({'User-Agent': useragent})    

def getSolved(profile_url):
    page = session.get(profile_url).text
    profile_soup = BeautifulSoup(page,features = "lxml")

    problem_solved_soup = profile_soup.select(".problems-solved")[0].find_all("article")
    problem_solved_categories = profile_soup.find_all("h5")

    categories = len(problem_solved_categories)
    if categories == 2:
        fullysolved = problem_solved_soup[0]
        partiallysolved = problem_solved_soup[1]
    elif categories == 1:
        if problem_solved_categories[0].text.startwith("Fully Solved"):
            fullysolved = problem_solved_soup[0]
        else:
            partiallysolved = problem_solved_soup[0]
    else:
        raise ValueError("No Problem section Found on profile")

    # for fully solved problems:
    solved_fully = {}
    contests = fullysolved.find_all("p")
    for contest in contests:
        contest_name = contest.find("strong").text[:-1]
        contest_problems = contest.find("span").find_all("a")
        solved_fully[contest_name] = []
        for problem in contest_problems:
            solved_fully[contest_name].append(problem.text)

    # for partially solved problems:
    solved_part = {}
    contests = partiallysolved.find_all("p")
    for contest in contests:
        contest_name = contest.find("strong").text[:-1]
        contest_problems = contest.find("span").find_all("a")
        solved_part[contest_name] = []
        for problem in contest_problems:
            solved_part[contest_name].append(problem.text)
    print(len(solved_fully), len(solved_part))
    return solved_fully, solved_part


def getSolutions(solutions_url):
    page = session.get(solutions_url).text
    soup = BeautifulSoup(page,features = "lxml")
    return soup

class Solution:
    def __init__(self, tr_tag):
        fields = tr_tag.find_all("td")
        print(fields)
    
def getSolutionObj(tr_tag):
    return Solution(tr_tag)

try:
    solved_fully, solved_part = getSolved(profile_url)
    # saving practice fully solved
    if 'Practice' in solved_fully.keys():
        problems = solved_fully['Practice']
        for problem in problems:
            solutions_url = f"https://www.codechef.com/status/{problem},{userhandle}"
            # print(solutions_url)
            solutions = getSolutions(solutions_url).select("table.dataTable tbody")[0].find_all("tr")
            solutions_list = []
            for solution in solutions:
                solutions_list.append(getSolutionObj(solution))
            # dev-remove
            break
except Exception as e:
    raise e


