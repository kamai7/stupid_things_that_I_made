import imageio, math
import numpy as np

ENCODE_CHARS = "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN1234567890=&"

def resize(img,ratio,file_name,transform,color_bitrate=16):
    size = int(len(img) / (222/ratio))
    parts = []
    for i in range(len(img)):
        if i%size == 0:
            r = []
            for j in range(len(img[i])):
                if j%size == 0:
                    part = []
                    rows = [row for k,row in enumerate(img) if k >= i and k < i+size and k < len(img)]
                    for row in rows:
                        pixels = [pixel for l,pixel in enumerate(row) if l >= j and l < j+size and l < len(row)]
                        part.append(pixels)
                        

                    r.append(part)

            parts.append(r)

    new_img = []
    for row in parts:
        new_row = []
        for pixels in row:
            new_row.append(transform(pixels))
        new_img.append(new_row)

    set_bitrate(new_img,color_bitrate)
    imageio.imwrite(f'tests/{file_name}',new_img)
    return new_img

def average(img):
    sumR = 0
    sumV = 0
    sumB =  0
    pixels = 0

    for rows in img:
        for pixel in rows:
            sumR += int(pixel[0])
            sumV += int(pixel[1])
            sumB += int(pixel[2])
            pixels += 1

            varR = int(sumR / pixels)
            varV = int(sumV / pixels)
            varB = int(sumB / pixels)

    return [np.uint8(varR),np.uint8(varV),np.uint8(varB)]

def median(img):
    r = []
    g = []
    b = []

    for rows in img:
        for pixel in rows:
            r.append(int(pixel[0]))
            g.append(int(pixel[1]))
            b.append(int(pixel[2]))

    r.sort()
    g.sort()
    b.sort()
    n = len(r) // 2

    if len(r)%2 == 0:
        return [np.uint8((r[n] + r[n-1]) // 2), np.uint8((g[n] + g[n-1]) // 2), np.uint8((b[n] + b[n-1]) // 2)]
    else:
        return [np.uint8(r[n]), np.uint8(g[n]), np.uint8(b[n])]

def variance(img):
    moy = average(img)
    varR = 0
    varV = 0
    varB =  0
    pixels = 0
    for rows in img:
        for pixel in rows:
            varR += int(int(pixel[0]) - int(moy[0]))**2
            varV += int(int(pixel[1]) - int(moy[1]))**2
            varB += int(int(pixel[2]) - int(moy[2]))**2
            pixels += 1

    factor = 1.1
    stdR = int(math.sqrt(varR / pixels) * factor)
    stdV = int(math.sqrt(varV / pixels) * factor)
    stdB = int(math.sqrt(varB / pixels) * factor)

    varR = int(moy[0]) + (stdR if moy[0] < 128 else -stdR)
    varV = int(moy[1]) + (stdV if moy[1] < 128 else -stdV)
    varB = int(moy[2]) + (stdB if moy[2] < 128 else -stdB)

    return [np.uint8(min(max(varR,0),255)),np.uint8(min(max(varV,0),255)),np.uint8(min(max(varB,0),255))]


def set_bitrate(img,bitrate):
    color_sapce = 255 / bitrate
    for row in img:
        for pixel in row:
            pixel[0] = np.uint8((pixel[0] // color_sapce) * color_sapce)
            pixel[1] = np.uint8((pixel[1] // color_sapce) * color_sapce)
            pixel[2] = np.uint8((pixel[2] // color_sapce) * color_sapce)

def normalize_colorspace(img, color_space):
    normalized_img = []
    for row in img:
        normalized_img.append([])
        for pixel in row:
            normalized_img[-1].append([pixel[0] // (256//bitrate),  pixel[1] // (256//bitrate), pixel[2] // (256//bitrate)])
    return normalized_img

def get_max_occ(img,pos_x,pos_y,len_x,len_y,string):
    bitrate = int(string[:2])
    counter = [0 for x in range(int(str(bitrate) + str(bitrate) + str(bitrate)))]
    for rownum in range(pos_x, pos_x + len_x):
        for pixelnum in range(pos_y, pos_y + len_y):
            counter[int(str(img[rownum][pixelnum][0]) + str(img[rownum][pixelnum][1]) + str(img[rownum][pixelnum][2]))] += 1

    max_occ = str(counter.index(max(counter)))
    while len(max_occ) < 3:
        max_occ = "0" + max_occ
    string = [int(max_occ[0]),int(max_occ[1]),int(max_occ[2])]
    return string

recurcivity_count = 0

def img_to_string(img,pos_x,pos_y,len_x,len_y,string, dominant_color = None):
    global recurcivity_count
    recurcivity_count += 1
    print("enter in img_to_string: ", pos_x, pos_y, len_x, len_y , "recurcivity : ", recurcivity_count)
    max_occ_color = get_max_occ(img,pos_x,pos_y,len_x,len_y,string)
    string_add = ""
    if dominant_color is not None:
        if dominant_color != max_occ_color:
            string_add += "," + str(pos_x) + ":" + str(pos_y) + ":" + str(len_x) + ":" + str(len_y) + ":" + str(max_occ_color[0]) + str(max_occ_color[1]) + str(max_occ_color[2])
    else:
        string_add += "," + str(pos_x) + ":" + str(pos_y) + ":" + str(len_x) + ":" + str(len_y) + ":" + str(max_occ_color[0]) + str(max_occ_color[1]) + str(max_occ_color[2])
    
    rec1 = [0,0,max(1,len_x // 2),max(1, len_y // 2)]
    rec2 = [(len_x // 2) , 0, max(1,len_x // 2),max(1, len_y // 2)]
    rec3 = [0,(len_y // 2),max(1,len_x // 2),max(1, len_y // 2)]
    rec4 = [(len_x // 2),(len_y // 2),max(1,len_x // 2),max(1, len_y // 2)]

    if len_x > 1 and len_y > 1:
        string_add += img_to_string(img,rec1[0],rec1[1],rec1[2],rec1[3],string,dominant_color = max_occ_color)
        string_add += img_to_string(img,rec2[0],rec2[1],rec2[2],rec2[3],string,dominant_color = max_occ_color)
        string_add += img_to_string(img,rec3[0],rec3[1],rec3[2],rec3[3],string,dominant_color = max_occ_color)
        string_add += img_to_string(img,rec4[0],rec4[1],rec4[2],rec4[3],string,dominant_color = max_occ_color)
    elif len_x > 1:
        string_add += img_to_string(img,rec1[0],rec1[1],rec1[2],rec1[3],string,dominant_color = max_occ_color)
        string_add += img_to_string(img,rec2[0],rec2[1],rec2[2],rec2[3],string,dominant_color = max_occ_color)
    elif len_y > 1:
        string_add += img_to_string(img,rec3[0],rec3[1],rec3[2],rec3[3],string,dominant_color = max_occ_color)
        string_add += img_to_string(img,rec4[0],rec4[1],rec4[2],rec4[3],string,dominant_color = max_occ_color)

    return string_add

bitrate = 8
divide = 8
resized_img = resize(imageio.imread('img/hihi.png'), divide,file_name="med.png",transform=median,color_bitrate=bitrate)
normalized = normalize_colorspace(resized_img,bitrate)
print(img_to_string(normalized,0,0,len(normalized[0]),len(normalized),"08"))