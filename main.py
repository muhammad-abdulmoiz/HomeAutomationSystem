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
        for device_name, tasks in self.tasks.items():
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

        return builder.get_schedule()


class SmartHomeManager:
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
    manager = SmartHomeManager()
    manager.create_and_execute_schedules()
