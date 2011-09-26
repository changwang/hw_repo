import random
import time

class Slot(object):
  """ slot class reprents a slot in the environment """

  # what's the shape of slot, could be rectangle, triangle, circle
  RECTANGLE = 1

  # what's the state of slot, could be clean, dirty
  CLEAN = 1
  DIRTY = 0

  def __init__(self, shape, state):
    self.shape = shape
    self.state = state
    self.location = -1

  def get_shape(self):
    return self.shape

  def set_shape(self, shape):
    self.shape = shape

  def get_state(self):
    return self.state

  def set_state(self, state):
    self.state = state

  def get_location(self):
    return self.location

  def set_location(self, location):
    self.location = location

class Environment(object):
  """
  environment represents the whole world,
  it contains slots, tells agents its state.
  """

  def __init__(self):
    self.slots = []

  def add_slot(self, slot):
    """ adds a new slot into slots """
    slot.set_location(len(self.slots)+1)
    self.slots.append(slot)

  def remove_slot(self, slot):
    """ removes a slot out of slots """
    if slot in self.slots:
      idx = self.slots.index(slot)
      # update location of rest slot
      for s in self.slots[idx:]:
        s.set_location(s.get_location()-1)
      self.slots.remove(slot)

  def get_slot(self, idx):
    """ returns the slot at index idx """
    assert (idx >= 0) and (idx < self.size()), "Index is out of range"
    return self.slots[idx]

  def update(self):
    """ randomly update a slot's state in the environment """
    if self.size() < 2: return
    idx = random.randint(0, 100) % 3
    if idx < 2:
      slot = self.slots[idx]
      if slot.get_state() == Slot.CLEAN:
        slot.set_state(Slot.DIRTY)
        # self.slots[idx] = slot

  def size(self):
    """ get the current size of slots in the environment """
    return len(self.slots)

class Sensor(object):
  """ sensor is an abstract class, which is used to perceive the environment """
  def __init__(self, name):
    self.name = name
    self.percept = -1 # holds last received percept

  def perceive(self, slot):
    raise NotImplementedError("Subclass must implement this method")

  def last_percept(self):
    """ returns the latest percept """
    return self.percept

class LocationSensor(Sensor):
  """ location sensor can tell the agent's location in current environment """
  def __init__(self, name="LocationSensor"):
    self.name = name
    self.percept = -1

  def perceive(self, slot):
    """ finds the location """
    # right now, let's just observe the first element in the world
    if isinstance(slot, Slot):
      self.percept = slot.get_location()
    else:
      raise RuntimeError("Cannot observe other objects right now!")

class DirtSensor(Sensor):
  """ dirt sensor can tell the agent, whether the slot is clean or dirty """
  def __init__(self, name="DirtSensor"):
    self.name = name
    self.percept = -1

  def perceive(self, slot):
    """ finds the state of slot """
    # right now, let's just observe the first element in the world
    if isinstance(slot, Slot):
      self.percept = slot.get_state()
    else:
      raise RuntimeError("Cannot observe other objects right now!")

class Actuator(object):
  """ actuator will act based on the percept has been received so far """
  def __init__(self, name="Actuator"):
    self.name = name

  def act(self, world, agent, **kwargs):
    """
    act based on the received percept and rules,
    kwargs should have two parts: percept and rules.
    and we know here only two percepts each time:
    first one is the location,
    second one is the state of slot
    """
    if kwargs == None or len(kwargs) == 0: return
    percept = kwargs["percept"] if kwargs["percept"] else None
    rules = kwargs["rules"] if kwargs["rules"] else None
    mask = percept[-1] << agent.get_location()
    if mask in rules:
      if mask == VacuumAgent.RIGHT:
        agent.set_location(agent.get_location()+1)
        agent.last_action = VacuumAgent.RIGHT
      elif mask == VacuumAgent.LEFT:
        agent.set_location(agent.get_location()-1)
        agent.last_action = VacuumAgent.LEFT
      else:
        world.get_slot(agent.get_location()-1).set_state(Slot.CLEAN)
        agent.last_action = VacuumAgent.SUCK
        agent.increase_score()

class VacuumAgent(object):
  """
  vacuum agent represents the vacuum machine,
  which observes the environment, then acts based on the observation.
  """

  # rules
  RIGHT = 1 << 1 # A & CLEAN
  LEFT  = 1 << 2 # B & CLEAN
  SUCK  = 0      # A & DIRTY OR B & DIRTY

  def __init__(self, location, sensors, actuator):
    self.sensors = sensors
    self.actuator = actuator
    self.location = 1 # initial location in the world
    self.last_action = -1
    self.score = 0

  def start(self, world):
    """ starts sensing the world """
    self.sense(world)

  def sense(self, world):
    """ senses the world """
    for sen in self.sensors:
      sen.perceive(world.get_slot(self.location-1))
    self.actuator.act(world, self, percept=[sen.last_percept() for sen in self.sensors],
        rules=(VacuumAgent.RIGHT, VacuumAgent.LEFT, VacuumAgent.SUCK))

  def get_location(self):
    """ returns the location of the agent in current world """
    return self.location

  def set_location(self, location):
    """ moves the location of the agent in current world """
    self.location = location
    
  def get_score(self):
    """ returns the score of agent """
    return self.score
    
  def increase_score(self):
    """ increases the score by 1 each time the agent sucks dirt """
    self.score += 1
        
  def last_move(self):
    """ returns agent's last action """
    return self.last_action
    
  def set_last_move(self, action):
    """ set the last movement """
    self.last_action = action

def action2string(agent):
  if agent.last_move() == VacuumAgent.RIGHT:
    return "Move to Right"
  elif agent.last_move() == VacuumAgent.LEFT:
    return "Move to Left"
  elif agent.last_move() == VacuumAgent.SUCK and agent.get_location() == 1:
    return "Suck Dirty in Slot A"
  elif agent.last_move() == VacuumAgent.SUCK and agent.get_location() == 2:
    return "Suck Dirty in Slot B"
  else:
    return ""

def print_world(world, agent, action):
  """ print the environment """
  s1 = "CLEAN" if world.get_slot(0).get_state() == Slot.CLEAN else "DIRTY"
  s2 = "CLEAN" if world.get_slot(1).get_state() == Slot.CLEAN else "DIRTY"

  s3 = "Agent" if agent.get_location() == 1 else ""
  s4 = "Agent" if agent.get_location() == 2 else ""
  
  dirt1 = "....." if world.get_slot(0).get_state() == Slot.DIRTY else ""
  dirt2 = "....." if world.get_slot(1).get_state() == Slot.DIRTY else ""
  
  ac = action2string(agent) if action else "before agent's action"

  str = """
            Environment
         A              B
  ===============================
  |\t%s\t|\t%s\t|
  |\t%s\t|\t%s\t| \t%s
  |\t%s\t|\t%s\t|
  ===============================
  """ % (s1, s2, dirt1, dirt2, ac, s3, s4)
  print str

if __name__ == '__main__':

  slot1 = Slot(Slot.RECTANGLE, Slot.DIRTY)
  slot2 = Slot(Slot.RECTANGLE, Slot.DIRTY)

  world = Environment()
  world.add_slot(slot1)
  world.add_slot(slot2)

  loc_sensor = LocationSensor()
  dit_sensor = DirtSensor()

  actuator = Actuator()

  va = VacuumAgent(1, [dit_sensor], actuator)
  va.start(world)

  for i in range(5):
    world.update()
    print_world(world, va, False)
    time.sleep(1)
    va.sense(world)
    print_world(world, va, True)

  print "Score is: %d" % va.get_score()