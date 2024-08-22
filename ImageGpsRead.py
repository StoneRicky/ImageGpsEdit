from PIL import Image
from PIL.ExifTags import TAGS
from fractions import Fraction

# 获取图片的GPS信息
def get_gps_info(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    print(exif_data)
    if exif_data is not None:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                print(value)
                return value

    return None


# dms转十进制
def dms_to_decimal(degree,minute,second):
    decimal = degree + minute/60 + second/60/60
    return decimal

if __name__ == '__main__':
    
    image_path = 'D:\\IMG_2687.jpeg'

    gps_info = get_gps_info(image_path)
    
        #                      纬度               经度             高度
    print("GPS信息：\n", gps_info[2],"\n",gps_info[4],"\n",gps_info[6])
    print("十进制:")
    print(dms_to_decimal(float(gps_info[2][0]),float(gps_info[2][1]),float(gps_info[2][2])),",",dms_to_decimal(float(gps_info[4][0]),float(gps_info[4][1]),float(gps_info[4][2])))