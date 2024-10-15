import time
import os
import random
import questionary
import pyfiglet
from rich.console import Console
from rich.text import Text

console = Console()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def animate_text(text, colors, delay=0.1):
    clear_screen()  # Clear the screen initially
    for i in range(len(text) + 1):
        figlet_text = pyfiglet.figlet_format(text[:i], font='short')
        colored_text = Text()
        for line in figlet_text.splitlines():
            # Choose a random color from the list for each line
            color = random.choice(colors)
            colored_text.append(line + "\n", style=color)
        console.print(colored_text)  # Print the current frame
        time.sleep(delay)  # Wait for the specified delay
        clear_screen()  # Clear the screen for the next frame

    # After the animation, print the final result without clearing
    final_figlet_text = pyfiglet.figlet_format(text, font='short')
    final_colored_text = Text()
    for line in final_figlet_text.splitlines():
        # Choose a random color for the final print
        color = random.choice(colors)
        final_colored_text.append(line + "\n", style=color)
    console.print(final_colored_text)  # Print the final ASCII art


def main():
    # Define the message and colors
    message = "Welcome to the habit tracker App!"
    color_list = ["red", "green", "yellow", "blue", "magenta", "cyan"]

    # Animate the text indefinitely with random colors
    animate_text(message, color_list)


if __name__ == "__main__":
    main()
