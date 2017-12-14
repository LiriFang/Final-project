import numpy as np
import pandas as pd
from datetime import datetime
# Module-level Variable
from scipy.stats import norm

# unit checking time for the system
UNIT_TIME = 1
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
DANIELSTREET_T = np.array([0, 0, 0])
SIXTHSTREET_T = np.array([0, 0, 0])
PARKINGLOTS_TEST = np.array([DANIELSTREET_T, SIXTHSTREET_T])


class RandomDurationTimeGenerator():
    def CarStayDuration(self, sample_number, low=1, mode=3, high=4):
        """
        This function is to produce random numbers according to the 'Modified PERT' distribution.
        :param sampleNumber: The number of the random sample. This would be defined by our parking system.
        :param sampleNumber: The number of the random sample. This would be defined by our parking system.
        :param low: The lowest value expected as possible. 1h is expected here because the shortest class duration is 1h.
        :param mode: The 'most likely' statistical value. 3h is expected here because the most likely class duration is 3h.
        :param high: The highest value expected as possible, 4h is expected here because the longest allowed parking is 4h.
        :return: a numpy array with random numbers that fit a PERT distribution

        >>> RandomDurationTimeGenerator.CarStayDuration(RandomDurationTimeGenerator, 2)
        """
        # Generate the parameters of Beta Distribution according to Paulo Buchsbaum's Formula:
        mean = (low + MODIFIED_LAMBDA * mode + high) / (MODIFIED_LAMBDA + 2)
        ss = (high - 2 * mode + low) / (mean - mode)
        a = (mean - low) / (high - low) * ss
        b = (high - mean) / (high - low) * ss

        # Generate the random number with Beta distribution and return the minutes
        duration_h = np.random.beta(a, b, sample_number)
        duration_m = (np.ceil(60 * (duration_h * (high - low) + low))).astype(int)
        return duration_m

    def ErrorStayDuration(self, sample_number):
        car_stay_error = (np.random.uniform(20, 61, size = sample_number)).astype(int)
        return car_stay_error


class RandomCarInGenerator():
    def __init__(self, week: str,  hour:int, minute:int):
        self.hour = hour
        self.minute = minute
        self.week = week

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
        car_num_unit_time = {'day': [], 'hour': [], 'minute': [], 'carIn': []}
        number = self.PersonRegistered (dataFile='course.csv')
        person_uniform = self.PersonIn ()
        car_uniform = self.CarInPercent ()
        car_num_hour = number * person_uniform * car_uniform

        for day in car_num_hour.columns:
            for hour in car_num_hour.index:
                for i in range (0, 61, UNIT_TIME):
                    X_e = i / UNIT_TIME + UNIT_TIME / 2
                    X_s = i / UNIT_TIME - UNIT_TIME / 2
                    car_dist_curr = norm.cdf (X_e, loc=50 / UNIT_TIME, scale=10 / UNIT_TIME) - norm.cdf (X_s,
                                                                                                         loc=50 / UNIT_TIME,
                                                                                                         scale=10 / UNIT_TIME)
                    car_num_bio = np.random.binomial (car_num_hour[day][hour], car_dist_curr)

                    car_num_unit_time['day'].append (day)
                    car_num_unit_time['hour'].append (hour)
                    car_num_unit_time['minute'].append (i)
                    car_num_unit_time['carIn'].append (car_num_bio)

        car_num_unit_time = pd.DataFrame (car_num_unit_time)

        return car_num_unit_time

    def CarInError(self, sample_number):
        """
        :param time: checking time
        :return: Error number of Car (uniform_distribution)
        """
        car_in_error = (np.random.uniform(-2, 2, size = sample_number)).astype(int)
        e = car_in_error < 0
        car_in_error[e] = 0

        return car_in_error


# print(RandomCarInGenerator("Monday", 9, 50).CarInDist())
# print(car.CarInDist())

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
        if np.count_nonzero(status[0]) != 0:
            # find out which street is available for parking
            availabel_street = np.nonzero(status[0])[0][0]
            # get the first empty parking place on that street
            empty_place = np.where(parking_status[availabel_street] == 0)[0][0]
            return [availabel_street, empty_place]
        else:
            return None

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
        :param parking_status: status of current parking lot
        :param duration_time: parking duration time of the car in minutes
        :return: parking status. If no empty parking place, return current parking status.

        >>> ParkingSystem.Parking(ParkingSystem, PARKINGLOTS_TEST, 90)
        array([[ 5, 10,  4],
               [90,  0, 30]])
        '''

        location = ParkingLot.FindParkingMeter(ParkingLot, parking_status)
        if location == None:
            return parking_status
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


    def CalculateParkingProbability(self):
        '''
        This function is used to calculate probability
        :param parking_status:
        :return: parking probability
        '''

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
        # The system will start from 8:00
        self.start = 8
        self.parking_status = 0
        self.week = ''

    def Main(self):
        '''

        :return:
        >>> iSchoolParkingSimulator.Main(iSchoolParkingSimulator)
        '''
        require_week = input("Please enter the day you want to check (Monday ~ Friday):")
        self.week = require_week
        require_time = input("Please enter the time you want to check (e.g.: 8:20):")
        require_time = require_time.split(':')
        self.input_hours = int(require_time[0])
        self.input_minutes = int(require_time[1])
        # Calculate the times to operate the UNIT simulation process
        simulation_times = int(((self.input_hours - 8) * 60 + self.input_minutes) / UNIT_TIME)

        # Call random car generator
        r_c = RandomCarInGenerator(self.week, self.input_hours, self.input_minutes)
        # The number of car coming into the parking lot at each unit time
        car_in = r_c.CarInDist()
        car_error = r_c.CarInError(simulation_times)

        # Repeate the simulation 10 times
        for i in range(10):
            print("*********************************************************")
            print("This is the " + str(i + 1) + " time simulation the parking process.")
            hour = self.start
            minute = 0
            self.parking_status = PARKINGLOTS_TEST
            # Simulate the process of parking
            for j in range(simulation_times):
                print("----------------------------------------------------")
                print("hour" + str(hour) + " minute " + str(minute))
                car_in_number = car_in.ix[
                    (car_in['day'] == self.week) & (car_in['hour'] == hour) & (
                        car_in['minute'] == minute), 'carIn']
                car_in_number = car_in_number.get_values()[0]
                self.UnitSimulation(self.parking_status, self.week, hour, minute, car_in_number, car_error[j])
                minute = minute + 1
                if (j + 1) % 60 == 0:
                    minute = 0
                    if hour < self.input_hours:
                        hour = hour + 1



    def UnitSimulation(self, parking_status: np.array, week: int, hour: int, minute: int, car_in_number: int, car_error_number):
        parking_system = ParkingSystem()
        # Unit time checking
        self.parking_status = parking_system.UnitTimeCheck(parking_status)

        print("After unit checking:")
        print(self.parking_status)


        # The number of error car coming into the parking lot at the unit time
        print("car in:")
        print(car_in_number)
        print("error car in:")
        print(car_error_number)

        #test:
        # car_error_number = 1
        # car_in_number = 1
        r_d = RandomDurationTimeGenerator()
        if car_in_number != 0:
            # A list of duration for car to stop
            car_in_duration = r_d.CarStayDuration(car_in_number)
            print("come in duration:")
            print(car_in_duration)
            for duration in car_in_duration:
                self.parking_status = parking_system.Parking(self.parking_status, duration)

            print("After adding coming car:")
            print(self.parking_status)

        if car_error_number != 0:
            # A list of duration for error to stop
            car_error_duration = r_d.ErrorStayDuration(car_error_number)
            print("error duration:")
            print(car_error_duration)
            for duration in car_error_duration:
                self.parking_status = parking_system.Parking(self.parking_status, duration)

            print("After adding error car:")
            print(self.parking_status)


s = iSchoolParkingSimulator()
s.Main()
# Calculate probability of parking at each street
print("\n\n**************************************************")
print(ParkingSystem.CalculateParkingProbability(ParkingSystem))
