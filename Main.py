import sys
import API

#Francis Miadi 1210100
#Miar Taweel 1210447
#Leena Abuhammd 1210460

def log(string):
    sys.stderr.write("{}\n".format(string))
def dynamic_turns_with_reverse():
    position = [0, 0]  # Starting position (row, column)
    direction = 0  # 0 = Up, 1 = Right, 2 = Down, 3 = Left

    # Movement deltas for each direction
    moves = {
        0: (-1, 0),  # Up
        1: (0, 1),   # Right
        2: (1, 0),   # Down
        3: (0, -1)   # Left
    }

    def move_forward():
        """Move forward and update the position."""
        nonlocal position
        API.moveForward()
        dx, dy = moves[direction]
        position[0] += dx
        position[1] += dy
        log(f"Moved to position: {position}")
        if position in [[-7, 7], [-8, 7], [-8, 8],
                        [-7, 8]]:
        # Destination reached
            log(f"GOAL REACHED")
            sys.exit()


    def move_backward():
        """Move backward and update the position."""
        nonlocal position
        turn_right()  # Assuming `moveForward(-1)` moves backward
        turn_right()
        API.moveForward()
        turn_right()
        turn_right()
        dx, dy = moves[(direction + 2) % 4]  # Reverse the direction
        position[0] += dx
        position[1] += dy
        log(f"Reversed to position: {position}")

    def turn_left():
        """Turn the robot to the left."""
        nonlocal direction
        API.turnLeft()
        direction = (direction - 1) % 4
        log(f"Turned left. Now facing direction {direction}")

    def turn_right():
        """Turn the robot to the right."""
        nonlocal direction
        API.turnRight()
        direction = (direction + 1) % 4
        log(f"Turned right. Now facing direction {direction}")

    def should_turn_right():
        """Check if the robot should turn right based on the given conditions."""
        return (
            (direction in [0, 1,2,3]) and API.wallFront() and not API.wallRight()
        )

    def should_turn_left():
        """Check if the robot should turn left based on the given conditions."""
        return (
            (direction in [0,1,2, 3]) and API.wallFront() and not API.wallLeft()
        )

    def should_turn_l_back():
        """Check if the robot should turn right based on the given conditions."""
        return (
            (direction in [0, 1,2,3]) and  API.wallRight()
        )

    def should_turn_r_back():
        """Check if the robot should turn left based on the given conditions."""
        return (
            (direction in [0,1,2, 3]) and API.wallLeft()
        )

    def is_surrounded():
        """Check if the robot is surrounded by walls on three sides."""
        return API.wallFront() and API.wallLeft() and API.wallRight()

    def is_surrounded_back():
        """Check if the robot is surrounded by walls on two sides."""
        return  API.wallLeft() and API.wallRight()
    def move_until_wall():
        """Move forward until a wall is encountered, handling turns and reversals as specified."""
        flag=0
        flag1=0
        while True:
            if is_surrounded():
                flag=1
                flag1=1
                log("Surrounded by walls! Reversing...")
                move_backward()

            elif is_surrounded_back() and flag1==1:
                flag=1
                log("Surrounded by walls again! Reversing...")
                move_backward()

            elif  flag==1 :
                log(" leaving blocked place Reversing...")
                if should_turn_l_back():
                    log(" wall on right turn left ")
                    turn_left()

                elif should_turn_r_back():
                    log(" wall on left turn right ")
                    turn_right()
                flag = 0

            elif should_turn_right() and should_turn_left() and direction==2:
                turn_left()
                flag=0
                flag1 = 0
            elif should_turn_right():
                turn_right()
                flag = 0
                flag1=0
            elif should_turn_left():
                turn_left()
                flag = 0
                flag1 = 0
            elif not API.wallFront():
                move_forward()
                flag = 0
                flag1 = 0
            else:
                log("Hit a wall and cannot proceed forward.")
                break

    try:
        move_until_wall()
    except API.MouseCrashedError:
        log("The robot crashed!")
    except Exception as e:
        log(f"An unexpected error occurred: {e}")

# Run the dynamic turns with reverse algorithm
if __name__ == "__main__":
    dynamic_turns_with_reverse()