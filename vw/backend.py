import sqlite3
import logging

class VWBackend():
    def __init__(self):
        sqlite_file = "db.sqlite"
        self.conn = sqlite3.connect(sqlite_file)
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS plateinfo 
            (appartment TEXT, name TEXT, mainplate TEXT, subplate TEXT,
            type TEXT, zhongwai TEXT, approver TEXT, id INTERGER PRIMARY KEY, year INTEGER, phone TEXT, 
            printed INTEGER, printdate TEXT, verified INTEGER)''')

    # TODO: There might be some space in approver names, we can split it in the future
    def load_xls(self):
        import xlrd
        # from collections import namedtuple
        # xls_entry = namedtuple('xls_entry', ['appartment', 'name', 'mainplate', 'subplate', 'type', 'zhongwai', \
        #     'approver', 'id', 'year', 'phone'])
        worksheet = xlrd.open_workbook('2018车辆管理系统导入模板.xls').sheet_by_index(0)
        res = []
        for i in range(1, worksheet.nrows):
            try:
                row_value = worksheet.row_values(i)
                # Move decimal zeros in phone number
                row_value[9] = int(row_value[9])
                row_value[3] = None if not row_value[3] else row_value[3]
                row_value.append(0) # printed
                row_value.append(None) # printdate
                row_value.append(0) # verified
                exist = False
                for p in (row_value[2], row_value[3]):
                    if self.check_plate_exist(p, row_value[7]):
                        print(p, row_value[7])
                        res.append((p, "id={:d}".format(int(row_value[7]))))
                        exist = True
                if not exist:
                    self.c.execute('INSERT INTO plateinfo VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', row_value)
            except sqlite3.IntegrityError:
                # print("!!!This ID already exsits in the system:\n{}\n".format(row_value))
                pass
            except ValueError:
                raise ValueError
        self.conn.commit()
        return res

    @classmethod
    def getdatetime(cls):
        import datetime
        _time = datetime.datetime.now()
        return _time.strftime("%Y-%m-%d %H:%M:%S")

    def getvalues_with_id(self, _id):
        self.c.execute('SELECT * FROM plateinfo WHERE id = ?', (_id,))
        return self.c.fetchone()
    
    def search(self, k, show_printed):
        '''
        k: keyword string of search
        show_printed: bool
        return: a list of results
        '''
        date_signal = 0
        if not k:
            if not show_printed:
                print('not show printed')
                self.c.execute('SELECT * FROM plateinfo WHERE printed = 0')
                res = self.c.fetchall()
                self.c.execute('SELECT id FROM plateinfo WHERE verified = 1 and printed = 0')
                ids = self.c.fetchall()
            else:
                self.c.execute('SELECT * FROM plateinfo')
                res = self.c.fetchall()
                self.c.execute('SELECT id FROM plateinfo WHERE verified = 1')
                ids = self.c.fetchall()

        else:
            date = None
            if '@' in k:
                k, date = k.split('@')
                k = k.strip()
                date = date.strip()

                if '-' not in date:
                    # 1 means wrong date format
                    print('wrong date1', date)
                    return (1, None, None)
                else:
                    m, d = date.split('-')
                    if not m or not d:
                        print('wrong date2', date)
                        return (1, None, None)
                    if len(m) == 1:
                        m = "0" + m
                    if len(d) == 1:
                        d = '0' + d
            else:
                date_signal = 2
                    
            if not show_printed:
                if date:
                    excute_str = '''SELECT * FROM plateinfo WHERE printed = 0 AND 
                    (printdate LIKE "2018-{1}-{2}%" or printdate LIKE "2019-{1}-{2}%")
                    AND (appartment LIKE "%{0}%" OR name LIKE "%{0}%" OR mainplate LIKE "%{0}%" 
                    OR subplate LIKE "%{0}%")'''.format(k, m, d)

                    sub_str = '''SELECT id FROM plateinfo WHERE verified = 1 AND printed = 0 AND printdate LIKE "2018-{1}-{2}%"
                    AND (appartment LIKE "%{0}%" OR name LIKE "%{0}%" OR mainplate LIKE "%{0}%" 
                    OR subplate LIKE "%{0}%")'''.format(k, m, d)

                else:
                    excute_str = '''SELECT * FROM plateinfo WHERE printed = 0 AND 
                    (appartment LIKE "%{0}%" OR name LIKE "%{0}%" OR mainplate LIKE "%{0}%" 
                    OR subplate LIKE "%{0}%")'''.format(k)

                    sub_str = '''SELECT id FROM plateinfo WHERE verified = 1 AND printed = 0 AND 
                    (appartment LIKE "%{0}%" OR name LIKE "%{0}%" OR mainplate LIKE "%{0}%" 
                    OR subplate LIKE "%{0}%")'''.format(k)

            else:
                if date:
                    excute_str = '''SELECT * FROM plateinfo WHERE 
                    (printdate LIKE "2018-{1}-{2}%" OR printdate LIKE "2019-{1}-{2}%") 
                    AND (appartment LIKE "%{0}%" OR name LIKE "%{0}%" OR mainplate LIKE "%{0}%" OR 
                    subplate LIKE "%{0}%")'''.format(k, m, d)

                    sub_str = '''SELECT id FROM plateinfo WHERE 
                    (printdate LIKE "2018-{1}-{2}%" OR printdate LIKE "2019-{1}-{2}%") AND verified = 1
                    AND (appartment LIKE "%{0}%" OR name LIKE "%{0}%" OR mainplate LIKE "%{0}%" OR 
                    subplate LIKE "%{0}%")'''.format(k, m, d)

                else:
                    excute_str = '''SELECT * FROM plateinfo WHERE appartment LIKE "%{0}%" 
                    OR name LIKE "%{0}%" OR mainplate LIKE "%{0}%" OR subplate LIKE "%{0}%"'''.format(k)

                    sub_str = '''SELECT id FROM plateinfo WHERE verified = 1 AND (appartment LIKE "%{0}%" 
                    OR name LIKE "%{0}%" OR mainplate LIKE "%{0}%" OR subplate LIKE "%{0}%")'''.format(k)
                    
            self.c.execute(sub_str)
            ids = self.c.fetchall()
            self.c.execute(excute_str)
            res = self.c.fetchall()

        ids = [i[0] for i in ids]
        return (date_signal, ids, res)

    def check_plate_exist(self, plate, _id):
        if not plate:
            return None
        self.c.execute('SELECT * FROM plateinfo WHERE (id != ? AND id > 0) AND (mainplate = ? OR subplate = ?)', (_id, plate, plate, ))
        return self.c.fetchone()

    def update(self, values, _id):
        values.append(_id)
        self.c.execute('''UPDATE plateinfo SET appartment = ?, name = ?, mainplate = ?, 
                subplate = ?, type = ?, zhongwai = ?, approver = ?, year = ?, phone = ?, 
                printed = 0, printdate = NULL WHERE id = ?''', values)
        self.conn.commit()
    
    def set_ids_printed(self, ids):
        for _id in ids:
            self.c.execute('''UPDATE plateinfo SET printed = 1, printdate = ? WHERE id = ?''', 
            (self.getdatetime(), _id))
        self.conn.commit()
    
    def get_min_id(self):
        self.c.execute('SELECT MIN(id) FROM plateinfo')
        _id = self.c.fetchone()[0]
        return _id - 1 if _id and _id < 0 else -1

    def add_plate(self, values):
        print('Start Add-plate')
        values.append(0)
        values.append(None)
        values.append(0)
        self.c.execute('INSERT INTO plateinfo VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', values)
        self.conn.commit()
        print('Done Add-plate')
    
    def check_verified(self, _id):
        self.c.execute('SELECT verified FROM plateinfo WHERE id = ?', (_id,))
        return self.c.fetchone()
    
    def verify_plate(self, _id):
        self.c.execute('UPDATE plateinfo SET verified = 1 WHERE id = ?', (_id,))
        self.conn.commit()
    
    def deverify_plate(self, _id):
        self.c.execute('UPDATE plateinfo SET verified = 0 WHERE id = ?', (_id,))
        self.conn.commit()
        


if __name__ == "__main__":
    VW_TEST = VWBackend()
    VW_TEST.load_xls()
    print(VW_TEST.get_min_id())
    print(VW_TEST.getvalues_with_id(5))