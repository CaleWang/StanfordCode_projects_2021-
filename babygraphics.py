"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """

    x_coordinate = GRAPH_MARGIN_SIZE + (width - GRAPH_MARGIN_SIZE * 2) // len(YEARS) * year_index
    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')  # delete all existing lines from the canvas

    # Write your code below this line
    #################################
    # upper line
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, )
    # bottom line
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE,
                       CANVAS_HEIGHT - GRAPH_MARGIN_SIZE)
    # left line
    canvas.create_line(GRAPH_MARGIN_SIZE, 0, GRAPH_MARGIN_SIZE, CANVAS_HEIGHT)

    # coordinate of years(vertical lines)
    for i in range(len(YEARS)):
        canvas.create_line(get_x_coordinate(CANVAS_WIDTH, i), 0, get_x_coordinate(CANVAS_WIDTH, i), CANVAS_HEIGHT)
    # label of years
    for i in range(len(YEARS)):
        canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i) + 3, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE + 3, text=YEARS[i],
                           anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)  # draw the fixed background grid

    # Write your code below this line
    #################################
    for i in range(len(lookup_names)):
        line_coordinates = []
        # store the coordinate(x, y) of each data
        for j in range(len(YEARS)):
            x = get_x_coordinate(CANVAS_WIDTH, j)
            # the coordinates of the data in the x direction
            y = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
            # the coordinates of the data in the y direction when rank > 1000
            name_rank_beyond = f'{lookup_names[i]} *'
            # the text of name and rank when rank > 1000

            # repeat the color cycles (len(COLORS)==4)
            if i <= 3:
                color = COLORS[i]
            else:
                color = COLORS[i - len(COLORS)*(i//len(COLORS))]

            if name_data[lookup_names[i]].__contains__(f'{YEARS[j]}'):
                # check key(year) whether in the dictionary of name_data[name]
                rank = name_data[lookup_names[i]][f'{YEARS[j]}']
                # rank = name_data['name']['year']
                name_rank = f'{lookup_names[i]} {rank}'
                # the text of name and rank

                # plot all the label(year:rank) on canvas
                if int(rank) <= 1000:
                    y = GRAPH_MARGIN_SIZE + int(rank) * 0.56
                    # int(rank)*0.56 to fit the actual spacing on canvas (Vertical spacing==560)
                    canvas.create_text(x + TEXT_DX, y, text=name_rank, anchor=tkinter.NW, fill=color)
                    line_coordinates.append((x, y))
                else:
                    canvas.create_text(x + TEXT_DX, y, text=name_rank_beyond, anchor=tkinter.SW, fill=color)
                    line_coordinates.append((x, y))
            else:
                canvas.create_text(x + TEXT_DX, y, text=name_rank_beyond, anchor=tkinter.SW, fill=color)
                line_coordinates.append((x, y))

            # draw connection lines
            r = 2
            # the radius of the circle
            x1 = line_coordinates[j-1][0]
            y1 = line_coordinates[j-1][1]
            canvas.create_oval(x1-r, y1-r, x1+r, y1+r, fill=color)
            x2 = line_coordinates[j][0]
            y2 = line_coordinates[j][1]
            canvas.create_oval(x2-r, y2-r, x2+r, y2+r, fill=color)
            canvas.create_line(x1, y1, x2, y2, fill=color, width=LINE_WIDTH)


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
