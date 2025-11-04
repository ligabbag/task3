from os.path import exists

from PIL import Image, ImageStat
from pathlib import Path


TILE_SIZE = (10, 10)

while True:
    oldim = input('Введите путь к изображению: \n')
    path = Path(oldim)
    if path.exists() and path.is_file():
        break
    else:
        print('Файл не найден, Попробуйте еще раз')

oldim = Image.open(oldim).convert('RGB')
WIDTH, LENGTH = oldim.size
WIDTH = WIDTH * TILE_SIZE[0]
LENGTH = LENGTH  * TILE_SIZE[1]
oldim = oldim.resize((WIDTH, LENGTH))


while True:
    folder = Path(input('Введите расположение папки с изображениями: \n'))
    if folder.exists() and folder.is_dir():
        break
    else:
        print('Такой папки не существует, Попробуйте еще раз')

imags = []
for suf in ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.webp'):
    for img in folder.glob(suf):
        img = Image.open(img).convert('RGB').resize(TILE_SIZE)
        avg_colors = tuple(map(int, ImageStat.Stat(img).mean))
        imags.append((img, avg_colors))


def best_tile(target_color, images):
    if not images:
        return None
    best_tile = None
    min_distance = float('inf')
    for img, avg_colors in images:
        dist = ((target_color[0] - avg_colors[0]) ** 2 +
                   (target_color[1] - avg_colors[1]) ** 2 +
                   (target_color[2] - avg_colors[2]) ** 2)**0.5
        if dist < min_distance:
            min_distance = dist
            best_tile = img
    return best_tile


mosaic = Image.new('RGB',(WIDTH, LENGTH))
for x in range(0, WIDTH, TILE_SIZE[0]):
    for y in range(0, LENGTH, TILE_SIZE[1]):
        box = (x, y, x + TILE_SIZE[0], y + TILE_SIZE[1])
        pix = oldim.crop(box)
        tg_color = tuple(map(int, ImageStat.Stat(pix).mean))
        besti_tile = best_tile(tg_color, imags)
        if besti_tile is not None:
            mosaic.paste(besti_tile, box)
        else:
            print('Ошибка с папкой Изображений')
mosaic.save('Результат.jpg')
mosaic.show()
