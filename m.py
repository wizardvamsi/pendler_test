import creds
base_fare = creds.base_fare
tim_fare_permin = creds.tim_fare_permin
Drop_dist = creds.Drop_dist
Drop_tim = creds.Drop_tim
max_drp_time = creds.max_drp_time
max_drp_time_permin = creds.max_drp_time_permin
ref_perc = creds.ref_perc
DF1_per = creds.DF1_per
DF2_per = creds.DF2_per
DF3_per = creds.DF3_per
DF4_per = creds.DF4_per
DF5_per = creds.DF5_per
Tax_GST_perc = creds.Tax_GST_perc
peak_tperc = creds.peak_tperc
peak_time = creds.peak_time
delay_time = creds.delay_time
lpf_per = creds.lpf_per
pickup_dist = creds.pickup_dist
pck_crg_permin = creds.pck_crg_permin
pck_limit_cap = creds.pck_limit_cap

peak_frac = float(peak_tperc)/100


def get_fare1():

    tim_fare = float(Drop_tim)*float(tim_fare_permin)

    if 0 < Drop_dist < 2:
        DF1 = DF2 = DF3 = DF4 = DF5 = 0
        if 0 < Drop_tim < float(max_drp_time):
            tim_fare = 0
        elif Drop_tim > float(max_drp_time):
            tim_fare = (float(Drop_tim) - float(max_drp_time)) * \
                float(max_drp_time_permin)

    print("time fare - ", tim_fare)

    if 2 < Drop_dist < 4:
        DF1 = 2*float(DF1_per)
        DF2 = (float(Drop_dist)-2)*float(DF2_per)
        DF3 = DF4 = DF5 = 0

    if 4 < Drop_dist < 6:
        DF1 = 2*float(DF1_per)
        DF2 = 2*float(DF2_per)
        DF3 = (float(Drop_dist)-4)*float(DF3_per)
        DF4 = DF5 = 0

    if 6 < Drop_dist < 10:
        DF1 = 2*float(DF1_per)
        DF2 = 2*float(DF2_per)
        DF3 = 2*float(DF3_per)
        DF4 = (float(Drop_dist)-6)*float(DF4_per)
        DF5 = 0

    if 10 < Drop_dist < 200:
        DF1 = 2*float(DF1_per)
        DF2 = 2*float(DF2_per)
        DF3 = 2*float(DF3_per)
        DF4 = 4*float(DF4_per)
        DF5 = (float(Drop_dist)-10)*float(DF5_per)

    TDF = DF1 + DF2 + DF3 + DF4 + DF5

    if pickup_dist > 3:
        pckup_crg = (float(pickup_dist)-float(pck_limit_cap)) * \
            float(pck_crg_permin)
    else:
        pckup_crg = 0

    Sub_TF = float(base_fare) + float(tim_fare) + float(TDF) + \
        float(pckup_crg)

    if peak_time == True:
        peak_crg = float(Sub_TF)*float(peak_frac)
    else:
        peak_crg = 0

    ref_frac = float(ref_perc)/100
    Ref_crg = float(ref_frac)*float(Sub_TF)

    Tax_GST_Frac = float(Tax_GST_perc)/100
    Tax_GST = float(Tax_GST_Frac)*(float(Sub_TF) +
                                   float(Ref_crg) + float(peak_crg))

    Tol_Fare = round(float(Sub_TF) + float(Ref_crg) +
                     float(Tax_GST) + float(peak_crg))

    DE = float(Tol_Fare) - float(Ref_crg) - float(Tax_GST)
    print("drop distance -", Drop_dist)
    print("drop time -", Drop_tim)
    print("DF1- ", DF1)
    print("DF2 - ", DF2)
    print("DF3 - ", DF3)
    print("DF4 - ", DF4)
    print("DF5 - ", DF5)
    print("TDF - ", TDF)
    print("pickup charges - ", pckup_crg)
    print("sub total - ", Sub_TF)
    print("peak charges - ", peak_crg)
    print("referral charge -", Ref_crg)
    print("GST -", Tax_GST)
    print("estimated total fare - ", Tol_Fare)
    print("estimated driver earning - ", DE)
    return Sub_TF, peak_crg, Ref_crg


def final_fare():
    fare_charge = list(get_fare1())

    sub_tf1 = fare_charge[0]
    peak_crg1 = fare_charge[1]
    Ref_crg1 = fare_charge[2]

    delay_time_round = round(float(delay_time)/60)
    del_crg = float(delay_time_round)*float(lpf_per)
    print("delay charges -", del_crg)

    Tax_GST_Frac = float(Tax_GST_perc)/100
    Tax_GST1 = float(Tax_GST_Frac)*(float(sub_tf1) +
                                    float(Ref_crg1) + float(peak_crg1) + float(del_crg))

    fin_fare = round(float(sub_tf1) + float(Ref_crg1) +
                     float(Tax_GST1) + float(peak_crg1) + float(del_crg))
    FDE = float(fin_fare) - float(Ref_crg1) - float(Tax_GST1)

    print("actual GST -", Tax_GST1)
    print("final total fare - ", fin_fare)
    print("final driver earning - ", FDE)


final_fare()
