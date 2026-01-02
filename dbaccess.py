import psycopg2
import json 
from datetime import datetime, timedelta

class databaseConn(object):

    def __init__(self):

        with open(r"credentials.json", "r") as credentials:
            creds = json.loads(credentials.read())

        self.db_conn = psycopg2.connect(database=creds['database'],
        user=creds['user'],
        password=creds['password'],
        host=creds['host'],
        port=creds['port'])

    ''' functions for Fantasy 
    '''
    def get_fantasy_data(self):

        select_sql = f'''
        select to_char(draw_date, 'YYYY-MM-DD'), numa, numb, numc, numd, nume
        from fantasy_five
        order by draw_date desc
        '''

        cur = self.db_conn.cursor()

        cur.execute(select_sql)

        winners = cur.fetchall()

        cur.close()

        return winners

    def get_fantasy_select(self, count):

        ''' This function will get only the last N winners
        '''

        select_sql = f'''
        select to_char(draw_date, 'YYYY-MM-DD'), numa, numb, numc, numd, nume
        from fantasy_five
        order by draw_date desc
        limit {count}
        '''

        cur = self.db_conn.cursor()

        cur.execute(select_sql)

        winners = cur.fetchall()

        cur.close()

        ''' convert to list and get only the numbers before returning
        '''
        winners = [list(w) for w in winners]
        
        winners = [w[1:] for w in winners]

        return winners

    def get_fantasy_filtered(self, selected):

        select_list = "({}, {}, {}, {}, {})".format(selected[0], selected[1], selected[2], selected[3], selected[4])

        select_sql = f'''
        select to_char(draw_date, 'YYYY-MM-DD'), numa, numb, numc, numd, nume
        from fantasy_five
        where numa in {select_list}
        or numb in {select_list}
        or numc in {select_list}
        or numd in {select_list}
        or nume in {select_list}
        order by draw_date desc
        '''

        cur = self.db_conn.cursor()

        cur.execute(select_sql)

        winners = cur.fetchall()

        cur.close()

        # select only those that have four or more matches
        winners_select = []
        for win in winners:
            if len(set(win[1:]).intersection(set(selected))) >= 4:
                winners_select.append(win)

        return winners_select

    def check_fantasy_winner(self, numbers, play_date=''):

        cur = self.db_conn.cursor()

        select_sql = f'''
        select draw_date from fantasy_five
        where numa = {numbers[0]}
        and numb = {numbers[1]}
        and numc = {numbers[2]}
        and numd = {numbers[3]}
        and nume = {numbers[4]}
        '''

        if play_date:
            select_sql = select_sql + f'''and draw_date >= '{play_date}' '''

        cur.execute(select_sql)

        return True if cur.fetchall() else False

    def check_close_fantasy_winner(self, numbers):

        select_list = "({}, {}, {}, {}, {})".format(numbers[0], numbers[1], numbers[2], numbers[3], numbers[4])
        last_date = (datetime.now() - timedelta(2000)).strftime("%Y-%m-%d")

        cur = self.db_conn.cursor()

        select_sql = f'''
        select to_char(draw_date, 'YYYY-MM-DD'), numa, numb, numc, numd, nume
        from fantasy_five
        where (numa in {select_list}
        or numb in {select_list}
        or numc in {select_list}
        or numd in {select_list}
        or nume in {select_list})
        and draw_date > '{last_date}'
        order by draw_date
        '''

        cur.execute(select_sql)
        winners = cur.fetchall()
        cur.close()

        ''' convert to list before comparing
        '''
        winners = [list(w) for w in winners]

        win_select = [w for w in winners if len(set(w[1:]).intersection(set(numbers))) in [4,5]]

        return True if len(win_select) == 0  else False

    def store_fantasy_plays(self, generated):

        play_date = (datetime.now()).strftime("%Y-%m-%d")

        cur = self.db_conn.cursor()

        '''
        get sequence number with today's date
        '''

        select_sql = f'''
        select max(seq_num)
        from fantasy_five_bets
        where play_date = '{play_date}'
        '''

        cur.execute(select_sql)
        seq_num = cur.fetchall()[0][0]
        if seq_num:
            seq_num += 1
        else:
            seq_num = 1

        saved_ind = False

        for gen in generated:

            '''
            insert
            '''

            insert_sql = f'''
            insert into fantasy_five_bets
            (numa, numb, numc, numd, nume, play_date, seq_num, saved_ind)
            values ({gen[0]}, {gen[1]}, {gen[2]}, {gen[3]},  \
                    {gen[4]}, '{play_date}', {seq_num}, {saved_ind}) '''

            cur.execute(insert_sql)
            self.db_conn.commit()

        cur.close()

    def save_fantasy_plays(self):

        play_date = (datetime.now()).strftime("%Y-%m-%d")

        cur = self.db_conn.cursor()

        '''
        get sequence number with today's date
        '''

        select_sql = f'''
        select max(seq_num)
        from fantasy_five_bets
        where play_date = '{play_date}'
        '''

        cur.execute(select_sql)
        seq_num = cur.fetchall()[0][0]

        '''
        update
        '''

        saved_ind = True

        update_sql = f'''
        update fantasy_five_bets
        set saved_ind = {saved_ind}
        where play_date = '{play_date}'
        and seq_num = {seq_num}
        '''

        cur.execute(update_sql)
        self.db_conn.commit()

        cur.close()

    def delete_fantasy_plays(self):

        cur = self.db_conn.cursor()

        saved_ind = False

        '''
        delete all rows that does not have saved indicator set
        '''
        delete_sql = f'''
        delete from fantasy_five_bets
        where saved_ind = {saved_ind}
        '''

        cur.execute(delete_sql)
        self.db_conn.commit()
        cur.close()

    ''' functions for Mega, Powerball and Super
    '''
    def get_mps_data(self, table_name):

        select_sql = f'''
        select to_char(draw_date, 'YYYY-MM-DD'), numa, numb, numc, numd, nume, numx
        from {table_name}
        order by draw_date desc
        '''

        cur = self.db_conn.cursor()

        cur.execute(select_sql)

        winners = cur.fetchall()

        cur.close()

        return winners

    def get_mps_select(self, table_name, count):

        ''' This function will get only the last N winners
        '''

        select_sql = f'''
        select to_char(draw_date, 'YYYY-MM-DD'), numa, numb, numc, numd, nume
        from {table_name}
        order by draw_date desc
        limit {count}
        '''

        cur = self.db_conn.cursor()

        cur.execute(select_sql)

        winners = cur.fetchall()

        cur.close()

        ''' convert to list and get only the numbers before returning
        '''
        winners = [list(w) for w in winners]
        
        winners = [w[1:] for w in winners]

        return winners

    def get_mps_filtered(self, table_name, selected):

        select_list = "({}, {}, {}, {}, {})".format(selected[0], selected[1], selected[2], selected[3], selected[4])
        extr_num = selected[5]

        select_sql = f'''
        select to_char(draw_date, 'YYYY-MM-DD'), numa, numb, numc, numd, nume, numx
        from {table_name}
        where numa in {select_list}
        or numb in {select_list}
        or numc in {select_list}
        or numd in {select_list}
        or nume in {select_list}
        or numx = {extr_num}
        order by draw_date desc
        '''

        cur = self.db_conn.cursor()

        cur.execute(select_sql)

        winners = cur.fetchall()

        cur.close()

        # select only those that have four or more matches
        winners_select = []
        for win in winners:
            int_len = len(set(win[1:6]).intersection(set(selected)))
            if int_len >= 2:
                win_data = list(win)
                win_data.append(int_len)
                winners_select.append(win_data)

        return winners_select

    def check_mps_winner(self, table_name, numbers, play_date=''):

        cur = self.db_conn.cursor()

        select_sql = f'''
        select draw_date from {table_name}
        where numa = {numbers[0]}
        and numb = {numbers[1]}
        and numc = {numbers[2]}
        and numd = {numbers[3]}
        and nume = {numbers[4]}
        '''

        if play_date:
            select_sql = select_sql + f'''and draw_date >= '{play_date}' '''

        cur.execute(select_sql)

        return True if cur.fetchall() else False

    def store_mps_plays(self, table_name, generated): 

        play_date = (datetime.now()).strftime("%Y-%m-%d")

        cur = self.db_conn.cursor()

        '''
        get sequence number with today's date
        '''

        select_sql = f'''
        select max(seq_num)
        from {table_name}
        where play_date = '{play_date}'
        '''

        cur.execute(select_sql)
        seq_num = cur.fetchall()[0][0]
        if seq_num:
            seq_num += 1
        else:
            seq_num = 1

        saved_ind = False

        for gen in generated:

            '''
            insert
            '''

            insert_sql = f'''
            insert into {table_name}
            (numa, numb, numc, numd, nume, numx, play_date, seq_num, saved_ind)
            values ({gen[0]}, {gen[1]}, {gen[2]}, {gen[3]}, {gen[4]},  \
                    {gen[5]}, '{play_date}', {seq_num}, {saved_ind}) '''

            cur.execute(insert_sql)
            self.db_conn.commit()

        cur.close()

    def save_mps_plays(self, table_name):

        play_date = (datetime.now()).strftime("%Y-%m-%d")

        cur = self.db_conn.cursor()

        '''
        get sequence number with today's date
        '''

        select_sql = f'''
        select max(seq_num)
        from {table_name}
        where play_date = '{play_date}'
        '''

        cur.execute(select_sql)
        # seq_num = cur.fetchall()[0][0]
        seq_num = cur.fetchall()[0][0]
        
        '''
        update
        '''
        saved_ind = True

        update_sql = f'''
        update {table_name}
        set saved_ind = {saved_ind}
        where play_date = '{play_date}'
        and seq_num = {seq_num}
        '''

        cur.execute(update_sql)
        self.db_conn.commit()

        cur.close()

    def get_plays(self, table_name, extra):

        saved_ind = True

        if extra:
            select_sql = f'''
            select to_char(play_date, 'YYYY-MM-DD'), numa, numb, numc, numd, nume, numx
            from {table_name}
            where saved_ind = {saved_ind}
            order by play_date desc, seq_num desc
            '''
        else:
            select_sql = f'''
            select to_char(play_date, 'YYYY-MM-DD'), numa, numb, numc, numd, nume
            from {table_name}
            where saved_ind = {saved_ind}
            order by play_date desc, seq_num desc
            '''

        cur = self.db_conn.cursor()

        cur.execute(select_sql)

        winners = cur.fetchall()

        cur.close()

        return winners


    def delete_mps_plays(self, table_name):

        cur = self.db_conn.cursor()

        saved_ind = False

        '''
        delete all rows that does not have saved indicator set
        '''
        delete_sql = f'''
        delete from {table_name}
        where saved_ind = {saved_ind}
        '''

        cur.execute(delete_sql)
        self.db_conn.commit()

    ''' functions for Fantasy, Mega, Powerball and Super
    '''
    def get_number_stats(self, table_name, order):

        if order == 0 or order == 1:

            select = f'''
            select A.num, sum(A.tot)
            from (
                select numa as num, count(*) as tot from {table_name} group by numa
                union
                select numb as num, count(*) as tot from {table_name} group by numb
                union
                select numc as num, count(*) as tot from {table_name} group by numc
                union
                select numd as num, count(*) as tot from {table_name} group by numd
                union
                select nume as num, count(*) as tot from {table_name} group by nume
                ) A

            group by A.num

            '''

            if order == 0:
                select += ' order by sum(A.tot) desc, A.num asc'
            else:
                select += ' order by A.num asc'

        else:

            select = f'''

            select numx, drwx 
            from (
                select num as numx, max(drw) as drwx 
                from (
                    select numa as num, draw_date as drw from {table_name} 
                    union
                    select numb as num, draw_date as drw from {table_name}
                    union
                    select numc as num, draw_date as drw from {table_name}
                    union
                    select numd as num, draw_date as drw from {table_name}
                    union
                    select nume as num, draw_date as drw from {table_name}
                    ) as A
                    
                    group by A.num) as B
            
            order by B.drwx desc
            '''
        cur = self.db_conn.cursor()

        cur.execute(select)

        number_counts = cur.fetchall()

        if order == 0 or order == 1:
            number_counts = [[n, int(c)] for n, c in number_counts]
        else:
            number_counts = [[n, str(c)] for n, c in number_counts]

        cur.close()

        return number_counts

    def get_extra_stats(self, table_name, order):

        if order == 0 or order == 1:
            select = f'''
            select numx as num, count(*) as tot from {table_name} group by numx
            '''

            if order == 0:
                select += ' order by tot desc'
            else:
                select += ' order by num asc'
        else:
            select = f'''
            select numx, max(draw_date) as maxdd 
            from (
                
                select numx, draw_date from {table_name}) as A
                
                group by numx
                order by maxdd desc
            '''

        cur = self.db_conn.cursor()

        cur.execute(select)

        number_counts = cur.fetchall()

        if order == 0 or order == 1:
            number_counts = [[n, int(c)] for n, c in number_counts]
        else:
            number_counts = [[n, str(c)] for n, c in number_counts]

        cur.close()

        return number_counts

    def get_top_stats_by_date(self, draw_date, table_name):

        select = f'''
        select A.num, sum(A.tot)
        from (
            select numa as num, count(*) as tot from {table_name} where draw_date < '{draw_date}' group by numa
            union
            select numb as num, count(*) as tot from {table_name} where draw_date < '{draw_date}' group by numb
            union
            select numc as num, count(*) as tot from {table_name} where draw_date < '{draw_date}' group by numc
            union
            select numd as num, count(*) as tot from {table_name} where draw_date < '{draw_date}' group by numd
            union
            select nume as num, count(*) as tot from {table_name} where draw_date < '{draw_date}' group by nume
            ) A

        group by A.num
        order by sum(A.tot) desc, A.num asc
        '''

        cur = self.db_conn.cursor()

        cur.execute(select)

        number_count = cur.fetchall()

        number_count = [n for n, c in number_count]

        return number_count

    def get_latest_winner(self, table_name):

        select_sql = f'''
        select to_char(draw_date, 'YYYY-MM-DD'), numa, numb, numc, numd, nume
        from {table_name}
        order by draw_date desc
        limit 1
        '''

        cur = self.db_conn.cursor()

        cur.execute(select_sql)

        winners = cur.fetchall()

        cur.close()

        return winners
    
    def get_combo_index(self, combo_key, table_name):

        select_sql = f'''
        select combo_idx
        from {table_name}
        where combo_key = '{combo_key}'
        '''

        cur = self.db_conn.cursor()

        cur.execute(select_sql)

        idx_key_list = cur.fetchall()

        cur.close()

        return idx_key_list[0][0]
    
    def execute_select(self, select_sql):

        cur = self.db_conn.cursor()

        cur.execute(select_sql)

        select_data = cur.fetchall()

        cur.close()

        return select_data

    def execute_insert(self, insert_sql, data):

        cur = self.db_conn.cursor()

        try: 
            cur.execute(insert_sql, data)
            self.db_conn.commit()
            cur.close()

            return True 

        except Exception as e:
            print(e)
            cur.close()
            return False

    def execute_update(self, update_sql):

        cur = self.db_conn.cursor()

        try: 
            cur.execute(update_sql)
            self.db_conn.commit()
            cur.close()

            return True 
        except Exception as e:
            print(e)
            cur.close()
            return False