import string
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

"""
    Takes in one argument, which is a string containing the URL for the Google Doc with the input data
    Parameters:
        req (int): The target URL with the data to decode
    Returns:
        Stdout of the decoded unicode letters
"""
def decode(req: string): 
    try:
        response = urlopen(req)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
       html_data = response.read()
       table = extract_table(html_data)

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
            if i + 2 <= len(table) and table[i + 2].text not in arr_2d_dict:
                # Handle non 0 x_coord case, (Any positions in the grid that do not have a specified character should be filled with a space character)
                if table[i] != 0:
                    x_coord_raw = table[i].text.strip().replace(',', '')
                    if x_coord_raw:
                        try:
                            x_coord = int(x_coord_raw)
                            arr_2d_dict[table[i + 2].text] = [" " for _ in range(x_coord)]
                            arr_2d_dict[table[i + 2].text].append(table[i + 1].text)
                        except ValueError:
                            print(f"Warning: Could not convert '{x_coord_raw}' to an integer for element {i}. Skipping or using a default value.")
                else:
                    arr_2d_dict[table[i + 2].text] = [table[i + 1].text]
            else:
                if i + 2 < len(table):
                    # Handle non 0 x_coord case, (Any positions in the grid that do not have a specified character should be filled with a space character)
                    if table[i] != 0:
                        x_coord_raw = table[i].text.strip().replace(',', '')
                        if x_coord_raw:
                            try:
                                x_coord = int(x_coord_raw)
                                for x in range(x_coord): 
                                    if arr_2d_dict[table[i + 2].text][x] == None: # make sure we don't add empty strs in occupied positions
                                        arr_2d_dict[table[x].text].append(" ")
                                arr_2d_dict[table[i + 2].text].append(table[i + 1].text)
                            except ValueError:
                                print(f"Warning: Could not convert '{x_coord_raw}' to an integer for element {i}. Skipping or using a default value.")
                    else:
                        arr_2d_dict[table[i + 2].text].append(table[i + 1].text)

    # Construct a list of lists from arr_2d_dict
    arr_2d = []
    for key, val in arr_2d_dict.items():
        if key == 0:
            arr_2d.append(val)
        elif key == 1:
            arr_2d.append(val)
        elif key == 2:
            arr_2d.append(val)
        else:
            arr_2d.append(val)

    # Print 2D array from arr_2d (printing it backwards to get the Capital 'F')
    for i in range(len(arr_2d)-1, -1, -1):
        for char in arr_2d[i]:
            print(char, end="")
        print()

"""
    Helper function to simply extract the html table containing the necesary data
"""
def extract_table(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    relevant_data = list(soup.find_all(class_="c0"))

    # Since the doc changes every 5 mins, ensure that len of table is 25 for below logic to work (from my observation)
    return relevant_data[5:] if len(relevant_data) == 30 else relevant_data[3:]

if __name__ == "__main__":
    req = Request('https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub')
    decode(req)
    

