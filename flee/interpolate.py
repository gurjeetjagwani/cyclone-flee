from scipy.interpolate import interp1d
import csv

if __name__ == '__main__':

    # Setting variables for the camp
    name = "Sea_Side_Tongoa"
    start_X = 0
    start_Y = 0
    mid_X = 8
    mid_Y = 1685
    end_X = 20
    end_Y = 100

    X = [start_X, mid_X, end_X]
    Y = [start_Y, mid_Y, end_Y]

    # Finding the first interpolation with linear regression
    sample_X = int((mid_X + end_X)/2)
    y_interp = interp1d(X, Y)
    sample_Y = y_interp(sample_X)

    # Inserting it between mid and end (based on the current array at 2nd position)
    X.insert(2, sample_X)
    Y.insert(2, sample_Y.item())

    # Interpolating remaining data using quadratic regression
    for i in range (start_X + 1, end_X):
        if i != mid_X and i != end_X :
            temp_X = i
            y_interp = interp1d(X, Y, kind='quadratic')
            temp_Y = y_interp(temp_X)

            if temp_X != sample_X:
                X.insert(temp_X, temp_X)
                Y.insert(temp_X, round(temp_Y.item(), 2))

    with open(f'config_template/source_data/{name}.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the data
        index = 0
        for i in Y:
            row = [index, i]
            index += 1
            writer.writerow(row)

    print(X)
    print(Y)


