# Process *.jpg.cat files from CAT_DATASET


# *.jpg.cat files should be one line with the following convention, each separated by a space:
# 9 {left_eye_x} {left_eye_y} {right_eye_x} {right_eye_y} {mouth_x} {mouth_y} {left_ear_1_x} {left_ear_1_y}
# {left_ear_2_x} {left_ear_2_y} {left_ear_3_x} {left_ear_3_y} {left_ear_1_x} {right_ear_1_y} {right_ear_2_x}
# {right_ear_2_y} {right_ear_3_x} {right_ear_3_y}
# This returns tuple for each feature
def get_points(path):
    with open(path, 'r') as file:
        string = file.readline()
        if string[0] != '9':
            raise ValueError
        else:
            split_str = string.split()[1:]
            return tuple((int(loc_x), int(loc_y)) for loc_x, loc_y in zip(split_str[::2], split_str[1::2]))


def get_head(feature_points):
    x_min = min(feature_points[0][0], feature_points[1][0], feature_points[2][0])
    x_max = max(feature_points[0][0], feature_points[1][0], feature_points[2][0])
    y_min = min(feature_points[0][1], feature_points[1][1], feature_points[2][1])
    y_max = max(feature_points[0][1], feature_points[1][1], feature_points[2][1])
    # Because the head is larger than just nose and eyes
    ex = int(0.3 * (x_max - x_min))
    ey = int(0.3 * (y_max - y_min))
    return x_min - ex, y_min - ey, x_max + ex, y_max + ey


def get_ears(feature_points):
    # Left ear
    x_min_left = min(feature_points[3][0], feature_points[4][0], feature_points[5][0])
    x_max_left = max(feature_points[3][0], feature_points[4][0], feature_points[5][0])
    y_min_left = min(feature_points[3][1], feature_points[4][1], feature_points[5][1])
    y_max_left = max(feature_points[3][1], feature_points[4][1], feature_points[5][1])
    # Right ear
    x_min_right = min(feature_points[6][0], feature_points[7][0], feature_points[8][0])
    x_max_right = max(feature_points[6][0], feature_points[7][0], feature_points[8][0])
    y_min_right = min(feature_points[6][1], feature_points[7][1], feature_points[8][1])
    y_max_right = max(feature_points[6][1], feature_points[7][1], feature_points[8][1])
    return (x_min_left, y_min_left, x_max_left, y_max_left), (x_min_right, y_min_right, x_max_right, y_max_right)


if __name__ == "__main__":
    import os
    cwd = os.getcwd()
    output_list = list()
    for i in range(6):
        dir_name = "CAT_{:02d}".format(i)
        for file_name in os.listdir(dir_name):
            if file_name[-4:] == ".cat":
                points = get_points(dir_name + "/" + file_name)
                head_str = ",".join(str(point) for point in get_head(points)) + ",0"
                ear_l_str, ear_r_str = [",".join(str(point) for point in ear) + ",1" for ear in get_ears(points)]
                output_list.append(" ".join(
                    ("/".join((cwd, dir_name, file_name[:-4])), head_str, ear_l_str, ear_r_str),
                ))
    with open("data_train.txt", 'w') as output_file:
        output_file.write("\n".join(output_list))