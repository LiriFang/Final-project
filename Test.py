import numpy as np
import pandas as pd
from datetime import datetime
# Module-level Variable
from scipy.stats import norm

# unit checking time for the system
UNIT_TIME = 5
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
    pass

class RandomCarInGenerator():
    def __init__(self, hour:int, minute:int):
        self.hour = hour
        self.minute = minute
        File = 'course.csv'

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

    @staticmethod
    def BionomialDist(n, p):
        np.random.binomial(n, p)


    def CarInDist(self, unit_time=1):
        """
        :param time: checking time
        :return: car in distribution around starting time of class
        >>> RandomCarInGenerator.CarInDist(RandomCarInGenerator)
        """
        car_num_unit_time = {'day':[],'hour':[], 'minute':[], 'carIn':[]}
        number = self.PersonRegistered(dataFile='course.csv')
        person_uniform = self.PersonIn()
        car_uniform = self.CarInPercent()
        car_num_hour = number * person_uniform * car_uniform

        for day in car_num_hour.columns:
            for hour in car_num_hour.index:
                for i in range(0, 61, unit_time):
                    X_e = i/unit_time + unit_time/2
                    X_s = i/unit_time - unit_time/2
                    car_dist_curr = norm.cdf(X_e, loc=50/unit_time, scale=10/unit_time) - norm.cdf(X_s, loc=50/unit_time, scale=10/unit_time)
                    car_num_bio = np.random.binomial(car_num_hour[day][hour], car_dist_curr)

                    car_num_unit_time['day'].append(day)
                    car_num_unit_time['hour'].append(hour)
                    car_num_unit_time['minute'].append(i)
                    car_num_unit_time['carIn'].append(car_num_bio)

        car_num_unit_time = pd.DataFrame(car_num_unit_time)

        return car_num_unit_time


    def CarInError(self, time: datetime):
        """
        :param time: checking time
        :return: Error number of Car (skewed_distribution)
        """
        pass

car = RandomCarInGenerator(9, 60)
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
        # user_string = 'Empty parking places on each street:\n'
        # for i in range(len(empties)):
        #     user_string = user_string + PARKINGLOTSMAPPING[i] + ': ' + str(empties[i]) + '\n'
        # return (user_string)

        # get number of empty places on each street
        empty_records = pd.DataFrame.from_csv('EmptyRecords.csv', sep = ',', index_col = None)
        empties = empty_records.astype(bool).sum(axis=0)
        user_string = 'The probability of each street to find an empty parking place:\n'
        for i in range(len(empties)):
            probability = '{:.2f}%'.format(empties[i] / len(empty_records) * 100)
            user_string = user_string + 'PARKINGLOTSMAPPING[i]' + ':' + str(probability) + '\n'

        return(user_string)





print(ParkingSystem.CalculateParkingProbability(ParkingSystem, PARKINGLOTS_TEST))
ParkingSystem.UnitTimeCheck(ParkingSystem, PARKINGLOTS_TEST)
