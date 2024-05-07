from PIL import Image
from PIL.ExifTags import TAGS
import piexif

# 获取图片的GPS信息
def get_gps_info(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    # print(exif_data)
    if exif_data is not None:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                print(value)
                return value

    return None

# 向文件中写入GPS信息   path、 纬度 、经度 、 高度
def write_gps_info(image_path, gps_latitude,gps_longitude, gps_altitude):
    # 打开图片
    image = Image.open(image_path)
    # 修改GPS信息
    exif_dict = piexif.load(image.info['exif'])
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = _convert_to_dms(gps_latitude)
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = _convert_to_dms(gps_longitude)
    # 高度不更改
    # exif_dict['GPS'][piexif.GPSIFD.GPSAltitude] = (gps_altitude,1000)
    

    # # 将修改后的Exif数据重新写入图片
    # print(exif_dict)
    exif_bytes = piexif.dump(exif_dict)
    image.save(image_path,quality = 90,exif=exif_bytes)
    
    print("{} 图片写入完成".format(image_path))

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
    second = (decimal - degree) * 3600 % 60 # 保留两位小数（为了准确性，暂不四舍五入）
    
    return (degree,minute,second)

# dms转十进制
def dms_to_decimal(degree,minute,second):
    decimal = degree + minute/60 + second/60/60
    return decimal

if __name__ == '__main__':
    # 文件
    image_path = 'D:\\IMG_5060.jpeg'

    gps_info = get_gps_info(image_path)
    #                      纬度               经度             高度
    print("源文件GPS信息：\n", gps_info[2],"\n",gps_info[4],"\n",gps_info[6])
    print("十进制:")
    print(dms_to_decimal(float(gps_info[2][0]),float(gps_info[2][1]),float(gps_info[2][2])))
    print(dms_to_decimal(float(gps_info[4][0]),float(gps_info[4][1]),float(gps_info[4][2])))
    # 自定义纬度
    latEdit = 30.632045651757736
    # 自定义经度度
    longEdit = 104.06306964563989
     
    # 自定义高度
    # alEdit = 66
    alEdit =gps_info[6] #取原有高度
    
    gps_info[2] = decimal_to_dms(latEdit)
    gps_info[4] = decimal_to_dms(longEdit)
    
    print('修改后的坐标信息：')
    print(gps_info[2])
    print(gps_info[4])
    print("十进制:")
    print(latEdit,',',longEdit)
    # gps_info[2] = (36.0, 3.0, 42.199999999)
    # gps_info[4] = (120.0, 18.0, 35.59)
    gps_altitude = int(alEdit*1000)
    write_gps_info(image_path,gps_info[2],gps_info[4],gps_altitude)