from abc import ABC, abstractmethod


class DeviceController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DeviceController, cls).__new__(cls)
            cls._instance.device_registry = {}
        return cls._instance

    def add_device(self, device_name, device):
        self.device_registry[device_name] = device

    def get_device(self, device_name):
        return self.device_registry[device_name]

    def execute_device_operation(self, device_name, action):
        device = self.get_device(device_name)
        if device:
            return device.operate(action)
        return "Invalid: Device does not exist."


class SmartDeviceFactoryInterface(ABC):
    @abstractmethod
    def get_device(self, device_name):
        pass


class SmartDeviceFactory(SmartDeviceFactoryInterface):
    def get_device(self, device_name):
        try:
            if device_name == "light":
                return Light()
            elif device_name == "ceiling fan":
                return CeilingFan()
            elif device_name == "security camera":
                return SecurityCamera()
            elif device_name == "door lock":
                return DoorLock()
            elif device_name == "air conditioner":
                return AirConditioner()
            elif device_name == "thermostat":
                return ThermostatAdapter(SmartThermostat())
            elif device_name == "phanos":
                phanos = Phanos()
                phanos.add_light(NamedLight("blue"))
                phanos.add_light(NamedLight("red"))
                phanos.add_light(NamedLight("orange"))
                return phanos
            else:
                raise ValueError("Device name is not valid.")
        except ValueError as e:
            return f"Error: {e}"


class SmartDevice(ABC):
    @abstractmethod
    def operate(self, action):
        pass


class Light(SmartDevice):
    def operate(self, action):
        return f"Light is {action}."


class NamedLight(Light):
    def __init__(self, name):
        self.name = name

    def operate(self, action):
        # Call the superclass method and append the name
        return f"{self.name.capitalize()} {super().operate(action)}"


class CeilingFan(SmartDevice):
    def operate(self, action):
        return f"Ceiling fan is {action}."


class SecurityCamera(SmartDevice):
    def operate(self, action):
        return f"Security camera is now {action}."


class DoorLock(SmartDevice):
    def operate(self, action):
        return f"The door lock is {action}."


class AirConditioner(SmartDevice):
    def operate(self, action):
        return f"Air conditioner is {action}."


# Implementation of Adapter Structural Pattern
class ThermostatAdapter(SmartDevice):
    def __init__(self, thermostat):
        self.thermostat = thermostat

    def operate(self, action):
        words = action.split()
        temperature = " ".join(words[3:5])
        return self.thermostat.set_temperature(temperature)


class SmartThermostat:
    @staticmethod
    def set_temperature(temperature):
        return f"Thermostat temperature set to {temperature}."


class Phanos(SmartDevice):
    def __init__(self):
        self._lights = []

    def add_light(self, light):
        self._lights.append(light)

    def remove_light(self, light):
        self._lights.remove(light)

    def operate(self, action):
        results = []
        for light in self._lights:
            results.append(light.operate(action))
        results.append(f"Phanos with all lights {action}.")
        return results


class Task:
    def __init__(self, device_name: object, time: object, action: object) -> \
            object:
        self.device_name = device_name
        self.time = time
        self.action = action

    def __repr__(self):
        return (f"Task(device_name={self.device_name}, time={self.time}, "
                f"action={self.action})")


class Schedule:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def execute_tasks(self):
        for task in self.tasks:
            print(task)


class ScheduleBuilder:
    def __init__(self):
        self.schedule = Schedule()
        # Dictionary mapping device names to lists of tasks.
        self.tasks = {}

    def add_task_to_builder(self, task):
        if task.device_name not in self.tasks:
            self.tasks[task.device_name] = []
        self.tasks[task.device_name].append(
            f"At {task.time}, {task.action} {task.device_name}")

    def get_schedule(self):
        for tasks in self.tasks.values():
            for task in tasks:
                self.schedule.add_task(task)
        return self.schedule


class Director:
    @staticmethod
    def construct_morning_schedule():
        builder = ScheduleBuilder()

        builder.add_task_to_builder(
            Task("security_camera", "06:30", "start"))
        builder.add_task_to_builder(
            Task("ceiling_fan", "07:00", "turn off"))
        builder.add_task_to_builder(
            Task("bedroom_light", "07:00", "turn off"))
        builder.add_task_to_builder(
            Task("kitchen_light", "07:30", "turn on"))

        return builder.get_schedule()

    @staticmethod
    def construct_evening_schedule():
        builder = ScheduleBuilder()

        builder.add_task_to_builder(
            Task("security_camera", "18:00", "stop recording"))
        builder.add_task_to_builder(
            Task("bedroom_light", "18:30", "turn on"))
        builder.add_task_to_builder(
            Task("dining_room_light", "18:30", "turn on"))
        builder.add_task_to_builder(
            Task("kitchen_light", "19:00", "turn off"))
        builder.add_task_to_builder(
            Task("thermostat", "19:30", "set temperature to 22 C of"))

        return builder.get_schedule()

    @staticmethod
    def construct_night_schedule():
        builder = ScheduleBuilder()

        builder.add_task_to_builder(
            Task("door_lock", "21:00", "engage"))
        builder.add_task_to_builder(
            Task("bedroom_light", "21:30", "dim to 50%"))
        builder.add_task_to_builder(
            Task("air_conditioner", "21:30", "turn on"))
        builder.add_task_to_builder(Task("phanos", "22:00", "turn on"))

        return builder.get_schedule()


class SmartHomeManagerFacade:
    def __init__(self):
        self.controller = DeviceController()
        self.device_factory = SmartDeviceFactory()

        # Adding smart devices to the controller during initialization
        self._setup_devices()

    def _setup_devices(self):
        # Add smart devices to the controller using the factory
        self.controller.add_device("security_camera",
                                   self.device_factory.get_device("security "
                                                                  "camera"))
        self.controller.add_device("ceiling_fan",
                                   self.device_factory.get_device("ceiling "
                                                                  "fan"))
        self.controller.add_device("bedroom_light",
                                   self.device_factory.get_device("light"))
        self.controller.add_device("kitchen_light",
                                   self.device_factory.get_device("light"))
        self.controller.add_device("dining_room_light",
                                   self.device_factory.get_device("light"))
        self.controller.add_device("door_lock",
                                   self.device_factory.get_device("door lock"))
        self.controller.add_device("air_conditioner",
                                   self.device_factory.get_device(
                                       "air conditioner"))
        self.controller.add_device("thermostat",
                                   self.device_factory.get_device(
                                       "thermostat"))
        self.controller.add_device("phanos", self.device_factory.get_device(
            "phanos"))

    def create_and_execute_schedules(self):
        morning_schedule = Director.construct_morning_schedule()
        evening_schedule = Director.construct_evening_schedule()
        night_schedule = Director.construct_night_schedule()

        print("\n--- Morning Schedule ---")
        morning_schedule.execute_tasks()
        self._execute_schedule_tasks(morning_schedule)

        print("\n--- Evening Schedule ---")
        evening_schedule.execute_tasks()
        self._execute_schedule_tasks(evening_schedule)

        print("\n--- Night Schedule ---")
        night_schedule.execute_tasks()
        self._execute_schedule_tasks(night_schedule)

    def _execute_schedule_tasks(self, schedule):
        print("\n--- Executing Scheduled Tasks ---")
        for task in schedule.tasks:
            device_name = task.split()[-1]
            action = self.extract_action(task)
            print(self.controller.execute_device_operation(device_name,
                                                           action))
        print("--- Execution Complete ---")

    @staticmethod
    def extract_action(sentence):
        # Task format i.e. At 21:30, turn on air_conditioner
        parts = sentence.split(", ")

        # Split the second part (action and device name) by spaces
        action_parts = parts[1].split()

        # Join all parts except the last one (which is the device name)
        action = " ".join(action_parts[:-1])

        return action


if __name__ == "__main__":
    manager = SmartHomeManagerFacade()
    manager.create_and_execute_schedules()
