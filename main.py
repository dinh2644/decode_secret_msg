from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import sys


# Takes in one argument, which is a string containing the URL for the Google Doc with the input data
def decode(req, DEBUG_MODE):
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
       extract_table(html_data, DEBUG_MODE)


def extract_table(html_data, DEBUG_MODE):
    soup = BeautifulSoup(html_data, 'html.parser')
    relevant_data = list(soup.find_all(class_="c0"))

    # Since the doc changes every 5 mins, ensure that len of table is 25 for below logic to work
    table = relevant_data[5:] if len(relevant_data) == 30 else relevant_data[3:]     

    # Setup relevant html into a list of list to print the 2d array
    arr_2d_dict = {} # x-coord : []char

    if DEBUG_MODE == 0:
        # Process each row into its own arrays through a hash map, e.g. { x_coord : [char, char] } 
        is_new_row = 0
        for i in range(len(table)):
            is_new_row = i % 3

            if is_new_row == 0:
                if table[i].text not in arr_2d_dict:
                    if i + 2 <= len(table):
                        # Handle non 0 y_coordinate case
                        if table[i + 2] != 0:
                            y_coord = int(table[i + 2].text)
                            arr_2d_dict[table[i].text] = [" " for _ in range(y_coord)] # append necessary empty strs before placing the char in correct position
                            arr_2d_dict[table[i].text].append(table[i + 1].text)
                        else:
                            arr_2d_dict[table[i].text] = [table[i + 1].text]
                else:
                    if i + 2 <= len(table):
                        # Handle non 0 y_coordinate case
                        if table[i + 2] != 0:
                            y_coord = int(table[i + 2].text)
                            for x in range(y_coord): 
                                if arr_2d_dict[table[i].text][x] == None: # make sure we don't add empty strs in occuped positions
                                    arr_2d_dict[table[x].text].append(" ") # append necessary empty strs before placing the char in correct position
                            arr_2d_dict[table[i].text].append(table[i + 1].text)
                        else:
                            arr_2d_dict[table[i].text].append(table[i + 1].text)
        # Construct 2D array from arrays in hashmap
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

        # Print result
        for row in arr_2d:
            for char in row:
                print(char, end="")
            print()

        print(arr_2d)
    else:
        for row in table:
            print(row)
        print(len(table))
    

                    
def main():
    if len(sys.argv) != 2:
        print("USAGE: python main.py <DEBUG_MODE 1=YES, 0=NO")
        return 1 
        
    DEBUG_MODE = int(sys.argv[1])
    req = Request('https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub')
    decode(req, DEBUG_MODE)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
    

