from PIL import Image
import random
import numpy as np

blank = Image.open("./img_files2/blank.png")


def get_previous_adjacency(i, j, step):
    if (
        (j != 0 and full_map[i][j - 1] == step)
        or (i < heigth - 1 and full_map[i + 1][j] == step)
        or (i != 0 and full_map[i - 1][j] == step)
        or (j < width - 1 and full_map[i][j + 1] == step)
    ):
        return True
    else:
        return False


# merge each tile image in a line
def get_concat_h(im1, im2):
    dst = Image.new("RGB", (im1.width + im2.width, max(im1.height, im2.height)))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


# merge eache line of tiles vertically
def get_concat_v(im1, im2):
    dst = Image.new("RGB", (max(im1.width, im2.width), im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def get_path_by_tile_adjacency(i, j):
    path = ""
    if (
        i != 0
        and full_map[i - 1][j] != 0
        and (
            full_map[i - 1][j] - 1 == full_map[i][j]
            or full_map[i - 1][j] + 1 == full_map[i][j]
        )
    ):
        path += "w"
    if (
        j < (width - 1)
        and full_map[i][j + 1] != 0
        and (
            full_map[i][j + 1] - 1 == full_map[i][j]
            or full_map[i][j + 1] + 1 == full_map[i][j]
        )
    ):
        path += "d"
    if (
        i < (heigth - 1)
        and full_map[i + 1][j] != 0
        and (
            full_map[i + 1][j] - 1 == full_map[i][j]
            or full_map[i + 1][j] + 1 == full_map[i][j]
        )
    ):
        path += "s"
    if (
        j != 0
        and full_map[i][j - 1] != 0
        and (
            full_map[i][j - 1] - 1 == full_map[i][j]
            or full_map[i][j - 1] + 1 == full_map[i][j]
        )
    ):
        path += "a"
    if not path:
        path = "none"
    return path


size = int(input("Iterations: "))
width = size * 2
heigth = size * 2

full_map = [[0 for _ in range(width)] for _ in range(heigth)]

# fill matrix with iteration step value
step = 0
while step < size:
    created = False
    print(step)
    if step != 0:
        for i in range(len(full_map)):
            for j in range(len(full_map[i])):
                if full_map[i][j] == 0 and get_previous_adjacency(i, j, step):
                    if random.randint(0, 1):
                        full_map[i][j] = step + 1
                        print("criou")
                        created = True
                    else:
                        full_map[i][j] = 0
    else:
        full_map[width // 2][heigth // 2] = 1
        created = True
    if created:
        print(created)
        step += 1

for line in full_map:
    print(*line)
print("==========")

sum_columns = np.sum(full_map, axis=0)
sum_rows = np.sum(full_map, axis=1)

zero_row = []
zero_column = []

for i in range(size * 2):
    if sum_columns[i] == 0:
        zero_column.append(i)
    if sum_rows[i] == 0:
        zero_row.append(i)

zero_row = np.flip(zero_row)
zero_column = np.flip(zero_column)

print(zero_row)
print(zero_column)
print("==========")

for i in zero_row:
    full_map = np.delete(full_map, i, 0)
for i in zero_column:
    full_map = np.delete(full_map, i, 1)

for line in full_map:
    print(*line)
print("==========")

heigth = len(full_map)
width = len(full_map[0])

full_map_img = Image.new("RGB", (0, 0))


## TODO: melhorar/criar forma para adcionar sprites de entrada, saidas e pontos de interesse
for i in range(len(full_map)):
    line = Image.new("RGB", (0, 0))
    for j in range(len(full_map[i])):
        if full_map[i][j] == 0:
            line = get_concat_h(line, blank)
        else:
            path = get_path_by_tile_adjacency(i, j)
            if full_map[i][j] != 1:
                tile = Image.open(f"./img_files2/{path}.png")
            else:
                tile = Image.open(f"./img_files2/start/{path}.png")
            line = get_concat_h(line, tile)

    full_map_img = get_concat_v(full_map_img, line)

full_map_img.resize((width * 100, heigth * 100), Image.Resampling.NEAREST).show()

