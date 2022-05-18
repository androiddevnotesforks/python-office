from functools import cache, cached_property


class ImgReader:
    """
    image reader with lazy processing
    @Author & Date:CNSeniorious000 2022/5/17
    """

    def __init__(self, path: str, lang=("en", "ch_sim")):
        self.path = path
        self.lang = lang

    @cached_property
    def reader(self):
        from easyocr import Reader
        return Reader(self.lang)

    @cached_property
    def image(self):
        import cv2
        return cv2.imread(self.path)

    @staticmethod
    def show(image):
        from matplotlib.pyplot import imshow, show
        imshow(image)
        return show()

    @cached_property
    def texts(self):
        return self.reader.readtext(self.image)

    def render_bbox(self, color=(255, 0, 0)):
        from cv2 import line
        image = self.image.copy()
        for points, string, degree in self.texts:
            c = (*color, round(degree * 255))
            # noinspection PyPep8Naming
            A, B, C, D = [tuple(map(round, point)) for point in points]
            line(image, A, B, c)
            line(image, B, C, c)
            line(image, C, D, c)
            line(image, D, A, c)

        return image

    def show_image_with_bbox(self, color=(255, 0, 0)):
        return self.show(self.render_bbox(color))

    def classify(self, choices, page=0, *args, **kwargs):
        """
        返回choices中与图片ocr结果中匹配度最高的结果匹配度最高的一项
        :param page: the page to ocr
        :param choices: list or words to choose
        """
        from rapidfuzz.process import extractOne
        texts = [string for _, string, _ in self.texts]
        return sorted((extractOne(choice, texts)[1], choice) for choice in choices)[-1][1]
