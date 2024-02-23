from PIL import Image
from PIL.ExifTags import TAGS
import piexif
from fractions import Fraction
import pickle

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

# 向文件中写入GPS信息   path、 经度 、纬度 、 高度
def write_gps_info(image_path, gps_longitude,gps_latitude, gps_altitude):
    print(gps_longitude)
    print(gps_latitude)
    print(gps_altitude)
    # 打开图片
    image = Image.open(image_path)
    # 修改GPS信息
    exif_dict = piexif.load(image.info['exif'])
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = _convert_to_dms(gps_longitude)
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = _convert_to_dms(gps_latitude)
    exif_dict['GPS'][piexif.GPSIFD.GPSAltitude] = (gps_altitude,1000)
    

    # # 将修改后的Exif数据重新写入图片
    # print(exif_dict)
    exif_bytes = piexif.dump(exif_dict)
    image.save(image_path, "jpeg", exif=exif_bytes)

def _convert_to_dms(coordinate):
    degrees = int(coordinate[0])
    minutes = int(coordinate[1])
    seconds = int(coordinate[2] * 10000)
    dms = ((degrees, 1), (minutes, 1), (seconds, 10000))
    return dms

# 十进制转dms
def decimal_to_dms(decimal):
    degree = int(decimal) # 获取度
    minute = int((decimal - degree) * 60) # 获取分钟
    second = round(((decimal - degree) * 3600 % 60), 2) # 保留两位小数并四舍五入获取秒
    
    return (degree,minute,second)

if __name__ == '__main__':
    image_path = 'D:\\old.JPG'

    gps_info = get_gps_info(image_path)
    #                      纬度          经度        高度
    print("原GPS信息：", gps_info[2],gps_info[4],gps_info[6])
    
    # 自定义纬度
    longEdit = 39.11
    # 自定义经度
    latEdit = 120.22
    # 自定义高度
    # alEdit = 66
    alEdit =gps_info[6] #取原有高度
    
    gps_info[2] = decimal_to_dms(longEdit)
    gps_info[4] = decimal_to_dms(latEdit)
    
    # gps_info[2] = (1.0, 10.0, 7.76)
    # gps_info[4] = (4.0, 28.0, 32.31)
    gps_altitude = int(alEdit*1000)
    
    write_gps_info(image_path,gps_info[2],gps_info[4],gps_altitude)
    print("{} 图片写入完成".format(image_path))