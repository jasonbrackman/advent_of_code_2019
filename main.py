import day_01
import day_02
import day_03
import day_04
import day_05
from helpers import time_it_all


def main():
    codez = [day_01.run, day_02.run, day_03.run, day_04.run, day_05.run]
    time_it_all(codez)


if __name__ == "__main__":
    main()
