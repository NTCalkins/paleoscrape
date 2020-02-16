#!/usr/bin/env py3.7

# Nicholas Calkins
# January 9th, 2020
# This is a program for scraping paleoleap.com

import requests
from bs4 import BeautifulSoup

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_recipe(suburl):
    URL = 'https://paleoleap.com/' + suburl
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    servings = soup.body.find(class_="meta-servings")
    prep_time = soup.body.find(class_="meta-prep-time")
    cook_time = soup.body.find(class_="meta-cook-time")

    #Case for certain pages, where the data is not under the meta heading
    if servings == None:
        servings1 = soup.body.find("article")
        servings2 = servings1.find_all("span")

        servings = servings2[0]
        prep_time = servings2[1]
        cook_time = servings2[2]

    ingredients = soup.body.find_all("li", itemprop="ingredients")

    for ingredient in ingredients:
        print(ingredient.getText())

    instructions = soup.body.find("ol", itemprop="recipeInstructions")
    steps = instructions.find_all("li")

    for step in steps:
        print(step.getText())

    protein = soup.body.find(class_="protein-value")
    fat = soup.body.find(class_="fat-value")
    carbs = soup.body.find(class_="carbs-value")

    print(servings.getText())    
    print(prep_time.getText())
    print(cook_time.getText())

    print(protein.getText() + " grams of protein")
    print(fat.getText() + " grams of fat")
    print(carbs.getText() + " grams of carbohydrates")


def get_suburl():
    suburl = input ("enter the recipe with no hyphens: ")
    suburl_list = suburl.split(" ")
    for word in suburl_list:
        if word == "and" or word == "with":
            suburl_list.remove(word)
    suburl = "-".join(suburl_list)
    return suburl

def main():
    suburl = get_suburl()
    get_recipe(suburl)


if __name__ == "__main__":
    main()
