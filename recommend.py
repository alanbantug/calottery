
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
            diff_days = 4

        if self.topRange == 47:
            all_winners = dbconn.get_mps_data('super_lotto')

            raw_winners = []
            for winner in all_winners:
                raw_winners = [winner[:6] for winner in all_winners]

            hits_limit = 15
            diff_days = 12

        if self.topRange == 69:
            all_winners = dbconn.get_mps_data('power_ball')

            raw_winners = []
            for winner in all_winners:
                raw_winners = [winner[:6] for winner in all_winners]

            hits_limit = 5
            diff_days = 48

        winners = raw_winners
        print(winners[0])
        all_numbers = [i + 1 for i in range(self.topRange)]
        
        count = 0

        hi_select = []
        
        hi_hits = 0
        select_hits = 0
        select_latest = 0

        while True:
            try:
                random.shuffle(all_numbers)
                
                select = all_numbers[:25]

                hits = 0
                hi_hit_days = 0
                
                latest_hit = None
                hit_count = 0
                
                for winner in winners[:200]:
                    if self.check_winner(winner, select) == 5:
                        
                        if latest_hit:
                            pass
                        else:
                            hit_count += 1
                            if hit_count == 2:
                                latest_hit = datetime.strptime(winner[0], "%Y-%m-%d")
                            
                        hits += 1
                        
                if hits > hits_limit:
                    diff = date_today - latest_hit
                    if diff.days < diff_days:
                        if hits > hi_hits:
                            hi_select = sorted(select)
                            select_hits = hits
                            select_latest = latest_hit
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

        return hi_select





