'''
You can use the following libraries: numpy, pandas, and any Python standard libraries.
If you want to use any other third-party library, please contact the TA.

<<< Don't forget to input the arguments (k, T, N) of the optimization function (main.py) !! >>>
'''
import pandas as pd
import numpy as np 
from tqdm.auto import tqdm 
from multiprocessing import Pool, shared_memory


def calculate_distance(word, keyboard_layout):
    prev = ''
    for c in word:
        if prev == '':
            prev = c
            continue
        elif c.isalpha() == False:
            prev = ''
            continue
        elif prev.isalpha() == False and c.isalpha() == True:
            prev = c
            continue

        prev_pos = np.where(np.array(keyboard_layout) == prev.upper())
        cur_pos = np.where(np.array(keyboard_layout) == c.upper())
        distance = np.sqrt((prev_pos[0][0] - cur_pos[0][0]) ** 2 + (prev_pos[1][0] - cur_pos[1][0]) ** 2)
        prev = c
        yield distance

def calculate_time(word, keyboard_layout, a, b, prob:float):
    distance = list(calculate_distance(word, keyboard_layout))
    return np.sum([a + b * np.log2(1 + d) for d in distance])*prob


class KeyBoardLayout:
    def __init__(self, init_layout):
        self.layout = init_layout
    
    def simulate(self, key1, key2, word_df, a, b, k, T, prev_time):
        ''' Simulate the keyboard layout
        1. Swap the two keys
        2. Calculate the time
        3. Calculate the transition probability
        4. Accept the new layout with probability
        '''
        

        # return time


def swap(word_df, a, b, k, T, N, keyboard_shm_name, changes_in_t_shm_name, num_iter_shm_name):
    # retrieve shared memories
    keyboard = np.frombuffer(dtype=np.dtype('<U1'), buffer=shared_memory.SharedMemory(name=keyboard_shm_name).buf)
    changes_in_t = np.frombuffer(dtype=np.float64, buffer=shared_memory.SharedMemory(name=changes_in_t_shm_name).buf)
    num_iter = np.frombuffer(dtype=np.int64, buffer=shared_memory.SharedMemory(name=num_iter_shm_name).buf)

    # randomly select two keys
    key1 = np.random.choice(np.arange(30))
    key2 = np.random.choice(np.arange(30))

    prev_time = 0 if num_iter.item() == 0 else changes_in_t[num_iter.item()-1]
    layout = keyboard.copy()
    key1_y, key1_x = key1 // 6, key1 % 6
    key2_y, key2_x = key2 // 6, key2 % 6
    layout[key1_y][key1_x], layout[key2_y][key2_x] = layout[key2_y][key2_x], layout[key1_y][key1_x]
    # calculate the time
    time = 0
    for i, row in word_df.iterrows():   
        word = row['Word']
        prob = row['prob']
        time += calculate_time(word, layout, a, b, prob)
    
    # transition probability
    if (time - prev_time) <= 0:
        prob = 1.
    else:  
        prob = np.exp(-(time - prev_time) / (T*k))

    # accept the new layout with probability
    if prob > np.random.rand():
        # commit
        keyboard[:] = layout[:]

    changes_in_t[num_iter.item()] = time
    num_iter += 1



def optimization(a, b, k, T, N, keyboard_layout):
    '''
    Parameter
    1. a = 0.083 ( Touchscreen keyboarding - Fitts’ law parameter )
    2. b = 0.127 ( Touchscreen keyboarding - Fitts’ law parameter )
    3. k : k is a coefficient, input your value in main.py
    4. T : T is temperature, input your value in main.py
    5. N : Number of iteration, input your value in main.py
    6. keyboard_layout : Initial keyboard layout ( Python list )

    Return
    1. final_keyboard_layout : Optimized keyboard layout result (Python list format)
    2. t_value_sequence : Changes of the Fitts’ law movement time value recorded during the optimization process
        (Python list format)

    Result example
    1. Optimized keyboard layout result
        (1) '*' represents an empty key.
        (2) The keyboard layout list below is identical to Figure 1.

    Optimized_keyboard_layout_result_list = [
        ['Q', 'W', 'E', 'R', 'T', 'Y'],
        ['U', 'I', 'O', 'P', 'A', 'S'],
        ['D', 'F', 'G', 'H', 'J', 'K'],
        ['L', 'Z', 'X', 'C', 'V', 'B'],
        ['N', 'M', '*', '*', '*', '*']]

    2. Changes of the Fitts’ law movement time value recorded during the optimization process
        (1) The first element represents the Fitts’ Law value (t) of the initial keyboard layout.
        (2) The numbers are just examples.

    Changes_in_t = [3.312849, 2.980117, ..., 1.851442]

    Note
    1. You can use the "pandas" or "csv" library to read a CSV file.
    2. When reading CSV files, always use "relative path".
    3. Do not change the function name and structure.
    4. Your function should not read input from the user and print the results of your function.


    < Code explanation >





    '''
    # Read the word list
    word_df = pd.read_csv('scenario_1/dataset/word_frequency.csv', keep_default_na=False)
    word_df['prob'] = word_df['Frequency'] / word_df['Frequency'].sum()
    changes_in_t = np.zeros(N)
    shm = shared_memory.SharedMemory(create=True, size=changes_in_t.nbytes)
    shared_changes_in_t = np.frombuffer(shm.buf, dtype=changes_in_t.dtype, count=N)
    shared_changes_in_t[:] = changes_in_t[:]

    keyboard_layout = np.array(keyboard_layout)
    shm_key = shared_memory.SharedMemory(create=True, size=keyboard_layout.nbytes)
    shared_keyboard_layout = np.frombuffer(shm_key.buf, dtype=keyboard_layout.dtype, count=30).reshape((5,6))
    shared_keyboard_layout[:] = keyboard_layout[:]
    

    num_iter = np.array([0])
    shm_iter = shared_memory.SharedMemory(create=True, size=num_iter.nbytes)
    shared_num_iter = np.frombuffer(shm_iter.buf, dtype=num_iter.dtype, count=1)
    shared_num_iter[:] = num_iter[:]

    with Pool(4) as p:
        for _ in tqdm(range(N//4)):
            p.starmap(swap, [(word_df, a, b, k, T, N, shm_key.name, shm.name, shm_iter.name) for _ in range(4)])
    shm.close()
    return shared_keyboard_layout.tolist(), shared_changes_in_t
