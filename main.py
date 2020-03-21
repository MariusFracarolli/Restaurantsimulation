"""
gsettings set org.gnome.desktop.peripherals.keyboard repeat true
watch -n 1 cnee --replay -sp 125 -f xnee.xns
cnee --record --stop-key q --mouse --keyboard -o xnee.xns

Check if first_guess is false, e.g. write in event to a extra file with only one word
If first_guess and optimisation_part2.py is called, then
 pause till next input.

Anylogic + Python
1) Change first_guess to True in optimisation.py (also for first_guess) (Look where this information is saved in .alp)
    Not possible, but check is possible
3) Don't smooth highest value
4) Implement stopping criteria.
5) Do final optimisation
6) Give back not sys.exit() but repeat error (ask for input?)
7) What if no result, eg no queue or exp_result?
"""

import sys
import time
import os 

import opt

#start and clean
print("What to do?")
input_msg = input()
print(input_msg)
if 'clean' in input_msg.lower(): clean = True
else: clean = False


if 'first' in input_msg.lower(): fg = True
else: fg = False



if clean == True:
    opt.cleaner()
    print("Run experiment, press any button")
    print("Set first_guess to True")
    input()
    opt.opt_fg()
    print("Optimisation has run.")
else:
    if fg == True:
        print("Set first_guess to True")
        input()
        opt.opt_fg()
        print("Optimisation has run.")

print("Run experiment, press any button")
print("Set first_guess to False")
input()

for i in range(50):
    os.system('cnee --replay -sp 15 -f xnee.xns >/dev/null 2>&1')
    time.sleep(10)
    opt.opt()

print("Replication is finished.")

sys.exit()
clean = False
fi_gu = False 
while clean == False:
    print("Do you want to start a new experiment?")
    print("Old data will be moved and you have to restart.")
    print("Confirm with yes.")
    aux = input()
    aux = aux.lower()
    if (aux in ['no','nein','n'] or aux[0] in ['n','m']):
        print("You don't want to restart.")
        clean = True
        fi_gu = True
    if (aux in ['yes','ja','ok'] or aux[0] in ['y','j']):
         clean = True
         print('  Then we clean.')
         exec(open("cleaner.py").read())
         

#Prepare Anylogic, do first_guess simulation and start python script
while fi_gu == False:
    print("First start the current model in Anylogic.")
    print("Set first_guess to true and start the Simulation.")
    print("You find first guess on the top left as parameter. Click on it.")
    print("If you are done, confirm with yes.")
    aux = input()
    if (aux.lower() in ['yes','ja','ok'] or aux[0] in ['y','j']):
        fi_gu = True
        exec(open("optimisation.py").read())


#optimisation_part2()
while fi_gu == True:
    print("Change first_guess to false and start the Replication.")
    print("To start the replication, you have to choose it.")
    print("If you are done, confirm with any key.")
    aux = input() + '.'
    if (aux.lower() in ['yes','ja','ok'] or aux[0] in ['y','j']):
        fi_gu = False
time.sleep(2)
exec(open("optimisation_part2.py").read())

#start iteration
print("Is a macro installed to start the replication?")
print("yes: record new macro; no continue:")
aux = input()
if aux == 'yes':
    print("In three seconds the makro xnee.xns will be recorded.")
    print("Stop with the key q (Only record starting replication)")
    time.sleep(3)
    os.system('cnee --record --stop-key q --mouse --keyboard -o xnee.xns')
else: print('You use the old makro.')
#os.system('cnee --replay -sp 15 -f xnee.xns >/dev/null 2>&1')


i = 1
while i < 50:
    os.system('cnee --replay -sp 15 -f xnee.xns >/dev/null 2>&1')
    time.sleep(12)
    exec(open("optimisation_part2.py").read())

print("Replication is finished.")