import numpy as np

# Module-level Variable
UNIT_TIME = 5

class RandomDurationTimeGenerator():
    pass

class RandomCarInGenerator():
    pass

class ParkingSystem():

    def UnitTimeCheck(self, parking_status: np.array):
        '''
        This function is used to check current parking lot status every UNIT_TIME
        :param parking_status: status of current parking lot
        :return: parking stutus
        '''
        parking_status = parking_status - UNIT_TIME

        return parking_status

    def Parking(self, parking_status: np.array, duration_time: int):
        '''
        This function is used to parking a car
        :param location: the location to park the car
        :param parking_status: status of current parking lot
        :param duration_time: parking duration time of the car
        :return: parking status
        '''

        location = self.Parking(parking_status)
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
        '''

        empties = np.where(parking_status == 0)
        empty_num = len(empties)
        occupy_num = len(parking_status) - empty_num

        return (occupy_num, empty_num)

    def ParkingLot(self, parking_status: np.array):
        '''
        This function is used to find which place is empty
        :param parking_status: status of current parking lot
        :return: index of empty place
        '''
        location = None
        status = self.CheckParkingStatus(parking_status)
        if status[1] == 0:
            return None
        else:
            locations = np.where(parking_status == 0)
            location = locations[0][0]
        return location

    def CalculateParkingProbability(self, parking_status: np.array):
        '''
        This function is used to calculate probability
        :param parking_status:
        :return: parking probability
        '''
        status = self.CheckParkingStatus(parking_status)
        probability = status[0][1] / len(parking_status)
        user_string = "Current occupied number: " + status[0][0] + "\nCurrent empty number:" + status[0][1] + "\nParking Probability: "
        + probability
        return(user_string)
