"""m.java - the drawing of Gamevil Live (PHASE_7) and its registration record. Literal port.

as.a = m(); ag.L() calls as.aK() -> m.a() every frame while bV == 11. as.ho picks the screen.
"""
from pow.game.ag import ag
from pow.game.as_ import as_, B5
from pow.game.x import x
from pow.midp.rms import RecordStore


class m(as_):

    def a_v(self):  # m.java:4-56
        if as_.hq:
            ag.bb.e_v()
            if as_.hn is not None:
                x.a_Lg(ag.bu)
                ag.b_IIT(ag.bJ // 2, 2, as_.hn)
            as_.hq = False
        h = {1: self.bj_v, 2: self.bk_v, 3: self.bu_v, 4: self.bv_v, 5: self.bq_v, 6: self.br_v,
             7: self.bs_v, 8: self.bt_v, 9: self.bl_v, 10: self.bm_v, 11: self.bn_v, 12: m.bo_v,
             13: self.bp_v}.get(as_.ho)
        if h is not None:
            h()
        if ag.cS.b != 0:
            ag.cS.c_v()

    def bj_v(self):  # m.java:58-61  (list menu)
        self.aD_v()
        ag.h_II(-1, 2)

    def bk_v(self):  # m.java:63-77  (Safe: Local <-> Server)
        self.c_TI("Local", 85)
        self.c_II(ag.cz.E, 108)
        ag.a_IIIIMII(85, 138, 70, 21, ag.ct[7], 45, 138)
        if as_.ht[15] == 0:
            ag.a_IIIIMII(85, 138, 30, 21, as_.r, 0, 0)
            ag.a_IIIIMII(126, 139, 28, 19, as_.r, 30, 18)
        else:
            ag.a_IIIIMII(86, 139, 28, 19, as_.r, 30, 0)
            ag.a_IIIIMII(125, 138, 30, 21, as_.r, 0, 20)
        self.c_TI("Server", 167)
        self.c_II(as_.gy, 190)
        ag.h_II(-1, 2)

    def bl_v(self):  # m.java:79-101  (Sell: the price)
        from pow.game.e import e
        arrayOfString = ["Enter your selling", "price. " + str(as_.ht[4]) + "% of total", "will go to taxes."]
        str1 = "EnchantLv"
        b1 = 101
        x.a_Lg(ag.bu)
        for b2 in range(3):
            as_.a_TIII(arrayOfString[b2], 0, b1, 240)
            b1 += 13
        as_.a_IIIZ(as_.hi, 39, 180, False)
        self.c_IIII(71, 183, 130, 17)
        x.a_Lg(ag.bu)
        e.c_I(as_.hi)
        as_.a_TIII(str1 + str(as_.gR), 141, 180, 0)
        self.a_IIII(45, 210, 150, 22)
        x.a_Lg(ag.bv)
        as_.a_TIII(ag.n_I(as_.hv[14]), 0, 212, 240)
        ag.a_LzZI(ag.cz.Y[ag.fK[18]], True, -1)
        ag.dF.b.b = 155 - ag.dc
        ag.bb.k_v()
        ag.h_II(7, 2)

    def bm_v(self):  # m.java:103-120  (Cancel Sell: my 5 lots)
        from pow.game.e import e
        ag.h_II(-1, 2)
        self.i_I(83)
        i = 42
        for b in range(5):
            as_.a_IIIZ(as_.gz[b].a, i, 115, b == as_.hk)
            i += 32
        i = self.b_III(160, 200, 48)
        if as_.gz[as_.hk].a > 0:
            x.a_Lg(ag.bu)
            as_.a_TIII(e.c_I(as_.gz[as_.hk].a), i, 164, 200)
            as_.a_TIII("Price " + ag.n_I(as_.gB[as_.hk]), i, 178, 200)
            ag.a_LzZI(as_.gz[as_.hk], False, -1)

    def bn_v(self):  # m.java:122-148  (Sale List / Gift List)
        from pow.game.e import e
        arrayOfString1 = ["Listed Items", "has been sold."]
        arrayOfString2 = ["Listed Items", "has been recieved."]
        s = arrayOfString1[0] if as_.gD == 0 else arrayOfString2[0]
        x.a_Lg(ag.bu)
        as_.a_TIII(s, 0, 100, 240)
        s = arrayOfString1[1] if as_.gD == 0 else arrayOfString2[1]
        as_.a_TIII(s, 0, 113, 240)
        i = 42
        for b in range(5):
            as_.a_IIIZ(as_.gz[b].a, i, 130, b == as_.hk)
            i += 32
        i = self.b_III(166, 150, 45) + 25
        if as_.gz[as_.hk].a > 0:
            x.a_Lg(ag.bu)
            if as_.gD == 0:
                as_.a_TIII(e.c_I(as_.gz[as_.hk].a), i, 170, 100)
                as_.a_TIII("Price " + ag.n_I(as_.gB[as_.hk]), i, 183, 100)
                as_.a_TIII("EnchantLv " + str(as_.gz[as_.hk].f), i, 196, 100)
                return
            as_.a_TIII(as_.gC[as_.hk], i, 170, 100)
            as_.a_TIII(e.c_I(as_.gz[as_.hk].a), i, 183, 100)
            ag.a_LzZI(as_.gz[as_.hk], False, -1)
            ag.bb.k_v()

    @staticmethod
    def bo_v():  # m.java:150-156  (waiting: no answer for ~10 frames after the request -> "failed")
        if ag.cS.b == 0 and not as_.gu:
            as_.j += 1
            if as_.j - 1 > 10:
                as_.gt = 3
                ag.cS.d_I(29)
                as_.j = 0

    def bp_v(self):  # m.java:158-208  (registration: UserID, then the password)
        i = ag.bK // 2 - 45
        if as_.k == 0:
            x.a_Lg(ag.bu)
            x.a_TIII("Please enter", ag.bJ // 2, i, 1)
            x.a_TIII("your password.", ag.bJ // 2, i + 15, 1)
            x.a_TIII("(4-12 numbers)", ag.bJ // 2, i + 30, 1)
            x.b_IIIII(ag.bJ // 2 - 65, i + 65, 130, 20, 13421772)
            x.a_Lg(ag.bv)
            x.a_TIII(as_.l, ag.bJ // 2, i + 67, 1)
            if as_.gE and not (B5 and as_.gu):     # ORIG-BUG B5: not while the 530 is on its way
                as_.i += 1
                if as_.i - 1 > 2:
                    as_.k = 1
                    ag.cS.d_I(29)
                    as_.i = 0
                    as_.gE = False
            self.a_MIIIIII(ag.ct[7], 0, ag.bK - 20, ag.bJ, 20, 0, ag.bK - 20)
            b1 = 2
            if len(as_.l) > 0:
                b1 = 10
            if len(as_.l) >= 4:
                ag.h_II(8, b1)
                return
            ag.h_II(-1, b1)
        elif as_.k == 1:
            if ag.cS.b == 0:
                as_.gE = False
                x.a_Lg(ag.bu)
                x.a_TIII("In order to access", ag.bJ // 2, i - 30, 1)
                x.a_TIII("Gamevil Live", ag.bJ // 2, i - 10, 1)
                x.a_TIII("you must register first.", ag.bJ // 2, i + 10, 1)
                x.a_TIII("Please enter a UserID.", ag.bJ // 2, i + 30, 1)
                x.a_TIII("(4-12 characters)", ag.bJ // 2, i + 50, 1)
                x.b_IIIII(ag.bJ // 2 - 60, i + 70, 120, 20, 13421772)
                x.a_Lg(ag.bv)
                x.a_TIII(ag.bz.a_v(), ag.bJ // 2, i + 72, 1)
                ag.f_II(ag.bP, i + 90)
            self.a_MIIIIII(ag.ct[7], 0, ag.bK - 20, ag.bJ, 20, 0, ag.bK - 20)
            j = ag.bz.b_v()
            bool_ = 1                        # sic: (j >= 4 && j <= 12) ? true : true
            b2 = 2 if j == 0 else 10
            ag.h_II(bool_, b2)

    def bq_v(self):  # m.java:210-213  (Buy: categories)
        self.i_I(as_.hv[15])
        self.bj_v()

    def br_v(self):  # m.java:215-224  (Buy: kinds)
        i = 20 + (255 - 64 + ag.fK[6] >> 1)
        self.i_I(i)
        i += 32
        self.c_TI(as_.hw[as_.gP], i)
        i += 32
        ag.bb.a_IAzAI(i, None, as_.gF[as_.gP])
        ag.h_II(-1, 2)

    def bs_v(self):  # m.java:226-254  (Buy: how many lots at each enchant level)
        i_ = 0
        self.i_I(47)
        i = self.b_III(89, 200, 32)
        x.a_Lg(ag.bu)
        as_.a_TIII(as_.hw[as_.gP], i, 99, 167)
        as_.a_IIIZ(as_.gF[as_.gP][as_.gQ], i + 167, 91, False)
        j = 131
        b2 = 0
        for b1 in range(2):
            i = 32
            for b in range(5):
                as_.a_IIIZ(0, i, j, b2 == as_.gR)
                x.a_MIII(as_.s, i + 1, j + 8, 0)
                self.h_III(b2, i + 27, j + 6)
                as_.a_IIIZ(0, i, j + 28 + 1, b2 == as_.gR)
                self.h_III(as_.hu[15 - b2] // 10, i + 13, j + 28 + 8)
                self.h_III(as_.hu[15 - b2] % 10, i + 22, j + 28 + 8)
                i += 37
                b2 += 1
            j += 60
        del i_
        ag.h_II(-1, 2)

    def bt_v(self):  # m.java:256-276  (Buy: the lots of a page)
        j = 20 + (255 - 84 + ag.fK[6] + 10 + 32 >> 1)
        self.i_I(j)
        j += 42
        i = self.b_III(j, 200, 32)
        x.a_Lg(ag.bu)
        as_.a_TIII(as_.hw[as_.gP], i, j + 10, 157)
        i += 157
        as_.a_IIIZ(as_.hi, i - 15, j + 9 - 7, False)
        if as_.gP != 2:
            x.a_MIII(as_.s, i + 28 - 14, j + 11, 0)
            self.h_III(as_.gR, i + 28 + 14, j + 9)
        j += 42
        ag.bb.a_IAzAI(j, as_.gz, None)
        ag.fK[14] = 1
        ag.a_LzZI(as_.gz[ag.fK[18]], True, as_.gB[ag.fK[18]])
        ag.bb.k_v()
        ag.h_II(-1, 2)

    @staticmethod
    def b_v():  # m.java:278-285  (registered already?)
        try:
            rs = RecordStore.openRecordStore("gamevil_pow_regist", True)
            return not (rs.getNumRecords() == 0)
        except Exception:
            return False

    @staticmethod
    def c_v():  # m.java:287-305  (keep UserID [0..12) and password [12..28))
        arrayOfByte1 = bytearray(28)
        arrayOfByte2 = as_.l.encode("latin-1")
        for b in range(len(arrayOfByte2)):
            arrayOfByte1[b] = arrayOfByte2[b]
        arrayOfByte2 = as_.m.encode("latin-1")
        for b in range(len(arrayOfByte2)):
            arrayOfByte1[12 + b] = arrayOfByte2[b]
        try:
            rs = RecordStore.openRecordStore("gamevil_pow_regist", True)
            if rs.getNumRecords() == 0:
                rs.addRecord(bytes(arrayOfByte1), 0, len(arrayOfByte1))
            rs.setRecord(1, bytes(arrayOfByte1), 0, len(arrayOfByte1))
        except Exception:
            return

    def d_v(self):  # m.java:307-320  (read it back: l = [0..12), m = [12..26))
        arrayOfByte = bytes(26)
        try:
            rs = RecordStore.openRecordStore("gamevil_pow_regist", False)
            if rs is None or rs.getNumRecords() < 1:
                as_.l = ""
                as_.m = ""
                return
            arrayOfByte = rs.getRecord(1)
        except Exception:
            pass
        as_.l = ag.f_T(ag.a_ABII(arrayOfByte, 0, 12))
        as_.m = ag.f_T(ag.a_ABII(arrayOfByte, 12, 26))

    def bu_v(self):  # m.java:322-341  (Safe: the amount)
        if ag.ct[22] is None:
            ag.ct[22] = self.d_T(ag.bA.a_I(18))
        if ag.ct[24] is None:
            ag.ct[24] = self.d_T(ag.bA.a_I(20))
        if as_.ht[15] == 0:
            x.a_MII(ag.ct[22], 107, 111)
        else:
            x.a_MII(ag.ct[24], 107, 111)
        x.a_Lg(ag.bu)
        x.a_TIII("Local", ag.bJ // 2 - 44, 111, 1)
        x.a_TIII("Server", ag.bJ // 2 + 50, 111, 1)
        x.a_TIII("How much do", ag.bJ // 2, 131, 1)
        x.a_TIII("you want to move?", ag.bJ // 2, 143, 1)
        self.a_IIII(70, 163, 100, 20)
        x.a_Lg(ag.bv)
        x.a_TIII(ag.n_I(as_.hv[14]), ag.bJ // 2, 165, 1)
        ag.h_II(-1, 2)
        ag.cS.c_I(200)

    def a_IIII(self, paramInt1, paramInt2, paramInt3, paramInt4):  # m.java:343-356  (input box)
        ag.bo.c = paramInt3 + 1
        ag.bo.a = paramInt1 - 1
        ag.bo.d = paramInt4 + 1
        ag.bo.b = paramInt2 - 1
        ag.b_LacI(ag.bo, 0)
        ag.bo.a += 1
        ag.bo.b += 1
        ag.b_LacI(ag.bo, 16777215)
        ag.bo.c -= 1
        ag.bo.d -= 1
        ag.a_LacI(ag.bo, ag.k_III(192, 192, 192))

    def bv_v(self):  # m.java:358-380  (Backpack / Warehouse grid)
        if as_.ht[7] == 0:
            s = "Backpack"
            arrayOfZ = ag.cz.Y
        else:
            s = "Warehouse"
            arrayOfZ = as_.gw
        i = 20 + (255 - 38 + ag.fK[6] + 16 + 22 >> 1)
        self.c_TI(s, i)
        i += 38
        ag.bb.a_IAzAI(i, arrayOfZ, None)
        ag.fK[14] = 0
        ag.a_LzZI(arrayOfZ[ag.fK[18]], True, -1)
        ag.bb.k_v()
        if as_.ht[7] == 0:
            ag.h_II(4, 2)
            return
        ag.h_II(3, 2)
