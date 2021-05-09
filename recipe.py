import requests
from bs4 import BeautifulSoup
import json
import html
import re

site_styles = {
  'json':['allrecipes.com', 'tasteofhome.com'],
  'printable':['foodnetwork.com']
}

class CleanRecipe:
  def __init__(self, url):
    self.url = url
    self.style = self.match_site_style()

    if self.style == 'printable':
      if 'foodnetwork.com' in self.url:
        self.url += '.recipePrint'

    response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"})
    self.soup = BeautifulSoup(response.content, "html.parser")

    self.recipe = {}

    if self.style == 'json':
      raw_json = self.extract_json_from_html() 
      self.convert_json_to_dict(raw_json, self.recipe)

      self.recipe['time'] = self.clean_time()
      self.recipe['instructions'] = self.clean_instructions()
      self.recipe['nutrition'] = self.clean_nutrition()

    elif self.style == 'printable':
      self.convert_html_to_dict(self.recipe)


  def match_site_style(self):
    pattern = r'www.(\S*.com)/'
    match = re.search(pattern, self.url)[1]
    style = [k for k,v in site_styles.items() if match in v][0]

    return style


  def html_image_to_string(self, tag=tuple): #tuple = ('tag name', {attribute: value})
    return self.soup.find(tag[0], tag[1])['src'][2:]


  def html_name_to_string(self, tag=tuple):
    return self.soup.find(tag[0], tag[1]).text.strip()


  def html_time_to_string(self, tag=tuple): 
    return self.soup.find(tag[0], tag[1]).text.strip()

  
  def html_yield_to_string(self, tag=tuple):
    content = self.soup.find(tag[0], tag[1])
    _yield = ''

    for child in content.descendants:
      if child.name == 'li':
        if 'Yield:' in child.text:
          for _ in child:
            if len(_.string) > 1 and 'Yield' not in _.string:
              return _.string.strip()

    
  def html_ingredients_to_list(self, tag=tuple):
    _list = []
    content = self.soup.find(tag[0], tag[1])
    for child in content.descendants:
      if child.name == 'li':
        _list.append(child.text)
    return _list


  def html_instructions_to_list(self, tag=tuple):
    _list = []
    content = self.soup.find_all(tag[0], tag[1])[1]
    for child in content.descendants:
      if child.name == 'p':
        _list.append(child.text)
    return _list


  def convert_html_to_dict(self, _dict):
    image_tag = ('img', {'class': 'a-Image--Food'})
    name_tag = ('span', {'class': 'o-AssetTitle__a-HeadlineText'})
    time_tag = ('span', {'class': 'o-RecipeInfo__a-Description m-RecipeInfo__a-Description--Total'})
    yield_tag = ('div', {'class': 'm-RecipeBody'})
    ingredients_tag = ('div', {'class': 'o-Ingredients__m-Body'})
    instructions_tag = ('div', {'class': 'o-Method__m-Body'})

    _dict['image'] = self.html_image_to_string(image_tag)
    _dict['name'] = self.html_name_to_string(name_tag)
    _dict['time'] = self.html_time_to_string(time_tag)
    _dict['servings'] = self.html_yield_to_string(yield_tag)
    _dict['ingredients'] = self.html_ingredients_to_list(ingredients_tag)
    _dict['instructions'] = self.html_instructions_to_list(instructions_tag)
    

  


  def extract_json_from_html(self):
    result = self.soup .find('script', {'type': 'application/ld+json'}).string
    raw_json = json.loads(html.unescape(result))

    return raw_json


  def convert_json_to_dict(self, json, _dict):
    if 'allrecipes' in self.url:
      json = json[1]

    _dict['image'] = json['image']['url']
    _dict['name'] = json['name']
    _dict['time'] = json['totalTime']
    _dict['servings'] = json['recipeYield']
    _dict['ingredients'] = json['recipeIngredient']
    _dict['instructions'] = json['recipeInstructions']
    _dict['nutrition'] = json['nutrition']
    

  def clean_instructions(self):
    data = self.recipe['instructions']
    instructions = []

    if type(data) == list:
      if 'allrecipes' in self.url:
        for item in data:
          instructions.append(item['text'].strip())
    else:
      if 'tasteofhome' in self.url:
        instructions = [_.strip() for _ in data.split(' ,')]
    
    return instructions


  def clean_nutrition(self):
    data = self.recipe['nutrition']
    nutrition = []
    if type(data) == dict:
      for key in data:
        if data[key] is not None and key.isalpha():
          if 'Content' in key:
            item = key.replace('Content','').strip()
          else:
            item = key.strip()
          nutrition.append((item, data[key]))
      
      return nutrition
    
    else:
      print('data is not dict')


  def clean_time(self):
    data = self.recipe['time']

    pattern = r'(\d*H)*(\d*M)'
    match = re.search(pattern, data)

    return match[0]


  def print_full_recipe(self):
    if 'image' in self.recipe:
      print(self.recipe['image'])
    else:
      print('No name data')

    print('\n')

    if 'name' in self.recipe:
      print(self.recipe['name'])
    else:
      print('No name data')

    print('\n')

    if 'time' in self.recipe:
      print(self.recipe['time'])
    else:
      print('No time data')

    print('\n')

    if 'servings' in self.recipe:
      print(self.recipe['servings'])
    else:
      print('No servings data')

    print('\n')

    if 'ingredients' in self.recipe:
      print(*self.recipe['ingredients'], sep='\n')
    else:
      print('No ingredients data')

    print('\n')

    if 'instructions' in self.recipe:  
      print(*self.recipe['instructions'], sep='\n')
    else:
      print('No instructions data')
    
    print('\n')

    if 'nutrition' in self.recipe:
      for item, value in self.recipe['nutrition']:
        print(item + ': ' + value)
    else:
      print('No nutrition data')