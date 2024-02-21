from PIL import Image
from PIL.ExifTags import TAGS
import piexif
from fractions import Fraction

# 获取图片的GPS信息
def get_gps_info(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()

    if exif_data is not None:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                return value

    return None

# 向文件中写入GPS信息   path、 经度 、纬度 、 高度
def write_gps_info(image_path, gps_longitude,gps_latitude, gps_altitude):
    # 打开图片
    image = Image.open(image_path)

    # 创建一个空的Exif数据
    exif_dict = {"GPS": {}}

    # 构建GPS信息
    gps_info = {
        piexif.GPSIFD.GPSLatitude: _convert_to_dms(gps_longitude),
        piexif.GPSIFD.GPSLongitude: _convert_to_dms(gps_latitude),
        piexif.GPSIFD.GPSAltitude: (gps_altitude,1000),  # 将高度转换为以毫米为单位
    }

    print(gps_info)

    # 将GPS信息插入到Exif数据中
    exif_dict["GPS"] = gps_info

    # # 将修改后的Exif数据重新写入图片
    exif_bytes = piexif.dump(exif_dict)
    image.save(image_path, exif=exif_bytes)

def _convert_to_dms(coordinate):
    degrees = int(coordinate[0])
    minutes = int(coordinate[1])
    seconds = int(coordinate[2] * 10000)
    dms = ((degrees, 1), (minutes, 1), (seconds, 10000))
    return dms

if __name__ == '__main__':
    image_path = 'C:\projects\img_enhance\IMG\DJI_0001.JPG'
    wait_image_path = 'C:\projects\yolov8\datasets\solar\images\Undistort_IMGDJI_0001.JPG'

    gps_info = get_gps_info(image_path)
    #                      经度          纬度        高度
    print("图片的GPS信息：", gps_info[2],gps_info[4],gps_info[6])

    gps_altitude = int(gps_info[6]*1000)

    write_gps_info(wait_image_path,gps_info[2],gps_info[4],gps_altitude)
    print("{} 图片写入完成".format(wait_image_path))