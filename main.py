import day_01
import day_02
import day_03
from helpers import time_it_all


def main():
    codez = [day_01.run, day_02.run, day_03.run]
    time_it_all(codez)


if __name__ == "__main__":
    main()
