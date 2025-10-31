from PIL import Image, ImageStat
from pathlib import Path


TILE_SIZE = (10, 10)
oldim = ('Исходник.jpg')
oldim = Image.open(oldim).convert('RGB')
WIDTH, LENGTH = oldim.size
WIDTH = (WIDTH // TILE_SIZE[0]) * TILE_SIZE[0] * 10
LENGTH = (LENGTH // TILE_SIZE[1]) * TILE_SIZE[1] * 10
oldim = oldim.resize((WIDTH, LENGTH))


folder = Path('Изображения')
imags = []
for img in folder.glob('*.jpg'):
    img = Image.open(img).convert('RGB').resize(TILE_SIZE)
    avg_colors = tuple(map(int, ImageStat.Stat(img).mean))
    imags.append((img.copy(), avg_colors))


def best_tile(target_color, images):
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
        mosaic.paste(besti_tile, box)
mosaic.save('Результат.jpg')
mosaic.show()
