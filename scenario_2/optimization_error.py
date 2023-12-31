'''
You can use the following libraries: numpy, pandas, and any Python standard libraries.
If you want to use any other third-party library, please contact the TA.

<<< Don't forget to input the arguments (k, T, N) of the optimization function (main.py) !! >>>
'''
import pandas as pd
import numpy as np 
from tqdm.auto import tqdm 


ERROR_PROB = 4/100


def calculate_distance(word, keyboard_layout):
    prev = ''
    for c in word:
        if prev == '':
            prev = c
            continue
        elif c == ' ':
            c = 'Space'

        if len(c) == 1:
            c = c.upper()
        if (len(prev) == 1):
            prev = prev.upper()
            
        prev_pos = np.where(np.array(keyboard_layout) == prev)
        cur_pos = np.where(np.array(keyboard_layout) == c)
        distance = np.sqrt((prev_pos[0][0] - cur_pos[0][0]) ** 2 + (prev_pos[1][0] - cur_pos[1][0]) ** 2)
        prev = c

        # Fat finger error
        if np.random.rand() < ERROR_PROB:
            c = 'Backspace' 
            prev_pos = np.where(np.array(keyboard_layout) == prev)
            cur_pos = np.where(np.array(keyboard_layout) == c)
            distance = np.sqrt((prev_pos[0][0] - cur_pos[0][0]) ** 2 + (prev_pos[1][0] - cur_pos[1][0]) ** 2)
            yield distance*2

        yield distance


def calculate_time(word, keyboard_layout, a, b):
    ''' Calculate the time to type a word
        Here, word is a large text chunk (e.g., a full paragraph)
    '''
    distance = list(calculate_distance(word, keyboard_layout))
    return np.sum([a + b * np.log2(1 + d) for d in distance])


class KeyBoardLayout:
    def __init__(self, init_layout):
        self.layout = init_layout
        self.commit_cnt = 0
    
    def simulate(self, text_chunk, a, b, k, T, prev_time):
        ''' Simulate the keyboard layout
        1. Swap the two keys
        2. Calculate the time
        3. Calculate the transition probability
        4. Accept the new layout with probability
        ''' 
        layout = self.layout.copy()

        if prev_time > 0:
            # randomly select two keys
            key1 = np.random.choice(np.arange(30))
            key2 = np.random.choice(np.arange(30))

            key1_y, key1_x = key1 // 6, key1 % 6
            key2_y, key2_x = key2 // 6, key2 % 6
            layout[key1_y][key1_x], layout[key2_y][key2_x] = layout[key2_y][key2_x], layout[key1_y][key1_x]
        # calculate the time
        time = calculate_time(text_chunk, layout, a, b)
        
        # transition probability
        if (time - prev_time) <= 0:
            prob = 1.
        else:  
            prob = np.exp(-(time - prev_time) / (T*k))
        
        # accept the new layout with probability
        if prob > np.random.rand():
            # commit
            self.layout[:] = layout[:]
            self.commit_cnt += 1
            prev_time = time

        elif prev_time == 0:
            prev_time = time

        return prev_time, time

 
def optimization(a,b,k,T,N,keyboard_layout):
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
        (1) The keyboard layout list below is identical to Figure 2.

    Optimized_keyboard_layout_result_list = [
        ['Q', 'W', 'E', 'R', 'T', 'Y'],
        ['U', 'I', 'O', 'P', 'A', 'S'],
        ['D', 'F', 'G', 'H', 'J', 'K'],
        ['L', 'Z', 'X', 'C', 'V', 'B'],
        ['N', 'M', 'Space', 'Backspace', '-', ',']]

    2. Changes of the Fitts’ law movement time value recorded during the optimization process
        (1) The first element represents the Fitts’ Law value (t) of the initial keyboard layout.
        (2) The numbers are just examples.

    Changes_in_t = [3.312849, 2.980117, ..., 1.851442]

    Note
    1. When reading .txt files, always use "relative path".
    2. Do not change the function name and structure.
    3. Your function should not read input from the user and print the results of your function.


    < Code explanation >





    '''
    with open("scenario_2/dataset/writing.txt", 'r') as f:
        word_list = f.readlines()
    text_chunk = ''.join(word_list).replace("\n", "")
    # Initialize the keyboard layout
    keyboard_layout = KeyBoardLayout(keyboard_layout)
    prev_time = 0
    t_value_sequence = []
    for _ in tqdm(range(N)):
        k *= 0.99
        prev_time, time = keyboard_layout.simulate(text_chunk, a, b, k, T, prev_time)
        t_value_sequence.append(round(time, 6))
    return keyboard_layout.layout, t_value_sequence
