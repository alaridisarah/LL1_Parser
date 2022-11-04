import re
import sys
import tkinter as tk
from tkinter import *
from prettytable import PrettyTable
import Stack as st



def input_string_printer(input_list, input_pointer):
    str = ''
    for i in input_list[input_pointer:]:
        str = str + i + " "
    return str

def first_fn(production, terminal):
    ans = dict()
    for var in production:
        ans[var] = set()     # Initialize first of each var to an empty SET
    change = 1
    while change:
        change = 0
        for var in production:
            tmp_set = ans[var]
            for p in production[var]:
                length = len(p)
                char = ''
                for i in range(length):
                    char_ = p[i]
                    # to find appr. terminal like in int
                    char = char + p[i]
                    # print(char)
                    if (char_.isupper()):
                        char = ''
                        # char_ is a variable
                        tmp_set = tmp_set.union(ans[char_])
                        # if variable is having null in its first
                        if ('^' in ans[char_]) and (i != length-1):
                            tmp_set = tmp_set - {'@'}
                        else:
                            break
                    else:
                        if (char in terminal):
                            set_terminal = set([char])  # tmp set for terminal
                            tmp_set = tmp_set.union(set_terminal)
                            break

            if tmp_set != ans[var]:
                ans[var] = tmp_set
                change = 1
    return ans


def first_of_alpha(alpha, terminal, first_of_variables):
    ans = set()
    char = ''
    for i in range(len(alpha)):
        char_ = alpha[i]
        char = char + alpha[i]
        if (char_.isupper()):
            char = ''
            ans = ans.union(first_of_variables[char_])
            if ('@' in first_of_variables[char_]) and (i != len(alpha)-1):
                ans = ans - {'@'}
            else:
                break
        else:
            if char in terminal:
                set_terminal = set([char])
                ans = ans.union(set_terminal)
                break
    return ans


def follow_fn(production, terminal, start_symbol, first_of_variables):
    ans = dict()
    for var in production:
        ans[var] = set()
    # ans[start_symbol] = {'$'}
    change = 1
    while change:
        change = 0
        for var in production:
            tmp_set = ans[var]
            if (var == start_symbol):
                tmp_set = tmp_set.union({'$'})
            for lhs in production:
                for p in production[lhs]:
                    if p.find(var) < 0:
                        continue
                    elif p.find(var) < len(p)-1:
                        alpha = p[p.find(var)+1]
                        # print(var + " " + alpha)
                        if '@' not in first_of_alpha(alpha, terminal, first_of_variables):
                            tmp_set = tmp_set.union(first_of_alpha(
                                alpha, terminal, first_of_variables))
                        else:
                            tmp_set = tmp_set.union(first_of_alpha(
                                alpha, terminal, first_of_variables))
                            tmp_set = tmp_set - {'@'}
                            tmp_set = tmp_set.union(ans[lhs])
                    else:
                        tmp_set = tmp_set.union(ans[lhs])
            if tmp_set != ans[var]:
                ans[var] = tmp_set
                change = 1
    return ans


def parsing_table(production, terminal, first_of_variables, follow_of_variables):
    ans = dict()
    x = set(terminal) - {'@'}    # Terminals union '$'
    x = x.union('$')
    for var in production:
        ans[var] = dict()
        for t in x:
            ans[var][t] = 'Null'  # Denoting empty places by 'Null'
    flag = 0
    for var in production:
        for rhs in production[var]:
            tmp_set = first_of_alpha(rhs, terminal, first_of_variables)
            for each in tmp_set:
                if each == '@':
                    tmp_set_2 = follow_of_variables[var]
                    for some in tmp_set_2:
                        if (ans[var][some] != 'Null'):
                            flag = 1
                            break
                        else:
                            ans[var][some] = rhs
                else:
                    if (ans[var][each] != 'Null'):
                        flag = 1
                        break
                    else:
                        ans[var][each] = rhs
            if flag:
                break
        if flag:
            break
    if flag:
        print("\nGiven grammar is not LL(1)")
        sys.exit()
    return ans

def Ptable():
    table = parsing_table(production, terminal,
                          first_of_variables, follow_of_variables)
    print('\nParsing Table')
    ########### TABLE FORMATTING #############
    tmp_table = table
    x = terminal
    if '@' in x:
        x.remove('@')
    x.append('$')
    x.sort()
    l1 = ['Var/Term']
    x = ['Var/Term'] + x
    obj = PrettyTable(x)
    for var in tmp_table:
        tmp_list = list(var)
        ddd = tmp_table[var]
        for key in sorted(ddd):
            tmp_list.append(ddd[key])
        obj.add_row(tmp_list)

    print(obj)
    return obj, table


def Checking():
    input_string = inputstring.get().rstrip()
    input_list = []
    print(inputstring.get())
    tmp_input_string = ''
    # print(terminal)
    for i in input_string:
        if i != ' ':
            tmp_input_string = tmp_input_string + i
        # print(tmp_input_string)
        if tmp_input_string in terminal:
            input_list.append(tmp_input_string)
            tmp_input_string = ''
    input_list.append('$')
    print()
    ################# STACK #####################
    valid = 1
    input_pointer = 0
    stack = st.Stack()
    stack.push('$')
    stack.push(start_symbol)
    print(stack.print_bottom_up() + "		" +
          input_string_printer(input_list, input_pointer))

    while stack.top() != '$':
        top_sym = stack.top()
        next_input = input_list[input_pointer]
        if top_sym.isupper():
            if table[top_sym][next_input] == 'Null':
                valid = 0
                print('1')
                break
            else:
                tmp_list_2 = []
                char = ''
                length = len(table[top_sym][next_input])
                for i in range(length):
                    char_ = table[top_sym][next_input][i]
                    char = char + table[top_sym][next_input][i]
                    if (char_.isupper()):
                        char = ''
                        tmp_list_2.append(char_)
                    else:
                        if char in terminal:
                            tmp_list_2.append(char)
                            char = ''
                stack.pop()
                tmp_list_2.reverse()
                for i in tmp_list_2:
                    stack.push(i)
                print(stack.print_bottom_up() + "		" +
                      input_string_printer(input_list, input_pointer))
        else:
            if top_sym == input_list[input_pointer]:
                stack.pop()
                input_pointer = input_pointer + 1
                print(stack.print_bottom_up() + "		" +
                      input_string_printer(input_list, input_pointer))
            else:
                valid = 0
                break

    if valid == 1:
        res = tk.Label(frame, text="String ( "+input_string+")"+" is ACCEPTED!!!!", justify=CENTER,
                       fg="green", font=("calibri", 9))
        res.pack()
    else:
        res = tk.Label(frame, text="String ( "+input_string+" )"+" Oh no, is REJECTED", justify=CENTER,
                       fg="red", font=("calibri", 9))
        res.pack()


def main_screen():
    def stop():
        frame.destroy()
    # global Boxtext
    global inputstring
    global table
    global frame
    
    frame = Tk()
    frame.title("LL1 PARSER")
    frame.geometry('800x800')

    Production_final = """        PROGRAM → STMTS
	STMTS → STMT STMTS’
	STMTS’ → ϵ | ; STMTS
	STMT → id = EXPR
	EXPR → EXPR’ TERM
	EXPR’ → + TERM EXPR’ | - TERM EXPR’ | ϵ
	TERM → EXPO TERM’
	TERM’ → * EXPO TERM’ | / EXPO TERM’ | ϵ
	EXPO → FACTOR EXPO’
	EXPO’ → ^ EXPO| ϵ
	FACTOR → ( EXPR ) | id | integer | n FACTOR | p FACTOR"""

    # Grammar
    Label(text="").pack()
    Label(text="").pack()
    tk.Label(frame, text="LL1 grammar : ", font=(
        "calibri", 12), justify=LEFT).pack()
    tk.Label(text=Production_final, font=("Courier", 9), justify=LEFT).pack()
    tk.Label(frame, text="").pack()
    Note = "*NOTE*: n and p unary sign operators - and +. @ is ϵ in parsing table."
    tk.Label(text=Note, justify=CENTER, fg="red", font=("calibri", 9)).pack()

    # parsing table
    tk.Label(frame, text="").pack()
    tk.Label(frame, text="Parsing table : ", font=("calibri", 12)).pack()
    obj, table = Ptable()
    tk.Label(text=obj, font=("Courier", 9), justify=CENTER).pack()

    # checking
    tk.Label(frame, text="Check whether the string is accepted or rejected by the grammar", font=(
        "calibri", 12)).pack()

    tk.Label(frame, text="").pack()

    inputstring = tk.StringVar()
    Boxtext = Entry(frame, textvariable=inputstring)
    Boxtext.pack()
    tk.Label(frame, text="").pack()

    save = tk.Button(frame, text="check",height=1,width=5, command=Checking)
    save.pack()
    stopp = tk.Button(frame, text="stop",height=1,width=5, command=stop)
    stopp.pack()

    frame.mainloop()





####################################################################
#################### PROGRAM START FROM HERE #######################
# Productions for each variable as a dictionary with key as variable
production = dict()
fhandle = open("grammar6.txt", "r")   # file containing production rules
flag = 1
for line in fhandle:
    line = line.rstrip()
    tmp_list = re.split(" -> | \| ", line)
    lhs = str(tmp_list[0])
    rhs = tmp_list[1:]
    if flag:
        start_symbol = lhs
        flag = 0
    production[lhs] = rhs
# file containing terminal symbols
terminal_file = open('terminal6.txt', 'r')
terminal = []                                     # list of terminal symbols
for each in terminal_file:
    each = each.rstrip()
    terminal.append(each)

print('\nTerminal Symbols =', terminal)
# print(production)
first_of_variables = first_fn(production, terminal)
follow_of_variables = follow_fn(
    production, terminal, start_symbol, first_of_variables)
print('\nFirst of Variables : ')
for var in first_of_variables:
    print(var, '-', first_of_variables[var])
print('\nFollow of Variables : ')
for var in follow_of_variables:
    print(var, '-', follow_of_variables[var])
main_screen()
