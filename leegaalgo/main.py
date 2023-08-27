import csv

LEEGA_DIFF = 0.05

list_of_stocks = []
todays_data = dict()
prev_data = dict()


def calculate_cpr(high, low, close):
    # Calculate the Pivot Point (PP)
    pivot = (high + low + close) / 3.
    bottom_p = (high + low) / 2.
    top_p = (pivot - bottom_p) + pivot

    # Return the Pivot Point, Upper Resistance Level, and Lower Support Level
    return top_p, pivot, bottom_p


def calculate_closeness(top_p, pivot, bottom_p):
    pivot_diff = ((pivot - pivot) / pivot) * 100
    bottom_diff = ((bottom_p - pivot) / pivot) * 100
    top_diff = ((top_p - pivot) / pivot) * 100

    return top_diff, pivot_diff, bottom_diff


def check_prev_today_diff(prev_t, prev_b, today_t, today_b):
    today_diff = abs(today_t - today_b)
    prev_diff = abs(prev_t - prev_b)
    if today_diff < prev_diff:
        return True
    return False


def get_nifty500():
    print("Getting List of Stocks")
    global list_of_stocks
    file_name = 'nifty500.csv'
    with open(file_name, mode='r') as file:
        csvFile = csv.reader(file)

        # displaying the contents of the CSV file
        cnt = 0
        for lines in csvFile:
            if cnt == 0:
                cnt += 1
                continue
            if lines[3] == "EQ":
                list_of_stocks.append(lines[2])
            cnt += 1


def get_today_stock_data():
    global todays_data
    file_name = "input.csv"
    with open(file_name, mode='r') as file:
        csvFile = csv.reader(file)
        cnt = 0
        open_index = 4
        high_index = 5
        low_index = 6
        close_index = 7
        last_index = 8
        series_type = 1

        for lines in csvFile:
            if cnt == 0:
                symbol = lines.index("SYMBOL")
                open_index = lines.index("OPEN")
                high_index = lines.index("HIGH")
                low_index = lines.index("LOW")
                close_index = lines.index("CLOSE")
                last_index = lines.index("LAST")
                series_type = lines.index("SERIES")
                cnt += 1
                continue
            if lines[series_type] == "EQ":
                todays_data[lines[symbol]] = {
                    "OPEN": lines[open_index],
                    "HIGH": lines[high_index],
                    "LOW": lines[low_index],
                    "CLOSE": lines[close_index],
                    "LAST": lines[last_index]
                }


def get_prev_data():
    global prev_data
    file_name = "prev.csv"
    with open(file_name, mode='r') as file:
        csvFile = csv.reader(file)
        cnt = 0
        open_index = 4
        high_index = 5
        low_index = 6
        close_index = 7
        last_index = 8

        for lines in csvFile:
            if cnt == 0:
                open_index = lines.index("OPEN")
                high_index = lines.index("HIGH")
                low_index = lines.index("LOW")
                close_index = lines.index("CLOSE")
                last_index = lines.index("LAST")
                cnt += 1
                continue
            prev_data[lines[1]] = {
                "OPEN": lines[open_index],
                "HIGH": lines[high_index],
                "LOW": lines[low_index],
                "CLOSE": lines[close_index],
                "LAST": lines[last_index]
            }


if __name__ == "__main__":
    get_nifty500()
    get_today_stock_data()

    cnt = 0
    for each_stock in list_of_stocks:
        try:
            high_price = todays_data[each_stock]["HIGH"]
            low_price = todays_data[each_stock]["LOW"]
            closing_price = todays_data[each_stock]["CLOSE"]
            topp, pp, bp = calculate_cpr(float(high_price), float(low_price), float(closing_price))
            top_diff, piv_diff, btm_diff = calculate_closeness(topp, pp, bp)
            if (abs(top_diff) + abs(btm_diff)) < LEEGA_DIFF:
                print(each_stock + ",", end='')
                cnt += 1
        except:
            print("")
    print("\n")
    print(cnt)