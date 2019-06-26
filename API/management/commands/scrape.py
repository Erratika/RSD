from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import re
from API.models import *
from _datetime import datetime


class Command(BaseCommand):

    def getReleaseDate(self, source):
        try:
            return datetime.strptime(source.find("th", text="Release date\n").find_next("td").text.strip(' (Update)\n'),
                                     '%d %B %Y')
        except AttributeError:
            if re.match("^Recipe for Disaster:", self.getTitle(source)):
                return datetime(2006, 3, 15, 0, 0)
            elif re.match("^Dimension of Disaster:",self.getTitle(source)):
                return datetime(2015, 3, 23, 0, 0)
            else:
                return datetime.now()

    def getDifficulty(self, source):
        return source.find("th", text=re.compile("Official difficulty(\n)?")).find_next("td").text.strip()

    def isMemebersOnly(self, source):
        try:
            return source.find("a", attrs={"href": "/w/Members"}).find_next("td").text.replace("\n", "") == "Yes"
        except AttributeError:
            return source.find("th", text="Member requirement").find_next("td").text == " Memebrs only"

    def getAge(self, source):
        try:
            return source.find("a", attrs={"href": "/w/History"}).find_next("td").text.strip()
        except AttributeError:
            if re.match("^Recipe for Disaster:", self.getTitle(source)):
                return "Fifth Age"
            elif re.match("^Dimension of Disaster:", self.getTitle(source)):
                return "Sixth Age"
            else:
                return "Ambiguous"

    def getSeries(self):
        return

    def getTitle(self, source):
        try:
            return source.find('th', attrs={"class": "infobox-header"}).contents[0]
        except AttributeError:
            return source.find("h1", attrs={"id":"firstHeading", "class":"firstHeading"}).text

    # Ignore for now not really necessary
    # def getID(self, source):
    #     return source.find('th', attrs={"class": "infobox-header"}).contents[1].text

    def getQuestReqs(self, source):
        quest_reqs = source.find("table", attrs={"class": "questreq"})
        # List required quests
        quests = []
        if quest_reqs:
            quest_items = quest_reqs.find_next("tr").find_next("ul").find_next("ul").find_all("li",
                                                                                              recursive=False)

            for req_q in quest_items:
                quest_link = req_q.find("a")

                # Chef's assistant doesnt have normal requirements page on wiki
                if quest_link:
                    quest_title = quest_link.text
                    if not re.match("quest points",quest_title):
                        quests.append(quest_title)
        return quests

    def getSkillReqs(self, source):
        quest_details = source.find("td", attrs={"class": "questdetails-info qc-active"})
        skill_reqs = dict()
        if quest_details:
            reqs_list = quest_details.find_all("li")
            for reqs in reqs_list:
                if re.match('^[0-9]*  [A-z](.*)$', reqs.text):
                    level = reqs.text.split("  ")[0]
                    skill = reqs.text.split("  ")[1].split(' ', 1)[0]
                    try:
                        skill_reqs[skill] = max(level, skill_reqs[skill])
                    except KeyError:
                        skill_reqs[skill] = level
        return skill_reqs

    def getQuestPoints(self, source):
        # TODO Improve? Assumes last quest point link is reward and not a quest req
        return int(source.find_all('a', href="/w/Quest_points")[-1].parent.contents[0])

    def getLength(self, source):
        return source.find('th', text="Official length").find_next('td').text

    def handle(self, *args, **options):
        url = "https://apps.runescape.com/runemetrics/quests?user=Erratika"
        response = requests.get(url)
        data = response.json()

        failed_list = []
        quest_list = []

        for q in data['quests']:
            if "(miniquest)" not in q['title'] and "(saga)" not in q['title']:
                if q['title'] == "Dig Site":
                    altered_name = "The_Dig_Site"
                elif q['title'] == "Fremennik Isles":
                    altered_name = "The_Fremennik_Isles"
                elif q['title'] == "Tears of Guthix":
                    altered_name = "Tears_of_Guthix_(quest)"
                elif q['title'] == "The Watchtower":
                    altered_name = "Watchtower"
                elif q['title'] == "Fur 'n Seek":
                    altered_name = "Fur_%27n%27_Seek"
                elif q['title'] == "A Fairy Tale III - Battle at Ork's Rift":
                    altered_name = "Fairy_Tale_III_-_Battle_at_Ork%27s_Rift"
                elif q['title'] == "A Fairy Tale I - Growing Pains":
                    altered_name = "Fairy_Tale_I_-_Growing_Pains"
                elif q['title'] == "Recipe for Disaster: Freeing the Goblin Generals":
                    altered_name = "Recipe_for_Disaster:_Freeing_the_Goblin_generals"
                elif q['title'] == "Recipe for Disaster: Freeing the Mountain Dwarf":
                    altered_name = "Recipe_for_Disaster:_Freeing_the_Mountain_dwarf"
                elif q['title'] == "Unstable Foundations":
                    continue
                else:
                    altered_name = q['title'].replace(' ', '_')
                # print("VISITING https://runescape.wiki/w/" + altered_name)
                response = requests.get("https://runescape.wiki/w/" + altered_name)
                data = response.text

                # Check if request was successful
                if response.status_code != 200:
                    print('Failed to get ' + q['title'])
                    failed_list.append(q['title'])
                else:
                    soup = BeautifulSoup(data, features="html.parser")
                    if not soup:
                        print(q['title'])
                    quest = {'title': q['title'],
                             'difficulty': self.getDifficulty(soup),
                             'series': self.getSeries(),
                             'length': self.getLength(soup),
                             'age': self.getAge(soup),
                             'members': self.isMemebersOnly(soup),
                             'questPoints': self.getQuestPoints(soup),
                             'release': self.getReleaseDate(soup),
                             'skillReqs': self.getSkillReqs(soup),
                             'questReqs': self.getQuestReqs(soup)
                             }
                    quest_list.append(quest)

        quest_list.sort(key=lambda qu: (qu['release']))
        for item in quest_list:
            print(item)
            obj, created = Quests.objects.update_or_create(
                title=item['title'],
                difficulty=Difficulties.objects.get(difficulty__iexact=item['difficulty']),
                length=Lengths.objects.get(length__iexact=item['length']),
                age=Ages.objects.get(age__iexact=item['age']),
                members=item['members'],
                questPoints=item['questPoints'],
                release_date=item['release']
            )

            #       THIS ADDS QUESTS TO REQUIRED QUESTS COL

            for rq in item['questReqs']:
                try:
                    obj.required_quests.add(Quests.objects.get(title=rq))
                except Quests.DoesNotExist:
                    pass
            for rs,rl in item['skillReqs'].items():
                try:
                    obj.required_skills.add(SkillRequirements.objects.get(skill__skill_name__iexact=rs, level__exact=rl))
                except SkillRequirements.DoesNotExist:
                    print("Skill req doesnt exist.")



