#!/usr/bin/env python3

import recipe
import re

def main(url):  
  site_types = {
    'json':['allrecipes.com', 'tasteofhome.com'],
    'html':['foodnetwork.com']
  }

  key = match_site_type(url, site_types)
  if key == 'json':
    clean_recipe = recipe.CleanRecipe_JSON(url)
  elif key == 'html':
    clean_recipe = recipe.CleanRecipe_HTML(url)

  return clean_recipe


def match_site_type(url, types):
  pattern = r'www.(\S*.com)/'
  match = re.search(pattern, url)[1]
  key = [k for k,v in types.items() if match in v][0]

  return key


def print_full_recipe(recipe=dict):
  if 'image' in recipe:
    print(recipe['image'])
  else:
    print('No name data')

  print('\n')

  if 'name' in recipe:
    print(recipe['name'])
  else:
    print('No name data')

  print('\n')

  if 'time' in recipe:
    print(recipe['time'])
  else:
    print('No time data')

  print('\n')

  if 'servings' in recipe:
    print(recipe['servings'])
  else:
    print('No servings data')

  print('\n')

  if 'ingredients' in recipe:
    print(*recipe['ingredients'], sep='\n')
  else:
    print('No ingredients data')

  print('\n')

  if 'instructions' in recipe:  
    print(*recipe['instructions'], sep='\n')
  else:
    print('No instructions data')
  
  print('\n')

  if 'nutrition' in recipe:
    for item, value in recipe['nutrition']:
      print(item + ': ' + value)
  else:
    print('No nutrition data')


if __name__ == "__main__":
  #url = 'https://www.tasteofhome.com/recipes/scottish-shortbread/'
  #url = 'https://www.allrecipes.com/recipe/280721/instant-pot-shrimp-and-broccoli/'
  url = 'https://www.foodnetwork.com/recipes/food-network-kitchen/black-eyed-pea-soup-3361891'

  clean_recipe = main(url)
  print_full_recipe(clean_recipe.info)