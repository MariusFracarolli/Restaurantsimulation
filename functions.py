from matplotlib import pyplot as plt
import numpy  as np
import pandas as pd
import os
import sys
import glob

from pandas import DataFrame
import time

def print_pic_1_2(one_queue, shift_queue, queue_txt, it_n, ts, log):
    print(one_queue[1][1])
    max_queue = one_queue[1:4][:].max()
    if max_queue > 90: max_dia = int(max_queue*1.05)
    elif max_queue > 70: max_dia = 90
    elif max_queue > 40: max_dia =70
    else: max_dia = 40
    runtimes = int(len(queue_txt)/1441);
    print('You did ' + str(runtimes) + ' replications.')
    plt.step(one_queue[0][:],one_queue[1][:], label = 'Service')
    plt.step(one_queue[0][:],one_queue[2][:], label = 'Receive')
    plt.step(one_queue[0][:],one_queue[3][:], label = 'Produce')
    plt.title('Queueing lengths per time')
    plt.xlabel('minutes (Model Time)')
    plt.ylabel('Number of waiting elements')
    plt.legend(loc = 'best')
    axes = plt.gca()
    axes.set_xlim([0,990])
    axes.set_ylim([0,max_dia])

    plt.savefig(ts + '_1_queue_Iteration_'+ str(it_n)+'.png', dpi = 300)
    plt.savefig('1_'+ts + 'queue_Iteration_'+ str(it_n)+'.png', dpi = 300)
    plt.close()
    log.write('A graph about the queue length has been created. It can be found in the folder as .png.\n')

    #service, receive, kitchen - picture 2
    plt.step(shift_queue[0][:],shift_queue[1][:], label = 'Service')
    plt.step(shift_queue[0][:],shift_queue[2][:], label = 'Receive')
    plt.step(shift_queue[0][:],shift_queue[3][:], label = 'Produce')
    plt.title('Queueing lengths per shift')
    plt.xlabel('minutes (Model Time)')
    plt.ylabel('Number of waiting elements')
    plt.legend(loc = 'best')
    axes = plt.gca()
    axes.set_xlim([0,990])
    axes.set_ylim([0,max_dia])

    plt.savefig(ts + '_2_shift_queue_Iteration_'+ str(it_n)+'.png', dpi = 300)
    plt.savefig('2_'+ ts + '_shift_queue_Iteration_'+ str(it_n)+'.png', dpi = 300)
    plt.close()
    log.write('The average queue length per shift has been calculated and an image was created.\n')
    
    return max_dia

def obj_fulfill(mean_res, log):
    if  (mean_res[2] > 0.9 and mean_res[3] > 0.95 and
        mean_res[8] > 0.8 and mean_res[9] > 0.9):
        obj_fulfilled = True
        print('The objectives are fulfilled!')
        log.write('The objectives are fulfilled!\n')
        log.write(" 5min service queue: %5.3f%%, 8min: %5.3f%%.\n" %
            (mean_res[2]*100, mean_res[3]*100))
        log.write(" 5min food queue: %5.3f%%, 8min: %5.3f%%.\n" %
            (mean_res[8]*100, mean_res[9]*100))
    else:
        obj_fulfilled = False
        log.write('The objectives are not fulfilled!\n')
        log.write(' Objectives 5 min order: 0.9, 8 min order 0.95\n')
        log.write(' Objectives 5 min receive: 0.8, 8 min receive 0.9\n')
        log.write(' Real values:  %1.3f, %1.3f, %1.3f, %1.3f.\n' %
                (mean_res[2], mean_res[3], mean_res[8], mean_res[9]))

def ut_rates(mean_res, log):
    print(" The utility of waiter was %5.3f%% and of cooks %5.3f%%." %
            (mean_res[24]*100, mean_res[25]*100 ))
    print(" 5min service queue: %5.3f%%, 8min: %5.3f%%" %
            (mean_res[2]*100, mean_res[3]*100))
    print(" 5min food queue: %5.3f%%, 8min: %5.3f%%" %
            (mean_res[8]*100, mean_res[9]*100))

    log.write("The utility of waiter was %5.3f%% and of cooks %5.3f%%.\n" %
            (mean_res[24]*100, mean_res[25]*100 ))

def analyse(exp_txt, log):
    #[0]queueingLess1Min 2Min 5Min 8Min 10Min 15Min    6x
    #[6]+ kitchenLess1Min 2Min 5Min 8Min 10Min 15Min   6x
    #[12]+ foodLess2Min 5Min 8Min 10Min 15Min 20Min     6x
    #[18]+ receiveLess2Min 5Min 8Min 10Min 15Min 20Min  6x
    #[24]+ Waiter.utilization() Cook.utilization()      2x
    mean_res = np.average(exp_txt, axis = 0)
    std_res  = np.std(exp_txt, axis = 0)
    results_txt = open('mean_results.txt','a')
    results_txt.write((''.join(['%10.6f ']*mean_res.size)+'\n') % tuple(mean_res))
    results_txt.close()
    results_txt = open('stdev_results.txt','a')
    results_txt.write((''.join(['%10.6f ']*std_res.size)+'\n') % tuple(std_res))
    results_txt.close()
    log.write('It''s been written to mean_results.txt and stdev_results.txt.\n')
    log.write('mean_results.txt:\n')
    log.write((''.join(['%10.6f ']*mean_res.size)+'\n') % tuple(mean_res))
    log.write((''.join(['%10.6f ']*std_res.size)+'\n') % tuple(std_res))

    aux = pd.read_csv('waiter.txt', sep = ' ', header=None)
    waiter_txt = aux[-5:][:]    #last five rows
    waiter_mean = np.average(waiter_txt,axis =0)
    waiter_std =  np.std(waiter_txt,axis = 0)
    aux = pd.read_csv('cook.txt', sep = ' ', header=None)
    cook_txt = aux[-5:][:]    #last five rows
    cook_mean = np.average(cook_txt,axis =0)
    cook_std =  np.std(cook_txt,axis = 0)
    log.write('It''s been successfully read waiter.txt and cook.txt.\n')
    log.write('waiter_mean, waiter_std, cook_mean and cook_std are: \n')
    log.write( ' '.join(map(str,waiter_mean.astype(int))))
    log.write('\n')
    log.write( ' '.join(map(str,cook_mean.astype(int))))
    log.write('\n')
    return mean_res, std_res

def queue_txt_usable(log):
    if not os.path.isfile('queue.txt'):
        print('Do experiment first!')
        print('queue.txt has not been found.')
        time.sleep(10)
    queue_txt = pd.read_csv('queue.txt', sep = ' ', header=None)
    if len(queue_txt) % 1441 != 0 :
        print('Set first guess to true and try again!')
        log.write('Set first guess to true and try again!')
        print(len(queue_txt) % 1441)
        print('queue.txt has not the right length.')
        time.sleep(10)
    if os.path.isfile('first_guess.txt'):
        os.remove('first_guess.txt')
        log.write('first_guess.txt has been removed.\n')

    log.write('queue.txt has been loaded and is sufficient.')
    return queue_txt

def setup(first_guess_bool = False):
    log = open("logfile.txt","a")
    
    ts = time.gmtime()
    ts = time.strftime("%y%m%d_%H%M%S",ts)
    if first_guess_bool == True:
        if not os.path.isfile('queue.txt'):
            print('Do experiment first!')
            print('queue.txt does not exist.')
            time.sleep(10)                                                                              #Check and delete
        queue_txt = pd.read_csv('queue.txt', sep = ' ', header=None)
        if len(queue_txt) % 1441 != 0:
            print('Set first guess to true and try again!')
            print(len(queue_txt))
            os.remove('queue.txt')    
            print('queue.txt has not the right length.')
            time.sleep(10)                                                                                #Check and delete

        #reading result from first guess
        if os.path.isfile('first_guess.txt'):
            first_guess = pd.read_csv('first_guess.txt', sep = ' ', header=None)
        else:
            print('Run experiment first. No first_guess found')
            print('Set first_guess to True')
            time.sleep(20)  
        return log, ts, 1, first_guess, queue_txt

    if os.path.isfile('first_guess.txt'):
        print('Be aware: first_guess is true!\n')
        print('Be aware: first_guess is true!\n')
        print('Be aware: first_guess is true!\n')
        print('Be aware: first_guess is true!\n')

    f= open("iterationnumber.txt","r")
    it_n = 1 + int(f.read())
    f.close()
    log.write('------------------------------------------------------\n')
    log.write('---- ' + ts + '    Iteration ' + str(it_n) + ' has started.  ----\n')
    log.write('------------------------------------------------------\n')
    
    if not os.path.isfile('exp_results.txt'):
        print('Do experiment first!')
        print(' exp_results.txt does not exist.')
        log.write('Do experiment first!')
        log.write('exp_results.txt does not exist.')
        time.sleep(10)
    exp_txt = pd.read_csv('exp_results.txt', sep = ' ', header=None)
    log.write('exp_results.txt has been successfully opened.\n')
    log.write(' It holds ' + str(len(exp_txt)) + ' datasets.\n')

    queue_txt = queue_txt_usable(log)
    return log, ts, it_n, exp_txt, queue_txt

def sample_data(queue_txt, log):
    runtimes = int(len(queue_txt)/1441)
    one_queue = np.zeros((4,1441))
    for run in range(runtimes):
        for i in range(1441):
            one_queue[1][i] += queue_txt[1][i+run*1441] #service
            one_queue[2][i] += queue_txt[2][i+run*1441] #receive
            one_queue[3][i] += queue_txt[3][i+run*1441] #kitchen
    one_queue /= runtimes
    one_queue[0] = list(range(0, len(one_queue[0])))

    shift_queue = np.zeros((4,49))
    for i in range(49):
        for run in range(31):
            shift_queue[1][i] += queue_txt[1][i*30+run]
            shift_queue[2][i] += queue_txt[2][i*30+run]
            shift_queue[3][i] += queue_txt[3][i*30+run]
    shift_queue /= 30
    shift_queue[0] = list(range(0, len(one_queue[0]),30))
    log.write('A sampled queue has been calculated.\n')
    return one_queue, shift_queue

def allocation(log):

    log.write('Allocation_staff.xlsx is read.\n')
    current_allocation = pd.read_excel('Allocation_staff.xlsx', index = False)
    current_allocation = np.asarray(current_allocation)
    waiter = np.zeros(48)
    cooks  = np.zeros(48)
    for i in range(48):
        waiter[i] = int(current_allocation[i][1])
        cooks[i]  = int(current_allocation[i][2])
    print(waiter)
    return waiter, cooks

def allocation_fg(log, first_guess):
    log.write('Allocation is read from experiment.\n')
    waiter = np.zeros(48)
    cooks  = np.zeros(48)
    interval = int((len(first_guess)-1)/48)
    for i in range(len(first_guess)-1):
        waiter[int(i/interval)] += (first_guess[1][i]+0.4) / interval
        cooks[int(i/interval)]   += (first_guess[2][i]+0.4) / interval
    return waiter, cooks

def upd_ql(log, it_n, waiter, cooks, shift_queue):
    log.write('The current allocation gets updated because of queue lengths.\n')
    co_ql = np.zeros(4) #w+(0),w-(1),c+(2),c-(3) 

    for i in range(48):
        if shift_queue[1][i] > 80 and it_n < 10:
            waiter[i] += 3
            cooks[i] += 1
            co_ql[0] += 3
            co_ql[2] += 1
            log.write(' In shift ' + str(i) + ' 3 waiters and one cook are added bc ' + str(shift_queue[1][i]) + '.\n')
        elif shift_queue[1][i] > 50 and it_n < 10:
            waiter[i] += 2
            co_ql[0] += 2
            log.write(' In shift ' + str(i) + ' 2 waiters are added bc ' + str(shift_queue[1][i]) + '.\n')
        elif shift_queue[1][i] > (waiter[i]*3+4)*(it_n+20)/20 and it_n < 30:
            waiter[i] += 1
            co_ql[0] += 1
            log.write(' In shift ' + str(i) + ' 1 waiter is added bc ' + str(shift_queue[1][i]) + '.\n')
        elif shift_queue[1][i] < 2 and waiter[i] > 2 and it_n < 10:
            waiter[i] -= 2
            co_ql[1] += 2
            log.write(' In shift ' + str(i) + ' 2 waiters are removed bc ' + str(shift_queue[1][i]) + '; now' + str(waiter[i]) + '.\n')
        elif (shift_queue[1][i] < (waiter[i]/2+1)*6/(it_n+8) and it_n < 30 and waiter[i] > 1):
            waiter[i] -= 1
            co_ql[1] += 1
            log.write(' In shift ' + str(i) + ' 1 waiter is removed added bc '  + str(shift_queue[1][i]) + '; now' + str(waiter[i]) + '.\n')

        if shift_queue[3][i] > 80 and it_n < 10:
            cooks[i] += 4
            co_ql[2] += 4
            log.write(' In shift ' + str(i) + ' 4 cooks are added bc ' + str(shift_queue[3][i] )+ '.\n')
        elif shift_queue[3][i] > 50 and it_n < 10:
            cooks[i] += 3
            co_ql[2] += 3
            log.write(' In shift ' + str(i) + ' 3 cooks are added bc ' + str(shift_queue[3][i]) + '.\n')
        elif shift_queue[3][i] > 30 and it_n < 10:
            cooks[i] += 2
            co_ql[2] += 2
            log.write(' In shift ' + str(i) + ' 2 cooks are added bc ' + str(shift_queue[3][i]) + '.\n')
        elif shift_queue[3][i] > (cooks[i]*5+7)*(it_n+20)/20 and it_n < 30:
            cooks[i] += 1
            co_ql[2] += 1
            log.write(' In shift ' + str(i) + ' 1 cook is added bc ' + str(shift_queue[3][i]) + '.\n')
        elif shift_queue[3][i] < 1 and cooks[i] > 2 and it_n < 10:
            cooks[i] -= 2
            co_ql[3] += 2
            log.write(' In shift ' + str(i) + ' 2 cooks are removed bc ' +  str(shift_queue[3][i])+ '; now' + str(cooks[i]) +'.\n')
        elif (shift_queue[3][i] < (cooks[i]/2+1.5)*8/(it_n+8) and it_n < 30
            and cooks[i] > 1):
            cooks[i] -= 1
            co_ql[3] += 1
            log.write(' In shift ' + str(i) + ' 1 cook is removed bc ' +  str(shift_queue[3][i]) + '; now' + str(cooks[i]) +'.\n')
    log.write('Update because of queue length is finished.\n\n')
    log.write('Due to queue length, ' + str(co_ql[0]) + ' waiter and ' + str(co_ql[2]) + ' has to be added.\n')
    log.write('                and, ' + str(co_ql[1]) + ' waiter and ' + str(co_ql[3]) + ' has to be removed.\n')   
    return waiter, cooks, co_ql

def upd_obj(log, it_n, waiter, cooks, shift_queue, mean_res):

    obj_5ord = 0.7
    obj_8ord = 0.99
    obj_5kit = 0.7
    obj_8kit = 0.82

    #Change current allocation regarding objectives.
    co_obj = np.zeros(4) #w+(0),w-(1),c+(2),c-(3) 
    
    highest_que_service = np.argsort(-shift_queue[1][:])
    highest_que_kitchen = np.argsort(-shift_queue[2][:])


    if   mean_res[2] < obj_5ord:
        co_obj[0] += int((1-mean_res[2])/(1-obj_5ord))
        #co_obj[0] += max(1,int((obj_5ord -mean_res[2])*25+1.8))
    elif mean_res[3] < obj_8ord:
        co_obj[0] += int((1-mean_res[3])/(1-obj_8ord))
        #co_obj[0] += max(1,int((obj_8ord-mean_res[3])* 8+1.8))
    if   mean_res[8] < obj_5kit:
        co_obj[2]   += max(1,int((obj_5kit -mean_res[8])*25+1.8))
    elif mean_res[9] < obj_8kit:
        co_obj[2]   += max(1,int((obj_8kit -mean_res[9])* 8+1.8))

    if (mean_res[2] > obj_5ord and mean_res[3] > obj_8ord):
        co_obj[1] += 1
    if (mean_res[8] > obj_5kit and mean_res[9] > obj_8kit):
        co_obj[3] += 1
    

    queue_waiter = shift_queue[1][:-1]*(waiter[:]+10)/(waiter[:]+7)
    queue_cook = shift_queue[3][:-1]*(cooks[:]+10)/(cooks[:]+7)

    highest_que_service = np.argsort(-queue_waiter)
    highest_que_kitchen = np.argsort(-queue_cook)

    for i in range(int(co_obj[0])):
        waiter[highest_que_service[i]] +=1
        log.write('One waiter in shift ' + str(highest_que_service[i])+ ' has to be added.\n')
    for i in range(int(co_obj[2])):
        cooks[highest_que_kitchen[i]]  +=1
        log.write('One cook in shift ' + str(highest_que_kitchen[i])+ ' has to be added.\n')
    k = 47
    for i in range(int(co_obj[1])):
        while waiter[highest_que_service[k]] == 1:
            k -= 1
        waiter[highest_que_service[k]] -= 1
        log.write('One waiter in shift ' + str(highest_que_service[k])+ ' has to be removed.\n')
        k -= 1
    k = 47
    for i in range(int(co_obj[3])):
        while cooks[highest_que_kitchen[k]] == 1:
            k -= 1
        cooks[highest_que_kitchen[k]] -= 1
        log.write('One cook in shift ' + str(highest_que_kitchen[k])+ ' has to be removed.\n')
        k -= 1
    
    log.write('To hold objectives, ' + str(co_obj[0]) + ' waiter and ' + str(co_obj[2]) + ' has to be added.\n')
    log.write('To hold objectives, ' + str(co_obj[1]) + ' waiter and ' + str(co_obj[3]) + ' has to be removed.\n')

    return waiter, cooks, co_obj

def upd_sm(log, it_n, waiter, cooks, co_ql, co_obj):
    co_sm = np.zeros(4) #w+(0),w-(1),c+(2),c-(3) 
    if co_ql[0] + co_obj[0] + co_ql[2] + co_obj[2] < 15 and it_n % 2 == 0:
        log.write('Check if the function has to be smoothened.\n')
        max_w = max(waiter)
        max_c = max(cooks)
        for i in range(1,47):
            if (waiter[i] < waiter[i-1] and waiter[i] < waiter[i+1]):
                var = abs(waiter[i]- min(waiter[i-1],waiter[i+1]))
                co_sm[0] += var
                log.write(' In shift ' + str(i) + ' ' + str(var) + ' waiter are added (Obj).\n')
                waiter[i] = min(waiter[i-1],waiter[i+1])
            if (waiter[i] > waiter[i-1] and waiter[i] > waiter[i+1] and waiter[i] != max_w):
                var = abs(waiter[i]-max(waiter[i-1],waiter[i+1]))
                co_sm[1] += var
                log.write(' In shift ' + str(i) + ' ' + str(var) + ' waiter are removed (Obj).\n')
                waiter[i] = max(waiter[i-1],waiter[i+1])
        for i in range(1,47):
            if (cooks[i] < cooks[i-1] and cooks[i] < cooks[i+1]):
                var = abs(cooks[i]-min(cooks[i-1],cooks[i+1]))
                co_sm[2] += var
                log.write(' In shift ' + str(i) + ' ' + str(var) + ' cooks are added (Obj).\n')
                cooks[i] = min(cooks[i-1],cooks[i+1])
            if (cooks[i] > cooks[i-1] and cooks[i] > cooks[i+1] and cooks[i] != max_c):
                var = abs(cooks[i]-max(cooks[i-1],cooks[i+1]))
                co_sm[3] += var
                log.write(' In shift ' + str(i) + ' ' + str(var) + ' cooks are removed (Obj).\n')
                cooks[i] = max(cooks[i-1],cooks[i+1])    
        log.write('Due to smoothing, ' + str(co_sm[0]) + ' waiter and ' + str(co_sm[2]) + ' has to be added.\n')
        log.write('Due to smoothing, ' + str(co_sm[1]) + ' waiter and ' + str(co_sm[3]) + ' has to be removed.\n')
        print('Due to smoothing, %d waiter and %d has to be added.' % (co_sm[0] ,co_sm[2]))
        print('             and, %d waiter and %d has to be removed.' % (co_sm[1] ,co_sm[3]))
    else: log.write('The function has not been smoothened.\n')
    return waiter, cooks, co_sm

def print_changes(log, waiter, cooks, co_ql, co_obj, co_sm):
    print('Next try, we have %d waiter shifts more and %d less,'
        ' all in all %d shifts.' %
            (co_ql[0] + co_obj[0] + co_sm[0], co_ql[1] + co_obj[1] + co_sm[1], sum(waiter)))
    print('Next try, we have %d cook shifts more and %d less,'
        ' all in all %d shifts.' %
        (co_ql[2] + co_obj[2] + co_sm[2], co_ql[3] + co_obj[3] + co_sm[3], sum(cooks)))
    log.write('Next try, we have %d waiter shifts more and %d less,'
        ' all in all %d shifts.\n' %
            (co_ql[0] + co_obj[0] + co_sm[0], co_ql[1] + co_obj[1] + co_sm[1], sum(waiter)))
    log.write('Next try, we have %d cook shifts more and %d less,'
        ' all in all %d shifts.\n' %
        (co_ql[2] + co_obj[2] + co_sm[2], co_ql[3] + co_obj[3] + co_sm[3], sum(cooks)))

def write_to_file(log, waiter, cooks, first_guess = False):
    df = DataFrame({'Time (in minutes)': range(0,1440,30),
                    '#Waiter': waiter, '#Cooks': cooks,
                    'First_guess':'false'})
    df.to_excel('Allocation_staff.xlsx',index = False, header = True,
                sheet_name='allocation_staff')
    if first_guess == True:
        timeline = ''
        for i in range(0,1440,30):
            timeline += str(i) + ' '
        waiter_txt = open('waiter.txt','w')
        waiter_txt.write(timeline + '\n')
    else: waiter_txt = open('waiter.txt','a')
    waiter_txt.write(' '.join(map(str,waiter.astype(int))) + '\n')
    waiter_txt.close()
    if first_guess == True:
        cook_txt = open('cook.txt','w')
        cook_txt.write(timeline + '\n')
    else: cook_txt = open('cook.txt','a')
    cook_txt.write(' '.join(map(str,cooks.astype(int))) + '\n')
    cook_txt.close()
    log.write('Allocation_staff.xlsx, waiter.txt, and cook.txt are updated.\n')

def print_3_im_new_all(ts, it_n, log, waiter, cooks):
    plt.step(range(0,1440,30), waiter.astype(int), label = 'Waiter')
    plt.step(range(0,1440,30), cooks.astype(int), label = 'Cook')
    plt.title('Staffing per time')
    plt.xlabel('minutes (Model Time)')
    plt.ylabel('Number of staff')
    plt.legend(loc = 'best')
    axes = plt.gca()
    axes.set_xlim([0,990])
    axes.set_ylim([0,50])

    plt.savefig(ts +'_3_Iteration_'+ str(it_n)+'.png', dpi = 300)
    plt.savefig('3_'+ ts +'_Iteration_'+ str(it_n)+'.png', dpi = 300)
    plt.close()
    log.write('A plot about the new staff allocation is created and saved as two images.\n')

def print_3_fg(ts, log, first_guess):
    plt.step(first_guess[0][:],first_guess[1][:], label = 'Waiter')
    plt.step(first_guess[0][:],first_guess[2][:], label = 'Cook')
    plt.title('Staffing per time - first guess')
    plt.xlabel('minutes (Model Time)')
    plt.ylabel('Number of staff')
    plt.legend(loc = 'best')
    axes = plt.gca()
    axes.set_xlim([0,990])
    axes.set_ylim([0,50])

    plt.savefig(ts + '_3_Iteration_0_first_guess.png', dpi = 300)
    plt.savefig('3_'+ ts +'_Iteration_0.png', dpi = 300)
    plt.close()

def finish(it_n, log):
    log.write('queue.txt/first_guess.txt and exp_results.txt is not necessary anymore and therefore removed.\n')
    if it_n == 1: os.remove('first_guess.txt')
    else: os.remove('queue.txt')
    os.remove('exp_results.txt')

    f= open("iterationnumber.txt","w")
    f.write(str(it_n))
    f.close()

    print('Iteration ' + str(it_n) + ' has successfully completed!')

    log.write('Iteration ' + str(it_n) + ' has successfully completed!\n\n')
    log.close()

def cleaner():
    #Set timestamp
    ts = time.gmtime()
    ts = time.strftime("%y%m%d_%H%M%S",ts)

    folder = ts + '_closed_experiment/'

    if not os.path.exists(folder):
        os.makedirs(folder)

    mv_files = ['cook.txt','waiter.txt','mean_results.txt','stdev_results.txt',
        'iterationnumber.txt', 'exp_results.txt','first_guess.txt','logfile.txt',
        'queue.txt']
    for mv_file in mv_files:
        if os.path.isfile(mv_file):
            os.rename(mv_file,folder + mv_file)

    for images in glob.glob("20*.png"):
        os.rename(images,folder + images) 
    for images in glob.glob("1_*.png"):
        os.rename(images,folder + images) 
    for images in glob.glob("2_*.png"):
        os.rename(images,folder + images) 
    for images in glob.glob("3_*.png"):
        os.rename(images,folder + images) 
   











