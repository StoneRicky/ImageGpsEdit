import exifread
# 获取图片的GPS信息
def get_gps_info(image_path):
    exif_data = exifread.process_file(open(image_path,'rb'))
    return exif_data



# dms转十进制
def dms_to_decimal(degree,minute,second):
    decimal = degree + minute/60 + second/60/60
    return decimal

if __name__ == '__main__':
    
    image_path = 'D:\\IMG_1653.HEIC'

    gps_info = get_gps_info(image_path)
    
    # 纬度       
    Lat = gps_info.get('GPS GPSLatitude', '0').values
    # 经度 
    Long = gps_info.get('GPS GPSLongitude', '0').values
    
    # print(Lat)
    print("GPS信息：\n",  Lat,"\n", Long,"\n")
    print("十进制:")
    # print(dms_to_decimal(Lat[0],Lat[1],Lat[2]))
    print(dms_to_decimal(float(Lat[0]),float(Lat[1]),float(Lat[2])))
    print(dms_to_decimal(float(Long[0]),float(Long[1]),float(Long[2])))