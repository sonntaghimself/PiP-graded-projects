# a function that calculates x and y coordinates for a snake-type stimulus using
# the tex_size and the number of tiles


def coord(tex_size, n_tiles, size_box, x, y):
    points_x = ((tex_size / 2) * -1) + (size_box[0] / 2) + (size_box[0] * x)
    points_y = ((tex_size / 2) * -1) + (size_box[0] / 2) + (size_box[0] * y)
    return points_x, points_y
