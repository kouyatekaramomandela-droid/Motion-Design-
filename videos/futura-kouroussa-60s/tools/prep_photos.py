"""Prepare the client photos for the 2.5D shots.

For each photo: remove company markings (inpainted, so no blur smudge remains), upscale x2 (Lanczos +
light unsharp), then split it into planes for parallax:
  <name>.jpg      cleaned full photo (upscaled)
  <name>-fg.png   nearest plane with soft alpha (GrabCut seeded by hand-drawn polygons: bridge,
                  machines, the well's basin, the two people at the meeting table)
  <name>-bg.jpg   clean plate: the subject region inpainted so the background can slide under it

Usage: python tools/prep_photos.py   (from the project root; needs opencv-python-headless, numpy)
"""
import os
import cv2
import numpy as np

SRC, OUT, WORK = "assets/photos/src", "assets/photos", "assets/photos/work"
SCALE = 2

# Company markings to erase, in source pixels: (x0, y0, x1, y1, mode)
#   "dark" inpaints only the dark lettering inside the box, "all" inpaints the whole box.
MARKINGS = {
    "R-reunion": [(818, 362, 906, 390, "dark"),   # lettering on the hi-vis vest
                  (92, 248, 160, 298, "all")],    # badge on the white cap
    "C-mine": [(486, 248, 538, 272, "dark"),      # brand on the excavator boom
               (566, 272, 606, 300, "dark"),      # lettering on the arm
               (668, 338, 700, 362, "dark")],     # plate on the counterweight
}

# Nearest-plane seeds (source pixels) for GrabCut: one or more polygons per photo.
POLYS = {
    "A-pont-niger": [[(180, 1366), (300, 1080), (470, 820), (640, 560), (735, 400), (790, 265),
                     (905, 20), (1000, 0), (975, 60), (880, 330), (835, 470), (780, 640),
                     (700, 900), (600, 1130), (520, 1366)]],
    "C-mine": [[(352, 238), (412, 222), (470, 214), (500, 224), (612, 290), (700, 296), (726, 350),
               (712, 392), (660, 420), (548, 372), (482, 358), (446, 366), (366, 334), (350, 290)]],
    # basin, pump and water cans in front of the villagers (the villagers stay in the back plane)
    "D-forage": [[(0, 665), (0, 505), (40, 500), (85, 462), (180, 436), (276, 444), (284, 418),
                 (330, 402), (346, 378), (452, 378), (640, 382), (646, 232), (722, 232), (726, 384),
                 (868, 392), (1100, 586), (1100, 665)]],
    # the two people at the table edge (the segmentation model loses their patterned clothes);
    # the colleague in the hi-vis vest stays in the back plane
    "R-reunion": [[(0, 768), (0, 330), (20, 272), (80, 248), (130, 250), (210, 292), (212, 305),
                   (188, 322), (186, 350), (190, 385), (178, 410), (170, 440), (150, 470), (260, 478),
                   (300, 462), (378, 470), (380, 500), (300, 512), (380, 600), (440, 700), (462, 768)],
                  [(555, 768), (560, 690), (600, 640), (660, 610), (700, 600), (745, 575), (775, 560),
                   (770, 520), (762, 470), (775, 410), (810, 385), (860, 378), (910, 390), (945, 430),
                   (950, 480), (940, 530), (915, 565), (905, 580), (960, 600), (1010, 635), (1020, 660),
                   (1020, 768)]],
}


def erase_markings(img, boxes):
    mask = np.zeros(img.shape[:2], np.uint8)
    for x0, y0, x1, y1, mode in boxes:
        if mode == "all":
            cv2.ellipse(mask, ((x0 + x1) // 2, (y0 + y1) // 2), ((x1 - x0) // 2, (y1 - y0) // 2), 0, 0, 360, 255, -1)
        else:
            roi = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
            dark = (roi < np.percentile(roi, 60) - 18).astype(np.uint8) * 255
            mask[y0:y1, x0:x1] = cv2.dilate(dark, np.ones((3, 3), np.uint8), iterations=2)
    out = cv2.inpaint(img, mask, 6, cv2.INPAINT_TELEA)
    # soften the repaired patches so the fill grain matches its surroundings
    soft = cv2.GaussianBlur(out, (0, 0), 1.6)
    m = cv2.GaussianBlur(cv2.dilate(mask, np.ones((5, 5), np.uint8)), (0, 0), 3)[..., None] / 255.0
    return (out * (1 - m) + soft * m).astype(np.uint8)


def upscale(img, interp=cv2.INTER_LANCZOS4):
    big = cv2.resize(img, None, fx=SCALE, fy=SCALE, interpolation=interp)
    if big.ndim == 3 and big.shape[2] == 3:
        blur = cv2.GaussianBlur(big, (0, 0), 1.4)
        big = cv2.addWeighted(big, 1.25, blur, -0.25, 0)
    return big


def grabcut_alpha(img, polys):
    h, w = img.shape[:2]
    seed = np.zeros((h, w), np.uint8)
    cv2.fillPoly(seed, [np.array(p, np.int32) for p in polys], 255)
    mask = np.full((h, w), cv2.GC_BGD, np.uint8)
    mask[cv2.dilate(seed, np.ones((25, 25), np.uint8)) > 0] = cv2.GC_PR_BGD
    mask[seed > 0] = cv2.GC_PR_FGD
    mask[cv2.erode(seed, np.ones((15, 15), np.uint8)) > 0] = cv2.GC_FGD
    bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(img, mask, None, bgd, fgd, 6, cv2.GC_INIT_WITH_MASK)
    a = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    a = cv2.morphologyEx(a, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    return cv2.GaussianBlur(a, (0, 0), 1.2)


def fill_holes(alpha):
    # close pattern holes (printed fabrics); subjects cut by the frame bottom stay closed there
    b = (alpha > 127).astype(np.uint8) * 255
    h, w = b.shape
    pad = np.zeros((h + 3, w + 2), np.uint8)
    pad[1:h + 1, 1:w + 1] = b
    pad[h + 1, 1:w + 1] = cv2.dilate(b[-1:], np.ones((1, 9), np.uint8))[0]
    flood = pad.copy()
    cv2.floodFill(flood, np.zeros((h + 5, w + 4), np.uint8), (0, 0), 255)
    holes = (flood[1:h + 1, 1:w + 1] == 0)
    out = alpha.copy()
    out[holes] = 255
    return out


def clean_plate(img, alpha):
    # inpaint at half resolution (large holes), then paste the fill back under the hole only
    hole = cv2.dilate((alpha > 20).astype(np.uint8) * 255, np.ones((31, 31), np.uint8))
    small = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    hs = cv2.resize(hole, (small.shape[1], small.shape[0]), interpolation=cv2.INTER_NEAREST)
    fill = cv2.inpaint(small, hs, 9, cv2.INPAINT_TELEA)
    fill = cv2.GaussianBlur(cv2.resize(fill, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC), (0, 0), 3)
    m = cv2.GaussianBlur(hole, (0, 0), 6)[..., None] / 255.0
    return (img * (1 - m) + fill * m).astype(np.uint8)


def main():
    os.makedirs(WORK, exist_ok=True)
    for name in ["A-pont-niger", "C-mine", "D-forage", "R-reunion"]:
        img = cv2.imread(f"{SRC}/{name}.jpg")
        if name in MARKINGS:
            img = erase_markings(img, MARKINGS[name])
        cv2.imwrite(f"{WORK}/{name}-clean.png", img)
        alpha = grabcut_alpha(img, POLYS[name])
        alpha = fill_holes(alpha)
        cv2.imwrite(f"{WORK}/{name}-alpha.png", alpha)
        big = upscale(img)
        a_big = cv2.resize(alpha, (big.shape[1], big.shape[0]), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(f"{OUT}/{name}.jpg", big, [cv2.IMWRITE_JPEG_QUALITY, 92])
        fg = big.copy()
        fg[a_big < 2] = 0  # empty pixels compress to nothing
        cv2.imwrite(f"{OUT}/{name}-fg.png", np.dstack([fg, a_big]), [cv2.IMWRITE_PNG_COMPRESSION, 9])
        cv2.imwrite(f"{OUT}/{name}-bg.jpg", clean_plate(big, a_big), [cv2.IMWRITE_JPEG_QUALITY, 90])
        print(name, big.shape[1], "x", big.shape[0], "subject", round(float((alpha > 128).mean()) * 100, 1), "%")


main()
