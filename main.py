#!/usr/bin/env python3

import recipe


def main():
#   #URL = 'https://www.tasteofhome.com/recipes/scottish-shortbread/'
#   #URL = 'https://www.allrecipes.com/recipe/280721/instant-pot-shrimp-and-broccoli/'
  URL = 'https://www.foodnetwork.com/recipes/food-network-kitchen/black-eyed-pea-soup-3361891'

  new_recipe = recipe.CleanRecipe(URL)
  new_recipe.print_full_recipe()


if __name__ == "__main__":
  main()