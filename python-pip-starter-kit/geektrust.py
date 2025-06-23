from sys import argv
from src.CommandFactory import factory
def main():
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]

    with open(file_path ,  "r") as file  :
        for line in file  :
            arr =   line.split()
            command = arr[0]
            args =  arr[1:]
            handler  = factory.get_handler(command)
            handler.handle_command(args)


    
if __name__ == "__main__":
    main()
