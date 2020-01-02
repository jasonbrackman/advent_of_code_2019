import day_01
import day_02
import day_03
import day_04
import day_05
import day_06
import day_07
import day_08
import day_09
import day_10
import day_11
import day_12
import day_13
import day_14
import day_15
import day_16
import day_17
import day_18
import day_19
import day_20
from helpers import time_it_all


def main():
    codez = [
        day_01.run,
        day_02.run,
        day_03.run,
        day_04.run,
        day_05.run,
        day_06.run,
        day_07.run,
        day_08.run,
        day_09.run,
        day_10.run,
        day_11.run,
        day_12.run,
        day_13.run,
        day_14.run,
        day_15.run,
        day_16.run,
        day_17.run,
        day_18.run,
        day_19.run,
        day_20.run,
    ]
    time_it_all(codez)


if __name__ == "__main__":
    main()
