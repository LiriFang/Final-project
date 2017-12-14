import numpy as np
import pandas as pd
from datetime import datetime
# Module-level Variable
from scipy.stats import norm

# unit checking time for the system
UNIT_TIME = 5
# Parameter for Pert distribution
MODIFIED_LAMBDA = 4
# Each array represents a street. The length of array represents the number of meters on that street, and the item in the array represents the time that the car will stoped.
DANIELSTREET = np.zeros(23)
SIXTHSTREET = np.zeros(30)
CHALMERSSTREET = np.zeros(23)
FIFTHSTREET = np.zeros(10)
STREET = np.zeros(4)
# whole parking lots around iSchool
PARKINGLOTSMAPPING = {0:'DANIELSTREET', 1: 'SIXTHSTREET', 2: 'CHALMERSSTREET', 3: 'FIFTHSTREET', 4: 'STREET'}
PARKINGLOTS = np.array([DANIELSTREET, SIXTHSTREET, CHALMERSSTREET, FIFTHSTREET, STREET])
DANIELSTREET_T = np.array([5, 1, 4])
SIXTHSTREET_T = np.array([0, 0, 30])
PARKINGLOTS_TEST = np.array([DANIELSTREET_T, SIXTHSTREET_T])


class RandomDurationTimeGenerator():
    def CarStayDuration(self, sampleNumber, low=1, mode=3, high=4):
        """
        This function is to produce random numbers according to the 'Modified PERT' distribution.
        :param sampleNumber: The number of the random sample. This would be defined by our parking system.
        :param sampleNumber: The number of the random sample. This would be defined by our parking system.
        :param low: The lowest value expected as possible. 1h is expected here because the shortest class duration is 1h.
        :param mode: The 'most likely' statistical value. 3h is expected here because the most likely class duration is 3h.
        :param high: The highest value expected as possible, 4h is expected here because the longest allowed parking is 4h.
        :return: a numpy array with random numbers that fit a PERT distribution

        """
        # Generate the parameters of Beta Distribution according to Paulo Buchsbaum's Formula:
        mean = (low + MODIFIED_LAMBDA * mode + high) / (MODIFIED_LAMBDA + 2)
        ss = (high - 2 * mode + low) / (mean - mode)
        a = (mean - low) / (high - low) * ss
        b = (high - mean) / (high - low) * ss

        # Generate the random number with Beta distribution and return the minutes
        duration_h = np.random.beta(a, b, sampleNumber)
        duration_m = int(np.ceil(60 * (duration_h * (high - low) + low)))
        return duration_m

    def ErrorStayDuration(self):
        car_stay_error = int(np.random.uniform(20, 61))
        return car_stay_error


class RandomCarInGenerator():
    def __init__(self, hour:int, minute:int):
        self.hour = hour
        self.minute = minute

    def PersonRegistered(self, dataFile):
        number = pd.read_csv(dataFile, index_col='hour')
        return number

    def PersonIn(self):
        """
        :return: (distribution)number of person attending in the class
        """
        person_uniform = np.random.uniform(0.5, 0.9)
        #person_attended = number * person_uniform
        return person_uniform

    def CarInPercent(self):
        """
        :return: percentage of person who drive car and stop the car in the parking area
        """
        car_uniform = np.random.uniform(0.3, 0.5)
        #car_num = car_uniform * person_attended
        return car_uniform



    def CarInDist(self):
        """
        :param time: checking time
        :return: car in distribution around starting time of class
        >>> RandomCarInGenerator.CarInDist(RandomCarInGenerator)
        """
        minute = self.minute
        hour = self.hour

        if minute >= 50:
            Y = (minute-50)/UNIT_TIME
        elif minute < 50:
            Y = minute/UNIT_TIME + 10/UNIT_TIME
        X = minute/UNIT_TIME
         #former

        number = self.PersonRegistered(dataFile='Course List.csv')
        person_uniform = self.PersonIn()
        car_uniform = self.CarInPercent()
        car_num_hour = number * person_uniform * car_uniform

        car_dist_curr = norm.pdf(X, loc=50/UNIT_TIME, scale=30/UNIT_TIME)
        car_curr = car_dist_curr * car_num_hour.iloc[hour]
        car_dist_fmr = norm.pdf(Y, loc=50/UNIT_TIME, scale=30/UNIT_TIME)


        car_fmr = car_dist_fmr * car_num_hour.iloc[hour + 1]
        print (car_num_hour.iloc[hour], car_num_hour.iloc[hour+1])
        car_num_unit_time = int(car_curr + car_fmr)
        return car_num_unit_time


    def CarInError(self):
        """
        :param time: checking time
        :return: Error number of Car (uniform_distribution)
        """
        car_in_error = np.random.uniform(-2, 2)
        car_in_error = int(car_in_error)
        if car_in_error < 0:
            car_in_error = 0

        return car_in_error


car = RandomCarInGenerator(9, 50)
print(car.CarInDist())


class ParkingLot():

    def FindParkingMeter(self, parking_status: np.array):
        '''
        This function is used to find which place is empty
        :param parking_status: status of current parking lots
        :return: index of available street(index) and the empty place on that street(index). None means no empty parking place.

        >>> ParkingLot.FindParkingMeter(ParkingLot, PARKINGLOTS_TEST)
        [1, 0]
        '''

        status = ParkingSystem.CheckParkingStatus(ParkingSystem, parking_status)
        # find out which street is available for parking
        availabel_street = np.nonzero(status[0])[0][0]

        if availabel_street == None:
            return None
        else:
            # get the first empty parking place on that street
            empty_place = np.where(parking_status[availabel_street] == 0)[0][0]
            return [availabel_street, empty_place]

class ParkingSystem():

    def UnitTimeCheck(self, parking_status: np.array):
        '''
        This function is used to check current parking lot status every UNIT_TIME
        :param parking_status: status of current parking lot
        :return: parking stutus

        >>> ParkingSystem.UnitTimeCheck(ParkingSystem, PARKINGLOTS_TEST)
        array([[ 0,  5,  0],
               [ 0,  0, 25]])
        '''
        parking_status = parking_status - UNIT_TIME
        for street in parking_status:
            error = street < 0
            street[error] = 0
        return parking_status

    def Parking(self, parking_status: np.array, duration_time: int):
        '''
        This function is used to parking a car
        :param location: the location to park the car
        :param parking_status: status of current parking lot
        :param duration_time: parking duration time of the car in minutes
        :return: parking status. None meas no empty parking place.

        >>> ParkingSystem.Parking(ParkingSystem, PARKINGLOTS_TEST, 90)
        array([[ 5, 10,  4],
               [90,  0, 30]])
        '''

        location = ParkingLot.FindParkingMeter(ParkingLot, parking_status)
        if location == None:
            return None
        else:
            parking_status[location[0]][location[1]] = duration_time

        return parking_status


    def CheckParkingStatus(self, parking_status: np.array):
        '''
        This function is used to calculate number of empty place and occupied place
        :param parking_status: status of current parking lot
        :return: number of empty place and occupied place for each parking lot

        >>> ParkingSystem.CheckParkingStatus(ParkingSystem, PARKINGLOTS_TEST)
        ([0, 2], [3, 1])
        '''
        empties = []
        occupies = []
        for street in parking_status:
            empty = np.where(street == 0)
            empty_num = len(empty[0])
            empties.append(empty_num)
            occupy_num = len(street) - empty_num
            occupies.append(occupy_num)

        # write the empty records into a csv file
        with open('EmptyRecords.csv', 'a') as er:
            for i in range(len(empties) - 1):
                er.write(str(empties[i]) + ',' )
            er.write(str(empties[-1]) + '\n')

        return (empties, occupies)


    def CalculateParkingProbability(self, parking_status: np.array):
        '''
        This function is used to calculate probability
        :param parking_status:
        :return: parking probability
        '''
        status = self.CheckParkingStatus(self, parking_status)
        empties = status[0]
        occupies = status[1]

        # get number of empty places on each street
        empty_records = pd.DataFrame.from_csv('EmptyRecords.csv', sep = ',', index_col = None)
        empties = empty_records.astype(bool).sum(axis=0)
        user_string = 'The probability of each street to find an empty parking place:\n'
        for i in range(len(empties)):
            probability = '{:.2f}%'.format(empties[i] / len(empty_records) * 100)
            user_string = user_string + PARKINGLOTSMAPPING[i] + ':' + str(probability) + '\n'

        return(user_string)


class iSchoolParkingSimulator():

    def __init__(self):
        self.input_hours = 0
        self.input_minutes = 0

    def Main(self):
        require_time = input("Please enter the time you want to check (e.g.: 8:20):")
        require_time = require_time.split(':')
        self.input_hours = int(require_time[0])
        self.input_minutes = int(require_time[1])
        # The system will start from 8:00
        # Calculate the times to operate the UNIT simulation process
        simulation_times = ((self.input_hours - 8) * 60 + require_time[1]) / UNIT_TIME
        # Repeate the simulation 100 times
        for i in range(100):
            # Simulate the process of parking
            for j in range(simulation_times):
                self.UnitSimulation(self, )

    def UnitSimulation(self, current_hour: int):
        parking_system = ParkingSystem()
        parking_system.UnitTimeCheck()





# s = iSchoolParkingSimulator.Main(iSchoolParkingSimulator)
