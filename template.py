from PIL import Image
import time
import os

root_dir = "./template/"
class Template:
    def __init__(self, iphone_type, fg_image):
        self.pre_dir = os.path.join(root_dir, iphone_type)
        self.image_name = os.listdir(self.pre_dir)[0]
        if(self.image_name == '.DS_Store'):
            self.image_name = os.listdir(self.pre_dir)[1]
        self.bg_image = os.path.join(self.pre_dir, self.image_name)
        self.fg_image = fg_image

        cd = list(map(int, self.image_name.split('-')[0:4]))
        self.x1 = cd[0]
        self.y1 = cd[1]
        self.x2 = cd[2]
        self.y2 = cd[3]

        fn = self.fg_image.split("/")
        fn[-1] = iphone_type + "_" + str(int(time.time())) + "_" + fn[-1]
        self.resultName = '/'.join(fn)

    def synthetic(self):
        background = Image.open(self.bg_image)  # 背景图
        foreground = Image.open(self.fg_image)  # 前景图

        foreground = foreground.resize(((self.x2 - self.x1), (self.y2 - self.y1)), Image.ANTIALIAS)
        blank = Image.new(background.mode, background.size, 0)
        blank.paste(foreground, (self.x1, self.y1))
        blank.paste(background, mask=background)
        blank.save(self.resultName)
        return self.resultName
