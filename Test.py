import numpy as np

# Module-level Variable
UNIT_TIME = 5
PARKINGLOT = np.array([10, 20, 0, 0])

class RandomDurationTimeGenerator():
    pass

class RandomCarInGenerator():
    pass

class ParkingLot():

    def FindParkingMeter(self, parking_status: np.array):
        '''
        This function is used to find which place is empty
        :param parking_status: status of current parking lot
        :return: index of empty place

        >>> ParkingLot.FindParkingMeter(ParkingLot, PARKINGLOT)
        2
        '''

        status = ParkingSystem.CheckParkingStatus(ParkingSystem, parking_status)
        if status[1] == 0:
            return None
        else:
            locations = np.where(parking_status == 0)
            location = locations[0][0]
        return location

class ParkingSystem():

    def UnitTimeCheck(self, parking_status: np.array):
        '''
        This function is used to check current parking lot status every UNIT_TIME
        :param parking_status: status of current parking lot
        :return: parking stutus

        >>> ParkingSystem.UnitTimeCheck(ParkingSystem, PARKINGLOT)
        array([ 5, 15,  0,  0])
        '''
        parking_status = parking_status - UNIT_TIME
        error = parking_status < 0
        parking_status[error] = 0

        return parking_status

    def Parking(self, parking_status: np.array, duration_time: int):
        '''
        This function is used to parking a car
        :param location: the location to park the car
        :param parking_status: status of current parking lot
        :param duration_time: parking duration time of the car in minutes
        :return: parking status

        >>> ParkingSystem.Parking(ParkingSystem, PARKINGLOT, 90)
        array([10, 20, 90,  0])
        '''

        location = ParkingLot.FindParkingMeter(ParkingLot, parking_status)
        if location == None:
            return None
        else:
            parking_status[location] = duration_time

        return parking_status


    def CheckParkingStatus(self, parking_status: np.array):
        '''
        This function is used to calculate number of empty place and occupied place
        :param parking_status: status of current parking lot
        :return: number of empty place and occupied place

        >>> ParkingSystem.CheckParkingStatus(ParkingSystem, PARKINGLOT)
        (2, 2)
        '''

        empties = np.where(parking_status == 0)
        empty_num = len(empties[0])
        occupy_num = len(parking_status) - empty_num

        return (occupy_num, empty_num)


    def CalculateParkingProbability(self, parking_status: np.array):
        '''
        This function is used to calculate probability
        :param parking_status:
        :return: parking probability

        >>> ParkingSystem.CalculateParkingProbability(ParkingSystem, PARKINGLOT)
        'Current occupied number: 2. Current empty number:2. Parking Probability: 0.5'
        '''
        status = self.CheckParkingStatus(self, parking_status)
        probability = status[1] / len(parking_status)
        user_string = "Current occupied number: " + str(status[0]) + ". Current empty number:" + str(status[1]) + ". Parking Probability: " + str(probability)
        return(user_string)
