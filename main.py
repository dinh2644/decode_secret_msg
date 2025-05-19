from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

DEBUG_MODE = 0

"""
    Takes in one argument, which is a string containing the URL for the Google Doc with the input data
    Parameters:
        req (int): The target URL with the data to decode
    Returns:
        Stdout of the decoded unicode letters
"""


def decode(req):
    try:
        response = urlopen(req)
    except HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except URLError as e:
        print("We failed to reach a server.")
        print("Reason: ", e.reason)
    else:
        html_data = response.read()
        table = extract_table(html_data)
        if DEBUG_MODE == 1:
            print(table)
            print(len(table))

        if DEBUG_MODE == 0:
            # This will map all y_coords as keys and its associated chars as a []char where its position in array depends on its x_coord, e.g. y-coord : ['', '', square(x=3)]
            arr_2d_dict = {}
            is_new_row = 0

            for i in range(len(table)):
                """
                Process each row at a time,
                e.g. this is considered a single row, the next 3 sets is another row
                <p class="c0"><span class="c2">0</span></p> # x_coord   (i)
                <p class="c0"><span class="c2">█</span></p> # char      (i + 1)
                <p class="c0"><span class="c2">0</span></p> # y_coord   (i + 2)
                """
                is_new_row = i % 3

                if is_new_row == 0:
                    if (i + 2 < len(table)and table[i + 2].text not in arr_2d_dict):
                        # Handle non 0 x_coord case, (Any positions in the grid that do not have a specified character should be filled with a space character)
                        x_coord = int(table[i].text.strip().replace(",", ""))
                        if x_coord != 0:
                            if x_coord:
                                try:
                                    arr_2d_dict[table[i + 2].text] = [" " for _ in range(x_coord)]
                                    arr_2d_dict[table[i + 2].text][x_coord - 1] = table[i + 1].text
                                except ValueError:
                                    print(
                                        f"Warning: Could not convert '{x_coord}' to an integer for element {i}. Skipping"
                                    )
                        else:
                            arr_2d_dict[table[i + 2].text][0] = table[i + 1].text
                    else:
                        if i + 2 < len(table):
                            # Handle non 0 x_coord case, (Any positions in the grid that do not have a specified character should be filled with a space character)
                            x_coord = int((table[i].text.strip().replace(",", "")))
                            if x_coord != 0:                  
                                if x_coord:
                                    try:
                                        row = arr_2d_dict[table[i + 2].text]
                                        if x_coord > len(row):
                                            # Append spaces if targeted x_cood is > length of target array
                                            while len(row) < x_coord:
                                                row.append(" ")
                                        row[x_coord-1] = table[i + 1].text
                                    except ValueError:
                                        print(
                                            f"Warning: Could not convert '{x_coord}' to an integer for element {i}. Skipping"
                                        )
                            else:
                                arr_2d_dict[table[i + 2].text][0] = table[i + 1].text

            # Construct a list of lists from arr_2d_dict
            arr_2d = []
            sorted_dict = dict(sorted(arr_2d_dict.items()))
            for key, val in sorted_dict.items():
                if key == 0:
                    arr_2d.append(val)
                elif key == 1:
                    arr_2d.append(val)
                elif key == 2:
                    arr_2d.append(val)
                else:
                    arr_2d.append(val)

            # Print 2D array from arr_2d (printing it backwards to get the Capital 'F')
            for i in range(len(arr_2d) - 1, -1, -1):
                for char in arr_2d[i]:
                    print(char, end="")
                print() 

            # for row in arr_2d:
            #     for char in row:
            #         print(char, end="")
            #     print() 


"""
    Helper function to simply extract the html table containing the necesary data
"""


def extract_table(html_data):
    soup = BeautifulSoup(html_data, "html.parser")
    relevant_data = list(soup.find("table").find_all_next("p"))
    # specific_data = relevant_data.fin

    # We don't care about the row headers, just the data
    return relevant_data[3:]


if __name__ == "__main__":
    req = Request(
        "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
    )
    # req = Request(
    #     "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
    # )
    decode(req)
