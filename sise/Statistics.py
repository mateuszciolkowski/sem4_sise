#dlugosc znalezionego roziwazania path
#liczbe stanow odwiedzonych
#liczba stanow przetworzonych
#maksymalna osiagniegta glebokosc rekursji
#czas trwaania w miliusekundach
import time


class Statistics:
    def __init__(self):
        self.path = ""
        self.max_depth_reached = 0

        self.isSolved = False

        self.visited_states = 0
        self.processed_states = 0

        self.time_start = time.time()
        self.time_end = 0
        self.time_reached = 0

    def stop_timer(self):
        time_end=time.time()
        self.time_reached=time_end-self.time_start

    def to_string(self):
            if self.path:
                print("Path: "+self.path)
                print("Path length: " + str(len(self.path)))
            if self.max_depth_reached:
                print("Max depth reached: "+str(self.max_depth_reached))
            if self.visited_states:
                print("Visited states: "+str(self.visited_states))
            if self.processed_states:
                print("Processed states: "+str(self.processed_states))
            if self.time_reached:
                print("Time reached: "+str(self.time_reached))
