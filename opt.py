import functions as fc
import sys

def cleaner():
    fc.cleaner()

def opt_fg():
    #Check if queue.txt is usable
    log, ts, it_n, first_guess, queue_txt = fc.setup(True)                            

    #Get data and sample them                                 
    one_queue, shift_queue = fc.sample_data(queue_txt, log)
    fc.print_pic_1_2(one_queue, shift_queue, queue_txt, it_n, ts, log)

    waiter, cooks = fc.allocation_fg(log, first_guess)

    fc.write_to_file(log, waiter, cooks, True)

    fc.print_3_fg(ts, log, first_guess)
    fc.print_3_im_new_all(ts, it_n, log, waiter, cooks)

    #Check for number of values file
    fc.finish(it_n, log)


def opt():
    #Set objectives
    obj_5ord = 0.7
    obj_8ord = 0.99
    obj_5kit = 0.7
    obj_8kit = 0.82


    #Set timestamp and iterationnumber and if queue.txt is usable
    log, ts, it_n, exp_txt, queue_txt = fc.setup()

    #Analyse previous results
    mean_res, std_res = fc.analyse(exp_txt, log)

    #Objectives fulfilled?
    fc.obj_fulfill(mean_res, log)

    #Utilisation rates
    fc.ut_rates(mean_res, log)

    #Get data and sample them
    one_queue, shift_queue = fc.sample_data(queue_txt, log)

    # print 1_queue_Iteration and 2_shift_queue_iteration
    max_dia = fc.print_pic_1_2(one_queue, shift_queue, queue_txt, it_n, ts, log)

    #Update staff allocation (1. get and allocate, 2. update queues, 3. update obj)
    waiter, cooks = fc.allocation(log)
    waiter, cooks, co_ql  = fc.upd_ql(log, it_n, waiter, cooks, shift_queue)
    waiter, cooks, co_obj = fc.upd_obj(log, it_n, waiter, cooks, shift_queue, mean_res)
    waiter, cooks, co_sm  = fc.upd_sm(log, it_n, waiter, cooks, co_ql, co_obj)
    fc.print_changes(log, waiter, cooks, co_ql, co_obj, co_sm)
    print(waiter)
    print(cooks)
    #Write to files (allocation_staff.xlsx, waiter.txt, cook.txt)
    fc.write_to_file(log, waiter, cooks)

    #produce staffing plot
    fc.print_3_im_new_all(ts, it_n, log, waiter, cooks)

    #Clean up, update iterationnumber
    fc.finish(it_n, log)


    #Find ending criteria
    #   2 shifts get changed.
    # <3 shifts more and or less
    # criteria are fullfilled
    #print std_dev_results.txt      just results from exp_results.txt
    #print mean_results.txt         
    #   first_guess std_dev just zeros, mean just print exp_results
    #   afterwards mean_results are already there
    #   for it_n > 10: check if std_dev is sufficiently small.



    #Criteria:
    # a) Objectives have to be fulfilled
    # b) Change shifts = 0
    # c) Choose value with smallest number of shifts.