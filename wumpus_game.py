#A game inspired by the classic text game Hunt the Wumpus, by Gregory Yob.
#There is a series of rooms that the player can travel between. In one 
#of these rooms is the Wumpus. If the player wanders into the Wumpus'
#room, then they die and the game is over. The player can also shoot 
#from their room into an adjacent room. If the Wumpus is in the room they 
#shoot into, the player wins and the game is over. When the player enters
#a room that is next to the room the Wumpus is in, a message is displayed
#saying that they can smell the Wumpus.

from wumpus import *

#Set up the maze...
#Reminder: The Maze constructor takes a list of Rooms.
#Reminder: The Room constructor takes 3 arguments: the room number,
#    the description of the room, and a list of the room numbers that this
#    Room connects to.
eight_room_maze = Maze( [ \
    Room(0, "This is the docking bay.", [1,2,3,4]), \
    Room(1, "This is the spaceship hangar.", [0,2,4,5]), \
    Room(2, "These are the crew's sleeping quarters.", [0,1,3,5]), \
    Room(3, "This is the galley.", [0,2,4,5]), \
    Room(4, "This is a storage closet.", [0,1,3,5]), \
    Room(5, "This is control room.", [1,2,3,4]) ] )

#Creating the Wumpus...
#Reminder: The Monster constructor takes 1 or 2 arguments. The first 
#    argument is the Monster's name, and the second is the starting room 
#    number. If the room number is missing, then the Monster is 
#    automatically placed in room 0.
wumpus = Monster("the Wumpus")
#So the Wumpus is now in room 0. We'll move him to a random location
#    later.

#Creating the Player...
#Reminder: The Player constructor takes 2 optional arguments: the number
#     of darts and the starting room number. If the number of darts is left
#    out, it defaults to only 1 dart. If the room number is left out, then 
#    the Player is automatically placed in room 0.
player1 = Player(2)
#So the player is now in room 0 and has 2 darts. We'll move him to a 
#    random location later.

#Moving the Wumpus and the Player to random Rooms...
#Reminder: Any Movable object has the .randomly_place() method, which takes
#    a Maze and an optional list of off-limits room numbers, and moves
#     the Movable to a random Room in the given Maze, but not one of the 
#    Rooms listed in the optional list.
#Reminder: Both Monsters and Players are Movable.

wumpus.randomly_place(eight_room_maze)
#This command places the Wumpus in a randomly selected Room in the 8-Room
#    Maze.

#Reminder: Any Movable object has the .location attribute, which stores
#    the room number that the object is in.
player1.randomly_place(eight_room_maze, [wumpus.location])
#Now the player is in a randomly selected room from the 8-Room Maze, but
#     not in the same room as the Wumpus.

#Display the intro message:
print("""Welcome to Wumpus Capture!

A wild Wumpus is loose in the area, and it's your job to capture it without
getting eaten. Travel around the map, and when you have figured out which
room the Wumpus is in, go to an adjacent room and shoot a tranquilizer 
dart into that room. If you hit the Wumpus, you win! But be careful; you
only have two darts!
""")

print("You begin the game in room " + str(player1.location))

#The main game loop:
while(True):
    #Display the room description for the room that player1 is currently in.
    #Reminder: the .describe_room() method returns a string containing the
    #    description of the room with the given number and a nicely printed
    #    list of adjacent rooms.
    print(eight_room_maze.describe_room(player1.location))

    if player1.location == wumpus.location:
        #If the player and the Wumpus are in the same room:
        print("The wumpus is here! It eats you!")
        #Game Over:
        break
    
    #Reminder: All Movables have an .is_near() method that takes another
    #    Movable and a Maze, and returns True if the second Movable is
    #    in a room that is adjacent to the first Movable (in the given Maze).
    if player1.is_near(wumpus, eight_room_maze):
        #If the Wumpus is in a room adjacent to where the Player is...
        print("The smell of wumpus fills the room. It must be nearby.")
    
    print("You have " + str(player1.num_darts) + " darts left.")
    
    #Get a command from the player, using the Player method .get_command(),
    #    which takes a Maze (so that it can figure out which rooms are
    #    adjacent to the player's room. This method will keep asking the
    #    user to input a command until they input a valid command.
    #    Valid commands are of the form "go to NUM" or "shoot into NUM",
    #    where NUM is one of the adjacent room numbers. If the user's
    #    command doesn't start with "go to" or "shoot into", then the
    #    command is rejected and the method asks again. If NUM isn't a 
    #    valid number representing an adjacent room, then the command is
    #    rejected, and the method asks again. .get_command() returns an 
    #    object of type Command.
    cmd = player1.get_command(eight_room_maze)
    
    #Reminder: The Command attribute .command_type is either "move"
    #    or "shoot", depending on the type of the Command.
    #Reminder: The Command attribute .target is the room number that
    #    the Command is targetting.
    if cmd.command_type == "move":
        #Reminder: The Movable method .move_to() moves the movable object
        #    to the given room number. It doesn't check to see if that
        #    room is adjacent or not.
        player1.move_to(cmd.target)
        print("Moving to room " + str(cmd.target))
    elif cmd.command_type == "shoot":
        #Reminder: The Player method .shoot() takes no arguments. If 
        #    the player has no darts left, it returns False. Otherwise, the 
        #    method reduces the player's darts by 1 and returns True.
        if player1.shoot():
            #If the player's gun shoots successfully...
            print("The gun goes *BANG*, and a dart flies into room " \
                    + str(cmd.target) + "...")
            if cmd.target == wumpus.location:
                #If the dart hits the wumpus...
                print("You hear a roar from the wumpus and a thump as it falls asleep.")
                print("Congratulations! You have captured the wumpus!")
                #Game Over:
                break
            else:
                #If the wumpus was in a different room...
                print("But it doesn't sound like you hit anything.")
