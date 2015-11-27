"""
A text adventure engine for willchatterr

Based on "Text Adventure Demo" by Al Sweigart (al@inventwithpython.com)
at https://github.com/totalgood/textadventuredemo
forked from https://github.com/asweigart/textadventuredemo
techniques and snippets from http://inventwithpython.com/blog/2014/12/11/
making-a-text-adventure-game-with-the-cmd-and-textwrap-python-modules/
"""
from __future__ import print_function
import json
world = json.load(open('demo.json', 'r'))

state = world['state']
THINGS = world['things']

"""
First, we will create some data structures for our game world.

Here's a 2-D "embedding" of the game world. An embedding is just a projection
that preserves connections and distances in a small number of dimensions, usually 2 or
3. This is 2-D embedding so it's just a flat map like you'd see in a D&D Dungeon Master's
play book.

        +---------+    +---------+
        | Thief   O    | Bakery  |
        | Guild   |    |         |
+------++------O--+    +----O----+
| Used |
|Anvils|        Town Square     +--------+
|      O                        |Obs Deck|
+------++----O----+    +----O----/  /
        | Black-  O    | Wizard /  /
        | smith   |    | Tower    /
        +---------+    +---------+
"""


"""
These constant variables are used because if I mistype them, Python will
immediately throw up an error message since no variable with the typo
name will exist. If we mistyped the strings, the bugs that it produces
would be harder to find.
"""
DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
UP = 'up'
DOWN = 'down'
GROUND = 'ground'
SHOP = 'shop'
GROUNDDESC = 'grounddesc'
SHORTDESC = 'shortdesc'
LONGDESC = 'longdesc'
TAKEABLE = 'takeable'
EDIBLE = 'edible'
DESCWORDS = 'descwords'

SCREEN_WIDTH = 80

"""
The game world data is stored in a dictionary (which itself has dictionaries
and lists). Python's normal rules of indentation are suspended when typing out
a dictionary value until it encounters the closing curly brace, which is
helpful for us to make the dictionary value readable.

Each dictionary value inside the world variable is a different area in the
game world. The key is a string (i.e. 'Town Square') that is the reference
name of the location. It will also be displayed as the title of the area.

The value is another dictionary, which has keys 'desc', 'north', 'south',
'east', 'west', 'up', 'down', 'shop', and 'ground'. We use the constant
variables (e.g. DESC, NORTH, etc.) instead of strings in case we make
typos.

DESC is a text description of the area. SHOP, if it exists, is a list of
items that can be bought at this area. (We don't implement money in this
program, so everything is free.) GROUND is a list of items that are on
the ground in this area. The directions (NORTH, SOUTH, UP, etc.) are the
areas that exist in that direction.
"""
"""
These variables track where the player is and what is in their inventory.
The value in the location variable will always be a key in the world variable
and the value in the inventory list will always be a key in the THINGS
variable.
"""
location = 'Town Square' # start in town square
inventory = ['README Note', 'Sword', 'Donut'] # start with blank inventory
showFullExits = True

import cmd, textwrap

def displayLocation(loc):
    """A helper function for displaying an area's description and exits."""
    # Print the room name.
    print(loc)
    print('=' * len(loc))

    # Print the room's description (using textwrap.wrap())
    print('\n'.join(textwrap.wrap(state[loc][DESC], SCREEN_WIDTH)))

    # Print all the items on the ground.
    if len(state[loc][GROUND]) > 0:
        print()
        for item in state[loc][GROUND]:
            print(THINGS[item][GROUNDDESC])

    # Print all the exits.
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
        if direction in state[loc].keys():
            exits.append(direction.title())
    print()
    if showFullExits:
        for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
            if direction in state[location]:
                print('%s: %s' % (direction.title(), state[location][direction]))
    else:
        print('Exits: %s' % ' '.join(exits))


def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global location

    if direction in state[location]:
        print('You move to the %s.' % direction)
        location = state[location][direction]
        displayLocation(location)
    else:
        print('You cannot move in that direction')


def getAllDescWords(itemList):
    """Returns a list of "description words" for each item named in itemList."""
    itemList = list(set(itemList)) # make itemList unique
    descWords = []
    for item in itemList:
        descWords.extend(THINGS[item][DESCWORDS])
    return list(set(descWords))

def getAllFirstDescWords(itemList):
    """Returns a list of the first "description word" in the list of
    description words for each item named in itemList."""
    itemList = list(set(itemList)) # make itemList unique
    descWords = []
    for item in itemList:
        descWords.append(THINGS[item][DESCWORDS][0])
    return list(set(descWords))

def getFirstItemMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    for item in itemList:
        if desc in THINGS[item][DESCWORDS]:
            return item
    return None

def getAllItemsMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    matchingItems = []
    for item in itemList:
        if desc in THINGS[item][DESCWORDS]:
            matchingItems.append(item)
    return matchingItems

class TextAdventureCmd(cmd.Cmd):
    prompt = '\n> '

    # The default() method is called when none of the other do_*() command methods match.
    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    # A very simple "quit" command to terminate the program:
    def do_quit(self, arg):
        """Quit the game."""
        return True # this exits the Cmd application loop in TextAdventureCmd.cmdloop()

    def help_combat(self):
        print('Combat is not implemented in this program.')


    # These direction commands have a long (i.e. north) and show (i.e. n) form.
    # Since the code is basically the same, I put it in the moveDirection()
    # function.
    def do_north(self, arg):
        """Go to the area to the north, if possible."""
        moveDirection('north')

    def do_south(self, arg):
        """Go to the area to the south, if possible."""
        moveDirection('south')

    def do_east(self, arg):
        """Go to the area to the east, if possible."""
        moveDirection('east')

    def do_west(self, arg):
        """Go to the area to the west, if possible."""
        moveDirection('west')

    def do_up(self, arg):
        """Go to the area upwards, if possible."""
        moveDirection('up')

    def do_down(self, arg):
        """Go to the area downwards, if possible."""
        moveDirection('down')

    # Since the code is the exact same, we can just copy the
    # methods with shortened names:
    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_u = do_up
    do_d = do_down

    def do_exits(self, arg):
        """Toggle showing full exit descriptions or brief exit descriptions."""
        global showFullExits
        showFullExits = not showFullExits
        if showFullExits:
            print('Showing full exit descriptions.')
        else:
            print('Showing brief exit descriptions.')

    def do_inventory(self, arg):
        """Display a list of the items in your possession."""

        if len(inventory) == 0:
            print('Inventory:\n  (nothing)')
            return

        # first get a count of each distinct item in the inventory
        itemCount = {}
        for item in inventory:
            if item in itemCount.keys():
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        # get a list of inventory items with duplicates removed:
        print('Inventory:')
        for item in set(inventory):
            if itemCount[item] > 1:
                print('  %s (%s)' % (item, itemCount[item]))
            else:
                print('  ' + item)

    do_inv = do_inventory


    def do_take(self, arg):
        """"take <item> - Take an item on the ground."""

        # put this value in a more suitably named variable
        itemToTake = arg.lower()

        if itemToTake == '':
            print('Take what? Type "look" the items on the ground here.')
            return

        cantTake = False

        # get the item name that the player's command describes
        for item in getAllItemsMatchingDesc(itemToTake, state[location][GROUND]):
            if THINGS[item].get(TAKEABLE, True) == False:
                cantTake = True
                continue # there may be other items named this that you can take, so we continue checking
            print('You take %s.' % (THINGS[item][SHORTDESC]))
            state[location][GROUND].remove(item) # remove from the ground
            inventory.append(item) # add to inventory
            return

        if cantTake:
            print('You cannot take "%s".' % (itemToTake))
        else:
            print('That is not on the ground.')


    def do_drop(self, arg):
        """"drop <item> - Drop an item from your inventory onto the ground."""

        # put this value in a more suitably named variable
        itemToDrop = arg.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)

        # find out if the player doesn't have that item
        if itemToDrop not in invDescWords:
            print('You do not have "%s" in your inventory.' % (itemToDrop))
            return

        # get the item name that the player's command describes
        item = getFirstItemMatchingDesc(itemToDrop, inventory)
        if item != None:
            print('You drop %s.' % (THINGS[item][SHORTDESC]))
            inventory.remove(item) # remove from inventory
            state[location][GROUND].append(item) # add to the ground


    def complete_take(self, text, line, begidx, endidx):
        possibleItems = []
        text = text.lower()

        # if the user has only typed "take" but no item name:
        if not text:
            return getAllFirstDescWords(state[location][GROUND])

        # otherwise, get a list of all "description words" for ground items matching the command text so far:
        for item in list(set(state[location][GROUND])):
            for descWord in THINGS[item][DESCWORDS]:
                if descWord.startswith(text) and THINGS[item].get(TAKEABLE, True):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def complete_drop(self, text, line, begidx, endidx):
        possibleItems = []
        itemToDrop = text.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)

        for descWord in invDescWords:
            if line.startswith('drop %s' % (descWord)):
                return [] # command is complete

        # if the user has only typed "drop" but no item name:
        if itemToDrop == '':
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for inventory items matching the command text so far:
        for descWord in invDescWords:
            if descWord.startswith(text):
                possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def do_look(self, arg):
        """Look at an item, direction, or the area:
"look" - display the current area's description
"look <direction>" - display the description of the area in that direction
"look exits" - display the description of all adjacent areas
"look <item>" - display the description of an item on the ground or in your inventory"""

        lookingAt = arg.lower()
        if lookingAt == '':
            # "look" will re-print the area description
            displayLocation(location)
            return

        if lookingAt == 'exits':
            for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
                if direction in state[location]:
                    print('%s: %s' % (direction.title(), state[location][direction]))
            return

        if lookingAt in ('north', 'west', 'east', 'south', 'up', 'down', 'n', 'w', 'e', 's', 'u', 'd'):
            if lookingAt.startswith('n') and NORTH in state[location]:
                print(state[location][NORTH])
            elif lookingAt.startswith('w') and WEST in state[location]:
                print(state[location][WEST])
            elif lookingAt.startswith('e') and EAST in state[location]:
                print(state[location][EAST])
            elif lookingAt.startswith('s') and SOUTH in state[location]:
                print(state[location][SOUTH])
            elif lookingAt.startswith('u') and UP in state[location]:
                print(state[location][UP])
            elif lookingAt.startswith('d') and DOWN in state[location]:
                print(state[location][DOWN])
            else:
                print('There is nothing in that direction.')
            return

        # see if the item being looked at is on the ground at this location
        item = getFirstItemMatchingDesc(lookingAt, state[location][GROUND])
        if item != None:
            print('\n'.join(textwrap.wrap(THINGS[item][LONGDESC], SCREEN_WIDTH)))
            return

        # see if the item being looked at is in the inventory
        item = getFirstItemMatchingDesc(lookingAt, inventory)
        if item != None:
            print('\n'.join(textwrap.wrap(THINGS[item][LONGDESC], SCREEN_WIDTH)))
            return

        print('You do not see that nearby.')


    def complete_look(self, text, line, begidx, endidx):
        possibleItems = []
        lookingAt = text.lower()

        # get a list of all "description words" for each item in the inventory
        invDescWords = getAllDescWords(inventory)
        groundDescWords = getAllDescWords(state[location][GROUND])
        shopDescWords = getAllDescWords(state[location].get(SHOP, []))

        for descWord in invDescWords + groundDescWords + shopDescWords + [NORTH, SOUTH, EAST, WEST, UP, DOWN]:
            if line.startswith('look %s' % (descWord)):
                return [] # command is complete

        # if the user has only typed "look" but no item name, show all items on ground, shop and directions:
        if lookingAt == '':
            possibleItems.extend(getAllFirstDescWords(state[location][GROUND]))
            possibleItems.extend(getAllFirstDescWords(state[location].get(SHOP, [])))
            for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
                if direction in state[location]:
                    possibleItems.append(direction)
            return list(set(possibleItems)) # make list unique

        # otherwise, get a list of all "description words" for ground items matching the command text so far:
        for descWord in groundDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        # otherwise, get a list of all "description words" for items for sale at the shop (if this is one):
        for descWord in shopDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        # check for matching directions
        for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
            if direction.startswith(lookingAt):
                possibleItems.append(direction)

        # get a list of all "description words" for inventory items matching the command text so far:
        for descWord in invDescWords:
            if descWord.startswith(lookingAt):
                possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def do_list(self, arg):
        """List the items for sale at the current location's shop. "list full" will show details of the items."""
        if SHOP not in state[location]:
            print('This is not a shop.')
            return

        arg = arg.lower()

        print('For sale:')
        for item in state[location][SHOP]:
            print('  - %s' % (item))
            if arg == 'full':
                print('\n'.join(textwrap.wrap(THINGS[item][LONGDESC], SCREEN_WIDTH)))


    def do_buy(self, arg):
        """"buy <item>" - buy an item at the current location's shop."""
        if SHOP not in state[location]:
            print('This is not a shop.')
            return

        itemToBuy = arg.lower()

        if itemToBuy == '':
            print('Buy what? Type "list" or "list full" to see a list of items for sale.')
            return

        item = getFirstItemMatchingDesc(itemToBuy, state[location][SHOP])
        if item != None:
            # NOTE - If you wanted to implement money, here is where you would add
            # code that checks if the player has enough, then deducts the price
            # from their money.
            print('You have purchased %s' % (THINGS[item][SHORTDESC]))
            inventory.append(item)
            return

        print('"%s" is not sold here. Type "list" or "list full" to see a list of items for sale.' % (itemToBuy))


    def complete_buy(self, text, line, begidx, endidx):
        if SHOP not in state[location]:
            return []

        itemToBuy = text.lower()
        possibleItems = []

        # if the user has only typed "buy" but no item name:
        if not itemToBuy:
            return getAllFirstDescWords(state[location][SHOP])

        # otherwise, get a list of all "description words" for shop items matching the command text so far:
        for item in list(set(state[location][SHOP])):
            for descWord in THINGS[item][DESCWORDS]:
                if descWord.startswith(text):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def do_sell(self, arg):
        """"sell <item>" - sell an item at the current location's shop."""
        if SHOP not in state[location]:
            print('This is not a shop.')
            return

        itemToSell = arg.lower()

        if itemToSell == '':
            print('Sell what? Type "inventory" or "inv" to see your inventory.')
            return

        for item in inventory:
            if itemToSell in THINGS[item][DESCWORDS]:
                # NOTE - If you wanted to implement money, here is where you would add
                # code that gives the player money for selling the item.
                print('You have sold %s' % (THINGS[item][SHORTDESC]))
                inventory.remove(item)
                return

        print('You do not have "%s". Type "inventory" or "inv" to see your inventory.' % (itemToSell))


    def complete_sell(self, text, line, begidx, endidx):
        if SHOP not in state[location]:
            return []

        itemToSell = text.lower()
        possibleItems = []

        # if the user has only typed "sell" but no item name:
        if not itemToSell:
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for inventory items matching the command text so far:
        for item in list(set(inventory)):
            for descWord in THINGS[item][DESCWORDS]:
                if descWord.startswith(text):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


    def do_eat(self, arg):
        """"eat <item>" - eat an item in your inventory."""
        itemToEat = arg.lower()

        if itemToEat == '':
            print('Eat what? Type "inventory" or "inv" to see your inventory.')
            return

        cantEat = False

        for item in getAllItemsMatchingDesc(itemToEat, inventory):
            if THINGS[item].get(EDIBLE, False) == False:
                cantEat = True
                continue # there may be other items named this that you can eat, so we continue checking
            # NOTE - If you wanted to implement hunger levels, here is where
            # you would add code that changes the player's hunger level.
            print('You eat %s' % (THINGS[item][SHORTDESC]))
            inventory.remove(item)
            return

        if cantEat:
            print('You cannot eat that.')
        else:
            print('You do not have "%s". Type "inventory" or "inv" to see your inventory.' % (itemToEat))


    def complete_eat(self, text, line, begidx, endidx):
        itemToEat = text.lower()
        possibleItems = []

        # if the user has only typed "eat" but no item name:
        if itemToEat == '':
            return getAllFirstDescWords(inventory)

        # otherwise, get a list of all "description words" for edible inventory items matching the command text so far:
        for item in list(set(inventory)):
            for descWord in THINGS[item][DESCWORDS]:
                if descWord.startswith(text) and THINGS[item].get(EDIBLE, False):
                    possibleItems.append(descWord)

        return list(set(possibleItems)) # make list unique


if __name__ == '__main__':
    print('Escape from Goula!')
    print('==================')
    print()
    displayLocation(location)
    TextAdventureCmd().cmdloop()

