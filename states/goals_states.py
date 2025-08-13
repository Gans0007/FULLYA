from aiogram.fsm.state import StatesGroup, State

class GoalStates(StatesGroup):
    waiting_for_goal_text = State()

class PlanStates(StatesGroup):
    choosing_goal_link = State()
    waiting_for_plan_text = State()
    skipping_goal_link = State()
    editing_plan = State()  

class DreamStates(StatesGroup):
    waiting_for_dream_text = State()

class DreamPhotoFSM(StatesGroup):
    choosing_dream = State()
    uploading_photo = State()

class GoalEditState(StatesGroup):
    choosing_goal = State()
    waiting_for_new_text = State()



