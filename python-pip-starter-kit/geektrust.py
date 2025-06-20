
from sys import argv

def main():
    if len (argv)!= 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    with open(file_path ,  "r") as file  :
        for line in file:
            arr = line.split()
            print(arr)
        if arr[0] == "BALANCE" :
            pass
        elif arr[0] == "CHECK_IN" :
            pass
        elif arr[0] =="PRINT_SUMMARY":
            pass

        
    

    

    
    """
    Sample code to read inputs from the file

    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, 'r')
    Lines = f.readlines()
    //Add your code here to process the input commands
    """
    
if __name__ == "__main__":
    main()