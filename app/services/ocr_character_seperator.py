from sqlalchemy.orm import Session
import imageio
import matplotlib.pyplot as plt
import numpy as np
from skimage import exposure
from skimage import filters
from skimage import io
from skimage.color import rgb2gray
from skimage.draw import line
from skimage.draw import rectangle
from skimage.filters.rank import mean
from skimage.filters.rank import median
from skimage.measure import label, regionprops
from skimage.morphology import closing, square, opening, dilation
from skimage.morphology import disk
from skimage.morphology import skeletonize
from skimage.transform import resize
from skimage.util import invert


class OcrCharacterSeperator:

    def __init__(self, db: Session):
        self.db = db


    def line_counter(self, inp_img):
        line_count = 1
        for i in range(len(lines) - 1):
            new_img = inp_img[lines[i]:lines[i + 1] - 1, 0:column]
            if int(new_img.shape[0]) < 30:
                continue
            new_img = resize(new_img, (90, int(new_img.shape[1] * (90 / float(new_img.shape[0])))))
            new_img = self.pre_image_processing(new_img)
            skeleton = skeletonize(new_img) * 255
            imgs.append(skeleton)
            line_count += 1
        return line_count


    @staticmethod
    def pre_image_processing(resized_image):

        equal_adapt_hist_image = exposure.equalize_adapthist(resized_image)
        rescale_intensity_image = exposure.rescale_intensity(equal_adapt_hist_image)
        adjust_sigmoid_image = exposure.adjust_sigmoid(rescale_intensity_image)
        gray_scale_image = rgb2gray(adjust_sigmoid_image)
        mean_image = mean(gray_scale_image, disk(1))
        mean_image = mean(mean_image, disk(1))
        mean_image = mean(mean_image, disk(1))

        median_image = dilation(median(mean_image, disk(1)), square(2))
        otsu_image = filters.threshold_otsu(median_image)
        closing_image = closing(median_image > otsu_image, square(1))
        #    opening_image = opening(closing_image, square(2))
        opening_image = invert(closing_image)
        return opening_image


    @staticmethod
    def line_separation(image):
        hor_lines = []
        hor_lines.append(0)
        row, column = image.shape
        black_pixel_sum = []

        for i in range(0, row):
            pixel_count = 0
            for j in range(0, column):
                pixel_value = image[i][j]
                if pixel_value == 0:
                    pixel_count += 1
            black_pixel_sum.append(pixel_count)

        i = 0
        while i < len(black_pixel_sum):
            if black_pixel_sum[i] == 0:
                white_row_count = 0
                for j in range(i, len(black_pixel_sum)):
                    if black_pixel_sum[j] == 0:
                        white_row_count += 1
                    else:
                        break
                if white_row_count > 15:
                    row_partition = white_row_count // 2
                    final_line_row = i + row_partition
                    hor_lines.append(final_line_row)
                i += (white_row_count)

            else:
                i += 1

        hor_lines.append(row)
        return hor_lines


    @staticmethod
    def line_and_base_seperation(closing_image2, image_count):
        histogram = closing_image2.sum(axis=1).reshape(1, -1)
        maximum_histogram_index = np.argmax(histogram)
        closing_img = closing_image2

        for i in range(1, closing_img.shape[1] - 1):
            if not (closing_img[maximum_histogram_index - 1][i] or
                    closing_img[maximum_histogram_index + 1][i] or
                    closing_img[maximum_histogram_index - 1][i - 1] or
                    closing_img[maximum_histogram_index - 1][i + 1] or

                    closing_img[maximum_histogram_index + 1][i - 1] or
                    closing_img[maximum_histogram_index + 1][i + 1]):
                closing_img[maximum_histogram_index - 2][i] = 0
                closing_img[maximum_histogram_index - 1][i] = 0
                closing_img[maximum_histogram_index][i] = 0

            elif (closing_img[maximum_histogram_index][i] != 0 and
                  closing_img[maximum_histogram_index - 1][i + 1] != 0 and
                  closing_img[maximum_histogram_index][i + 1] == 0 and
                  closing_img[maximum_histogram_index - 1][i + 2] == 0 and
                  closing_img[maximum_histogram_index - 1][i] == 0 and
                  closing_img[maximum_histogram_index - 2][i + 1] == 0 and
                  closing_img[maximum_histogram_index + 1][i] == 0 and
                  closing_img[maximum_histogram_index - 2][i + 2] == 0 and
                  closing_img[maximum_histogram_index - 2][i] == 0):

                closing_img[maximum_histogram_index][i] = 0
                closing_img[maximum_histogram_index - 1][i + 1] = 0

            elif (closing_img[maximum_histogram_index][i] != 0 and
                  closing_img[maximum_histogram_index - 1][i - 1] != 0 and
                  closing_img[maximum_histogram_index - 1][i] == 0 and
                  closing_img[maximum_histogram_index - 1][i - 2] == 0 and
                  closing_img[maximum_histogram_index - 2][i] == 0 and
                  closing_img[maximum_histogram_index][i - 1] == 0 and
                  closing_img[maximum_histogram_index + 1][i] == 0 and
                  closing_img[maximum_histogram_index - 2][i - 2] == 0 and
                  closing_img[maximum_histogram_index - 2][i] == 0):

                closing_img[maximum_histogram_index][i] = 0
                closing_img[maximum_histogram_index - 1][i - 1] = 0

            elif (closing_img[maximum_histogram_index][i] != 0 and
                  closing_img[maximum_histogram_index + 1][i - 1] != 0 and
                  closing_img[maximum_histogram_index - 1][i] == 0 and
                  closing_img[maximum_histogram_index][i - 1] == 0 and
                  closing_img[maximum_histogram_index + 1][i - 2] == 0 and
                  closing_img[maximum_histogram_index + 2][i - 1] == 0 and
                  closing_img[maximum_histogram_index + 1][i] == 0 and
                  closing_img[maximum_histogram_index - 1][i + 1] == 0):

                closing_img[maximum_histogram_index][i] = 0

            elif (closing_img[maximum_histogram_index][i] != 0 and
                  closing_img[maximum_histogram_index + 1][i + 1] != 0 and
                  closing_img[maximum_histogram_index][i + 1] == 0 and
                  closing_img[maximum_histogram_index + 2][i + 1] == 0 and
                  closing_img[maximum_histogram_index + 1][i] == 0 and
                  closing_img[maximum_histogram_index - 1][i] == 0 and
                  closing_img[maximum_histogram_index - 1][i - 1] == 0):

                closing_img[maximum_histogram_index][i] = 0


            else:
                x = maximum_histogram_index
                y = i

                count = 0
                up = False
                while True:
                    next_ = False
                    if closing_img[x - 1][y] == 255:
                        x -= 1
                        next_ = True
                        count += 1
                        up = True
                    elif closing_img[x - 1][y + 1] == 255:
                        x -= 1
                        y += 1
                        next_ = True
                        count += 1
                        up = True
                    elif closing_img[x - 1][y - 1] == 255:
                        x -= 1
                        y -= 1
                        next_ = True
                        count += 1
                        up = True

                    elif closing_img[x][y + 1] == 255 and count > 6:
                        y += 1
                        next_ = True
                        count += 1
                    if closing_img[x + 1][y + 1] == 255 and count > 20 and up:
                        rec_row, rec_col = rectangle((x, y), extent=(8, 20), shape=closing_img.shape)
                        closing_img[rec_row, rec_col] = 0
                        x += 1
                        y += 1
                        break

                    if next_ == False:
                        break

            if closing_img[maximum_histogram_index - 2][i] == 255:
                rr, cc = line(maximum_histogram_index - 1, i - 4, maximum_histogram_index - 1, i - 15)
                closing_img[rr, cc] = 0
                rr, cc = line(maximum_histogram_index - 2, i - 4, maximum_histogram_index - 2, i - 15)
                closing_img[rr, cc] = 0
                rr, cc = line(maximum_histogram_index - 3, i - 4, maximum_histogram_index - 3, i - 15)
                closing_img[rr, cc] = 0
                rr, cc = line(maximum_histogram_index - 4, i - 4, maximum_histogram_index - 4, i - 15)
                closing_img[rr, cc] = 0
                rr, cc = line(maximum_histogram_index, i - 4, maximum_histogram_index, i - 15)
                closing_img[rr, cc] = 0

        closing_img = closing(closing_img, square(3))
        closing_img = opening(closing_img, square(1))

        '''
        Base Line Detection
        '''

        for index, val in enumerate(histogram[0]):
            # flag = 0
            if 256 < histogram[0][index] <= 2550 and index > 40:
                for i in range(closing_img.shape[1] - 1):
                    closing_img[index][i] = False
                    closing_img[index + 2][i] = False
                    closing_img[index + 1][i] = False
                    closing_img[index + 3][i] = False

                break
        closing_image = closing_img * 255
        # imageio.imwrite(r"\pic\base" + str(image_count) + ".jpg", closing_image)
        return closing_image


    def character_extractor(self, path):
        global ax, row, column, lines, imgs, image, histogram
        inp_img = io.imread(path, as_gray=True)
        fig, ax = plt.subplots(figsize=(10, 10))
        row, column = inp_img.shape
        lines = self.line_separation(inp_img)
        imgs = []
        line_count = self.line_counter(inp_img)
        image_count = 1
        sentence_list = []
        for image in imgs:

            closing_image2 = np.copy(image)
            new_ = self.line_and_base_seperation(image, image_count)
            histogram = closing_image2.sum(axis=0).reshape(1, -1)

            maximum_histogram_index = np.argmax(histogram)
            closing_img = np.copy(closing_image2)

            word_marked = np.copy(closing_img)
            label_image = label(word_marked)
            image_num = 1
            for region in regionprops(label_image):
                minr, minc, maxr, maxc = region.bbox
                rec_row, rec_col = rectangle((minr - 5, minc - 5), end=(maxr + 5, maxc + 5), shape=word_marked.shape)
                word_marked[rec_row, rec_col] = 255
                # img = region.image * 255

            word_marked_90 = np.rot90(word_marked, 3)
            closing_image_90 = np.rot90(new_, 3)
            label_image = label(word_marked_90)
            image_num = 2
            word_list = []
            for region in regionprops(label_image):
                minr, minc, maxr, maxc = region.bbox
                # print(region.bbox)
                img = closing_image_90[minr:maxr, minc:maxc] * 255
                imageio.imwrite(r"\pic\\" + str(image_count) + "_" + str(image_num) + ".PNG",
                                np.rot90(dilation(img, square(2)), 1))
                img_90 = dilation(img, square(2))
                label_word_image = label(img_90)
                word_image_num = 0
                plt.imshow(label_word_image)
                plt.show()
                # character_list = []
                for char_region in regionprops(label_word_image):
                    if char_region.area > 0:
                        c_minr, c_minc, c_maxr, c_maxc = char_region.bbox
                        # print(char_region.bbox, char_region.area)
                        char_img = (char_region.image)
                        # char_img = img_90[c_minr:c_maxr, c_minc:c_maxc]*255
                        char_img = np.rot90(char_img, 1)

                        char_img = resize(char_img, (250, 250))
                        if char_region.area < 10 and c_minc < 43:

                            # character_list.append("fota")
                            continue
                        elif char_region.area >= 13:
                            imageio.imwrite(
                                r"\pic\char18\\" + str(image_count) + "_" + str(image_num) + "_" + str(
                                    word_image_num) + ".PNG", char_img)
                            word_image_num += 1
                        else:
                            continue

                # word_list.append(character_list)
                image_num += 1
            sentence_list.append(word_list)

            image_count += 1
