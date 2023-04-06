class Vehicle():
    def __init__(self, spot_size):
        self._spot_size = spot_size

    def get_spot_size(self):
        return self._spot_size

class Driver():
    def __init__(self, id, vehicle):
        self._id = id
        self._vehicle = vehicle
        self._payment_due = 0
    
    def get_id(self):
        return self._id

    def get_vehicle(self):
        return self._vehicle
    
    def charge(self, amount):
        self._payment_due += amount

class Car(Vehicle):
    def __init__(self):
        super().__init__(1)

class Limo(Vehicle):
    def __init__(self):
        super().__init__(2)

class SemiTruck(Vehicle):
    def __init__(self):
        super().__init__(3)
        
class ParkingFloor():
    def __init__(self, spot_count):
        self._spots = [0] * spot_count
        self._vehicle_map = {}
    
    def park_vehicle(self, vehicle: Vehicle) -> bool:
        size = vehicle.get_spot_size()
        #using 2 pointer technique
        l, r = 0, 0 
        while r < len(self._spots):
            if self._spots[r]!=0:
                l = r + 1
            if r - l + 1 == size: # if there's a spot, Fill!
                for i in range(l, r+1):
                    self._spots[i] = 1
                self._vehicle_map[vehicle] = [l, r]
                return True
            r += 1
        return False
    
    def remove_vehicle(self, vehicle):
        l, r = self._vehicle_map[vehicle]
        for i in range(l,r+1):
            self._spots[i] = 0
        del self._vehicle_map[vehicle]
    
    def get_parking_spots(self):
        return self._spots

    def get_vehicle_spot(self, vehicle):
        return self._vehicle_map.get(vehicle)
    
class ParkingGarage():
    def __init__(self, floor_count, spots_per_floor):
        self._parking_floor = [ParkingFloor(spots_per_floor) for _ in range(floor_count)]

    def park_vehicle(self, vehicle):
        for floor in self._parking_floor:
            if floor.park_vehicle(vehicle):
                return True
        return False

    def remove_vehicle(self, vehicle):
        for floor in self._parking_floor:
            if floor.get_vehicle_spot(vehicle): #if the vehicle found
                floor.remove_vehicle(vehicle)
                return True
        return False
    
from datetime import datetime
import math

class ParkingSystem():
    def __init__(self, parkingGarage, hourlyRate):
        self._parkingGarage = parkingGarage
        self._hourlyRate = hourlyRate
        self._timeParked = {} # map driver ID to time

    def park_vehicle(self, driver):
        currentHour = datetime.now().hour
        isParked = self._parkingGarage.park_vehicle(driver.get_vehicle())
        if isParked:
            self._timeParked[driver.get_id()] = currentHour
        return isParked

    def remove_vehicle(self, driver):
        if driver.get_id() not in self._timeParked:
            return False
        currentHour = datetime.now().hour
        timeParked = math.ceil(currentHour - self._timeParked[driver.get_id()])
        driver.charge(timeParked * self._hourlyRate)

        del self._timeParked[driver.get_id()]
        return self._parkingGarage.remove_vehicle(driver.get_vehicle())

# Simulate!
parkingGarage = ParkingGarage(3, 2) #3 floor, 2 spots
parkingSystem = ParkingSystem(parkingGarage, 5)

driver1 = Driver(1, Car())
driver2 = Driver(2, Limo())
driver3 = Driver(3, SemiTruck())

print(parkingSystem.park_vehicle(driver1)) #True
print(parkingSystem.park_vehicle(driver2)) #True
print(parkingSystem.park_vehicle(driver3)) #False

print(parkingSystem.remove_vehicle(driver1)) #True
print(parkingSystem.remove_vehicle(driver2)) #True
print(parkingSystem.remove_vehicle(driver3)) #True
