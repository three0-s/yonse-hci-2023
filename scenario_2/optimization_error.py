'''
You can use the following libraries: numpy, pandas, and any Python standard libraries.
If you want to use any other third-party library, please contact the TA.

<<< Don't forget to input the arguments (k, T, N) of the optimization function (main.py) !! >>>
'''

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

    return final_keyboard_layout, t_value_sequence
