import turtle as trtl
import math
import random as rand
#define the
wn = trtl.Screen()
#initialize the player's turtle
player1 = trtl.Turtle()
player2 = trtl.Turtle()
writer = trtl.Turtle()
writer.hideturtle()

list_of_lines = []

list_of_turtles = []

collisions_detected = 0

end_game = False

colors = ["DarkRed", "LightSalmon", "DeepPink", "Indigo", "DarkSlateBlue", "DarkKhaki", "Lime", "SeaGreen", "DarkGreen", "Olive", "Teal", "Navy", "DodgerBlue"]

def shoot (s_turtle):
    # Create and shoot the projectile
    global list_of_lines
    global list_of_turtles
    global end_game
    print(not(end_game))
    if not(end_game):
        #initialize a new turtle to make a line
        line = trtl.Turtle()
        #line.size(0.5)
        line.speed(30000)
        #have the new line writer goto the turtle that called the shoot command
        line.penup()
        line.setheading(s_turtle.heading())
        line.goto(s_turtle.xcor(), s_turtle.ycor())
        #make sure that the line is created 40 pixels ahead of the turtle
        line.penup()
        line.forward(40) 
        line.pendown()
        # a list to hold the start and end of the line created
        line_sne = []
        line_sne.append(round(line.xcor()))
        line_sne.append(round(line.ycor()))
        #if there are more than thirty lines, remove the first one created
        if len(list_of_turtles) > 30:
            eliminated = list_of_turtles.pop(0)
            list_of_lines.pop(0)
            eliminated.clear()
            
        #create a line all the way into the border of the game
        while (abs(line.xcor()) < 400) and (abs(line.ycor()) < 400):
                line.forward(100)
        #hide the turtle that made the line and save the endpoint of the line
        line.hideturtle()
        #save the turtle object for removal later
        list_of_turtles.append(line)
        line_sne.append(round(line.xcor()))
        line_sne.append(round(line.ycor()))
        list_of_lines.append(line_sne)
        print(list_of_lines)



def collision_detection (LOL, player):
    global collisions_detected
    for line in LOL:
        slope = ((line[1] - line[3]) / (line[0] - line[2]))
        b = line[1] - (slope * line[0])
        y = round(player.ycor())
        x = round(player.xcor())
        if abs(y - round((slope*x) + b )) <5 :
            if ((x >= line[0]) and  (x <= line[2])) or ((x <= line[0]) and  (x >= line[2])):
                if ((y >= line[1]) and  (y <= line[3])) or ((y <= line[1]) and  (y >= line[3])):
                    print("The game’s up, chump!")
                    print(collisions_detected)
                    collisions_detected +=1
                    end_the_game()

            #or (abs(player.xcor()) > 400) or (abs(player.ycor()) > 400))
            #((((x >= line[0]) and  (x <= line[2])) or ((x <= line[0]) and  x >= line[2]) ) and ((y >= line[1] and  y <= line[3]) or ((y <= line[1]) and  y >= line[3]) ) )):
            # Call an endgame function
        elif (abs(player.xcor()) > 400) or (abs(player.ycor()) > 400):
            print("The game’s up, chump!")
            print(collisions_detected)
            collisions_detected +=1
            end_the_game()

def bot_move (bot, index):
    global end_game
    bot.forward(5)
    old_ang = shoot_angle(player1, player2)
    bot.right(old_ang)
    new_angle = shoot_angle(player1, player2)
    if (new_angle >old_ang) and (abs(new_angle) > 10):
        bot.left(2*old_ang)
    if index%5 == 0:
        bot.setheading(bot.heading() - rand.randint(-50,50))
        if not(end_game):
            shoot(bot)



def shoot_angle(target, shooter):
    #calculate the angle difference between the line between both turtles and the line extending in front of the shooter
    line_calc = []
    changeInX = target.xcor() - shooter.xcor()
    changeInY = target.ycor() - shooter.ycor()
    #find the slope of the line between both turtles
    slope2 = changeInY / changeInX
    #find the slope of the line extending from the turtle's current heading
    line_calc.append(shooter.xcor())
    line_calc.append(shooter.ycor())
    shooter.forward(1)
    line_calc.append(shooter.xcor())
    line_calc.append(shooter.ycor())
    shooter.forward(-1)
    slope = ((line_calc[1] - line_calc[3]) / (line_calc[0] - line_calc[2]))
    #calculate the angle using fancy math
    if ((1+(slope *slope2)) == 0 ) or ((slope - slope2) == 0):
        return 0 
    else:
        return math.degrees(math.atan(abs((slope - slope2) / (1+(slope *slope2)))))
    
    
    



def start_game ():
    global list_of_lines
    global end_game
    player1.speed(100)
    player2.speed(100)
    #create the borders of the game
    player1.penup()
    player1.goto(400,400)
    player1.pendown()
    for i in range(4):
        player1.right(90)
        player1.forward(800)
    player1.penup()
    player1.goto(300,-300)
    player2.penup()
    player2.goto(-300,300)
    #define movement functions
    def turn_left ():
        player1.left(20)
    
    def turn_right():
        player1.right(20)
    
    def call_shoot():
        shoot(player1)
    
    #define responses to keypress events
    wn.onkeypress(turn_left, "Left")
    wn.onkeypress(turn_right, "Right")
    wn.onkeypress(call_shoot, "0")
    wn.listen()
    #begin the mainloop, in which the game is played
    index = 0
    while True:
        index += 1
        player1.forward(5)
        collision_detection(list_of_lines, player1)
        bot_move(player2, index)
        collision_detection(list_of_lines, player2)
        if end_game:
            break
    print("out of loop")

def end_the_game ():
    global end_game
    player1.hideturtle()
    player2.hideturtle()
    end_game = True
    writer.penup()
    writer.goto(-400, 400)
    writer.pendown()
    writer.write('Games Up Chump!', font = ("Arial", 100))
    index = 0
    for line in list_of_lines:

start_game()

wn.mainloop()
