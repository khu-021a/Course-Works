import os.path as p
import glob
import cv2


def clip2patches(in_file, out_dir, base_name, patch_size, overlap_size):
    in_img = cv2.imread(in_file)
    img_row = in_img.shape[0]
    img_col = in_img.shape[1]
    patch_row = patch_size[0]
    patch_col = patch_size[1]
    n_patch_row = (img_row + overlap_size[0]) / patch_row
    n_patch_col = (img_col + overlap_size[1]) / patch_col
    r_pad = (img_row + overlap_size[0]) % patch_row / 2
    c_pad = (img_col + overlap_size[1]) % patch_col / 2
    for x in range(n_patch_row):
        for y in range(n_patch_col):
            out_name = base_name + '_' + str(x) + '_' + str(y) + '.png'
            if x == 0:
                xs = r_pad + x * patch_row
            else:
                xs = r_pad + x * patch_row - overlap_size[0]

            if y == 0:
                ys = c_pad + y * patch_col
            else:
                ys = c_pad + y * patch_col - overlap_size[1]
            xe = xs + patch_row
            ye = ys + patch_col
            patch = in_img[xs:xe, ys:ye]
            cv2.imwrite(out_dir + out_name, patch)

source_dir = 'inputs/'
target_dir = 'targets/'
images = glob.glob(source_dir + '*.png')
for img in images:
    clip2patches(img, target_dir, p.splitext(p.basename(img))[0], (33, 33), (12, 12))

