##Developed by Tales Carlos de Pádua

###This game was based on PyGame tutorial from YouTube channel thenewboston. 
###Check it out on https://www.youtube.com/watch?v=K5F-aGDIYaM and subscribe this awesome channel

Developed in Python 2.7 with PyGame.

I developed this game for use in OOP workshop in Centro Universitário Senac SP to Computer Science students.
I made some changes in the tutorial code. 
Major changes are:
- I have created a Snake, Fruit, and Game classes in separate files and folders, in order to teach basics of python 
packages, classes and objects. The game is called in the main script "pysnake.py"
- The way snake body works. In this game snake body is a list of SnakeSegment objects. These objects have pos_x and 
pos_y values. Each time the snake eats a fruit, a segment is added at the end of the list, in the same position as the 
last segment.
- The way the snake moves. The snake in this game moves by popping the last element in the list and adding it to the 
front of the list, in the position of the next movement. This means that the head of the snake is the first element of
the list, and not the last one like in the thenewboston tutorial. I don't know if this approach is more efficient or not,
so if you know it, let me know
- Added a bunch of comments to the code. Although the video tutorials are very well done, the code itself is not commented,
so I put a lot of comments in the code to make it very understandable
- Collision is simple, as this game is not intended to be played with snake and fruit with different sizes, although the
code allows simple changes to make screen sizes and snake/fruit sizes different. Just be careful and use values that 
are multiples of screen width and height sizes.
"# smartsnake" 
