
# Title: 
Simulation of Parking around iSchool

## Team Member(s):
Liri Fang, Jiawei Li, Jing Du

# Monte Carlo Simulation Scenario & Purpose:

In this project, we will design a program to simulate the daily parking senario of iSchool students. Since the parking place on campus has limited number, especially within the walking distance from the School of Information Sciences Building. Sometimes it is difficult for students to find an available place to park near the school. This project tries to using Monte Carlo simulation method to make a prediction about the probability of whether an iSchool student successfully find a vacant parking lot at a particular time. Referencing this probability, the student can decide wether drive car to the school or park the car at somewhere else rather than near the school building.

### Hypothesis before running the simulation:

1. This project only consider the meters near to the iSchool including the places on the streets and in the parking lots. We define "near" as within a block distance from iSchool. Therefore, in this project, only the parking lots on Fifth St, Sixth St, Daniel St, Chalmers St and the parking lots within the rectangle are considered.
The numebr of meters near the School of Information Science Building is: 90. The distribution of all the meters as as follows:


Street Name&nbsp;&nbsp;Number&nbsp;&nbsp;Maximum Stay&nbsp;&nbsp;Owner


E Daniel St &nbsp;&nbsp;&nbsp; 23 &nbsp;&nbsp;&nbsp; 2h &nbsp;&nbsp;&nbsp; City of Champaign


S 6th St &nbsp;&nbsp;&nbsp; 30 &nbsp;&nbsp;&nbsp; 2h &nbsp;&nbsp;&nbsp; City of Champaign


E Chalmers St &nbsp;&nbsp;&nbsp; 23 &nbsp;&nbsp;&nbsp; 4h &nbsp;&nbsp;&nbsp; City of Champaign


S 5th St &nbsp;&nbsp;&nbsp; 10 &nbsp;&nbsp;&nbsp; 2h &nbsp;&nbsp;&nbsp; City of Champaign


N/A  &nbsp;&nbsp;&nbsp; 4 &nbsp;&nbsp;&nbsp; 10h &nbsp;&nbsp;&nbsp; UIUC

2. To simplify the simulation model, we assume that meters nearing iSchool are all used by iSchool students. We suppose that most students drive to school for classes. Therefore, we assume the number of cars come to parking has a positive correlation with the class time. Since at weekends and holidays, usually there is no class, and most of the parking lots are free of charge, we suppose that there are enough available parking all day. So, we will only simulate the weekday's parking senario as this is much more meaningful.

3. Additionaly, we idealize the time that driver consumes on the finding parking place and pull over. In the simulation system, all time spend on driving will be treated as 0.

### Simulation's variables of uncertainty

In this simulation, we have two variables of uncertainty:

* Number of cars already parked
<br>We use the time schedules of each class and its capacity to estimate the current number of students in the building. Using this estimated data we can multiply a range of percentage to find out the number of cars are parked.
The range of percentage is the probability of a student has a car and he/she will drive the car to the school. This data will be generated by statistic.

* Duration of parking period of each car
<br>Considering the time period of a class is around 3 hours and usually have a break at the middle, the duration of parking period of each car in this simulation will follow the bimodal normal distribution which each peak represents a break time. 



## Instructions on how to use the program:

User only needs to run the program and enter the time and day he/she will arrive at school. The system will generate a probability of he/she can successfully find a parking place near the school building.


## Sources Used:


