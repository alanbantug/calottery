
from datetime import date, datetime, timedelta
import random

class recommendNumbers(object):
    
    def __init__(self, rtype):

        self.rtype = rtype

        if self.rtype == 1:
            self.topRange = 39

        elif self.rtype == 2:
            self.topRange = 47

        elif self.rtype == 3:
            self.topRange = 70

        elif self.rtype == 4:
            self.topRange = 69

    def check_winner(self, winner, select):

        dd, na, nb, nc, nd, ne = winner

        nums = [na, nb, nc, nd, ne]
        
        return len([num for num in nums if num in select])

    def getRecommendation(self, dbconn):

        date_today = datetime.today()
        start = datetime.now()
        print(start)

        if self.topRange == 39:
            raw_winners = dbconn.get_fantasy_data()
            hits_limit = 15
            diff_days = 3 # last hit within 3 days indicating current  

        if self.topRange == 47:
            all_winners = dbconn.get_mps_data('super_lotto')

            raw_winners = []
            for winner in all_winners:
                raw_winners = [winner[:6] for winner in all_winners]

            hits_limit = 15
            diff_days = 10 # last hit within 10 days (3 draws)

        if self.topRange == 69:
            all_winners = dbconn.get_mps_data('power_ball')

            raw_winners = []
            for winner in all_winners:
                raw_winners = [winner[:6] for winner in all_winners]

            hits_limit = 5
            # diff_days = 48
            diff_days = 10 # last hit within 10 days (4 draws)

        if self.topRange == 70:
            all_winners = dbconn.get_mps_data('mega_lotto')

            raw_winners = []
            for winner in all_winners:
                raw_winners = [winner[:6] for winner in all_winners]

            hits_limit = 5
            # diff_days = 48
            diff_days = 10 # last hit within 10 days (3 draws)

        winners = raw_winners

        all_numbers = [i + 1 for i in range(self.topRange)]
        
        count = 0

        hi_select = []
        
        hi_hits = 0
        select_hits = 0
        select_latest = 0
        select_longest = 0

        while True:

            last_hit = None
            next_hit = None
            hit_diff = 0

            try:
                random.shuffle(all_numbers)
                
                select = all_numbers[:25]

                hits = 0
                hi_hit_days = 0
                
                first_hit = None
                second_hit = None

                hit_count = 0
                longest_hit_diff = 0
                
                for winner in winners[:200]:
                    if self.check_winner(winner, select) == 5:
                        
                        if last_hit == None:
                            last_hit = datetime.strptime(winner[0], "%Y-%m-%d")
                        else:
                            next_hit = datetime.strptime(winner[0], "%Y-%m-%d")
                            hit_diff = last_hit - next_hit
                            if hit_diff.days > longest_hit_diff:
                                longest_hit_diff = hit_diff.days
                            last_hit = next_hit

                        if second_hit:
                            pass
                        else:
                            hit_count += 1 
                            if hit_count == 1:
                                first_hit = datetime.strptime(winner[0], "%Y-%m-%d")
                            if hit_count == 2:
                                second_hit = datetime.strptime(winner[0], "%Y-%m-%d")
                            
                        hits += 1
                        
                if hits > hits_limit:
                    diff1 = date_today - first_hit
                    diff2 = first_hit - second_hit
                    ''' check that the latest hit occured in the last diff_days and the difference between the first
                        and second hits is the longest hit diffence. assumption is the combo is in current phase
                    '''
                    if diff1.days <= diff_days and diff2.days == longest_hit_diff:
                        if hits > hi_hits:
                            hi_select = sorted(select)
                            select_hits = hits
                            select_latest = first_hit
                            select_second = second_hit
                            select_longest = longest_hit_diff
                            hi_hits = hits
                    
                count += 1
            except Exception as e:
                print(e)
                break

            if count == 500000:
                break

        end = datetime.now()
        print(end)
        print("Time elapsed  : ", end - start)

        print('Selection     : ', hi_select )
        print('Number of hits: ', select_hits)
        print('Latest hit    : ', select_latest)
        print('Latest hit    : ', select_second)
        print('Longest gap   : ', select_longest)

        return hi_select





