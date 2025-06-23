from src.commands import *


class CommandFactory :
    def __init__(self ,  handlers_list):
        self.handlers  = {i.name  :  i for i in handlers_list}

    def get_handler(self , command):
        return self.handlers[command]


factory  =  CommandFactory([BalanceHandler() , CheckInHandler() , PrintSummaryHandler()])
