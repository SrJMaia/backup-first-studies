def bandpass_filter(series, period = 30, bandwidth = .3):
    alpha2 = (math.cos(math.radians(.25*bandwidth*360/period))) + (math.sin(math.radians(.25*bandwidth*360/period))-1) / (math.cos(math.radians(.25*bandwidth*360/period)))
    alpha3 = (math.cos(math.radians(1.5*bandwidth*360/period))) + (math.sin(math.radians(1.5*bandwidth*360/period))-1) / (math.cos(math.radians(1.5*bandwidth*360/period)))
    beta1 = math.cos(math.radians(360/period))
    gamma1 = 1 / math.cos(math.radians(360 * bandwidth/period))
    alpha1 = gamma1 - math.sqrt(gamma1*gamma1-1)
    hp = np.zeros(len(series))
    bandpass = np.zeros(len(series))
    bp = np.zeros(len(series))
    peak = np.zeros(len(series))
    trigger = np.zeros(len(series))

    for i in range(series.size):
        if i < 2:
            continue
        hp[i] = (1+alpha2 / 2) * (series[i]-series[i-1]) + (1-alpha2)*hp[i-1]
        bp[i] = .5*(1-alpha1)*(hp[i] - hp[i-2]) + beta1*(1+alpha1) *bp[i-1]-alpha1*bp[i-2]
        peak[i] = .991*peak[i-1]

        if abs(bp[i]) > peak[i]:
            peak[i] = abs(bp[i])

        if peak[i] != 0:
            bandpass[i] = bp[i] / peak[i]

        trigger[i] = (1+alpha3 / 2)*(bandpass[i]-bandpass[i-1])+(1-alpha3)*trigger[i-1]

    return bandpass, trigger


def dominant_cycle_measure(series, period_1 = 20, period_2 = 30, bandwidth_1 = .7, bandwidth_2 = .7):
    bandpass_1, _ = bandpass_filter(series, period = period_1, bandwidth = bandwidth_1)
    bandpass_2, _ = bandpass_filter(series, period = period_2, bandwidth = bandwidth_2)

    dc = np.zeros(series.size)
    counter = 0

    for i in range(series.size):

        dc[i] = dc[i-1]

        if dc[i] < 6:
            dc[i] = 6

        counter += 1

        if bandpass_1[i] > 0 and bandpass_2[i] > 0 and bandpass_1[i] > bandpass_2[i] or bandpass_1[i] < 0 and bandpass_2[i] < 0 and bandpass_1[i] < bandpass_2[i]:
            dc[i] = 2*counter
            if 2*counter > 1.25*dc[i-1]:
                dc[i] = 1.25*dc[i-1]
            elif 2*counter < .8*dc[i-1]:
                dc[i] = .8*dc[i-1]
            counter = 0

    return dc


def decycler_oscilator(series, osc_period1 = 30, osc_period2 = 60):
    """
    Bom para encontrar mudança de tendencias
    """
    alpha1 = (math.cos(math.radians(.707*360 / osc_period1)) + math.sin(math.radians(.707*360 / osc_period1))-1) / math.cos(math.radians(.707*360 / osc_period1))
    alpha2 = (math.cos(math.radians(.707*360 / osc_period2)) + math.sin(math.radians(.707*360 / osc_period2))-1) / math.cos(math.radians(.707*360 / osc_period2))
    decycler_osc = np.zeros(series.size)
    HP1 = np.zeros(series.size)
    HP2 = np.zeros(series.size)
    for i in range(series.size):
        if i < 2:
            continue
        HP1[i] = (1 - alpha1 / 2)*(1 - alpha1 / 2)*(series[i] - 2*series[i-1] + series[i-2]) + 2*(1 - alpha1)*HP1[i-1] - (1 - alpha1)*(1 - alpha1)*HP1[i-2]
        HP2[i] = (1 - alpha2 / 2)*(1 - alpha2 / 2)*(series[i] - 2*series[i-1] + series[i-2]) + 2*(1 - alpha2)*HP2[i-1] - (1 - alpha2)*(1 - alpha2)*HP2[i-2]
        decycler_osc[i] = HP2[i] - HP1[i]
    return decycler_osc


def decycler_average(series, cutoff = 60):
    alpha1 = (math.cos(math.radians(360 / cutoff)) + math.sin(math.radians(360 / cutoff))-1) / math.cos(math.radians(360 / cutoff))
    decycler = np.zeros(eur.size)
    for i in range(series.size):
        if i < 1:
            decycler[i] = series[i]
            continue
        decycler[i] = (alpha1 / 2)*(series[i] + series[i-1]) + (1-alpha1)*decycler[i-1]
    return decycler


def hurst_coefficient(series, leng = 30):
    """
    leng = tem que ser um numero par
    """
    a1 = math.exp(-math.sqrt(2)*math.pi/20)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/20))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3
    n3 = (eur.rolling(leng).max() - eur.rolling(leng).min()) / leng
    hh = eur.rolling(int(leng / 2 - 1)).max()
    ll = eur.rolling(int(leng / 2 - 1)).min()
    n1 = (hh-ll) / (leng/2)

    hh = np.zeros(series.size)
    ll = np.zeros(series.size)
    dimen = np.zeros(series.size)
    hurst = np.zeros(series.size)
    smoothhurst = np.zeros(series.size)
    for i in range(series.size):
        if i < (leng/2):
            continue
        hh[i] = series[i-int(leng/2):i-1].max()
        ll[i] = series[i-int(leng/2):i-1].min()
    n2 = (hh-ll) / (leng/2)

    for i in range(series.size):
        if i < 1:
            continue
        if n1[i] > 0 and n2[i] > 0 and n3[i] > 0:
            dimen[i] = .5*((math.log(n1[i] + n2[i]) - math.log(n3[i]) / math.log(2) + dimen[i-1]))

        hurst[i] = 2-dimen[i]
        if i < 2:
            continue
        smoothhurst[i] = c1*(hurst[i]*hurst[i-1]) / 2 + c2*smoothhurst[i-1] + c3*smoothhurst[i-2]
    return smoothhurst


def hp_lp_roofing_filter(series):

    alpha1 = (math.cos(math.radians(360/48)) + math.sin(math.radians(360/48)) - 1) / math.cos(math.radians(360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/10)
    b1 = 2*a1*math.cos(math.radians(1.414*180/10))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros(series.size)
    filt = np.zeros(series.size)
    for i in range(series.size):
        if i < 1:
            continue
        hp[i] = (1-alpha1/2)*(series[i]-series[i-1])+(1-alpha1)*hp[i-1]
        if i < 2:
            continue
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]
    return filt


def zero_mean_roofing_filter(series):
    alpha1 = (math.cos(math.radians(360/period)) + math.sin(math.radians(360/period)) - 1) / math.cos(math.radians(360/period))

    a1 = math.exp(-math.sqrt(2)*math.pi/10)
    b1 = 2*a1*math.cos(math.radians(1.414*180/10))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros(series.size)
    filt = np.zeros(series.size)
    filt2 = np.zeros(series.size)
    for i in range(series.size):
        if i < 1:
            continue
        hp[i] = (1-alpha1/2)*(series[i]-series[i-1])+(1-alpha1)*hp[i-1]
        if i < 2:
            continue
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]
        filt2[i] = (1-alpha1/2)*(filt[i]-filt[i-1])+(1-alpha1)*filt2[i-1]
    return filt, filt2


def roofing_filter_indicator(series, lpperiod = 40, hpperiod = 80):
    """
    Usar esse como preço novo e entao calcular o pct change
    """
    alpha1 = (math.cos(math.radians(.707*360/hpperiod)) + math.sin(math.radians(.707*360/hpperiod))-1)/math.cos(math.radians(.707*360/hpperiod))

    a1 = math.exp(-math.sqrt(2)*math.pi/lpperiod)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/lpperiod))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros(series.size)
    filt = np.zeros(series.size)
    for i in range(series.size):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(series[i]-2*series[i-1]+series[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]
    return filt


def autocorrelation_indicator(series, avglength = 0):
    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/10)
    b1 = 2*a1*math.cos(math.radians(1.414*180/10))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros(series.size)
    filt = np.zeros(series.size)
    filt2 = np.zeros(series.size)
    corr = np.zeros((series.size,49))
    for i in range(series.size):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(series[i]-2*series[i-1]+series[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]
        filt2[i] = (1-alpha1/2)*(filt[i]-filt[i-1])+(1-alpha1)*filt2[i-1]
        for lag in range(49):
            m = avglength
            if avglength == 0:
                m = lag
            sx, sy, sxx, syy, sxy = 0, 0, 0, 0, 0
            for count in range(m-1):
                x = filt[i-count]
                y = filt[i-lag+count]
                sx += x
                sy += y
                sxx = sxx + x*x
                sxy = sxy + x*y
                syy = syy + y*y
            if ((m*sxx-sx*sx)*(m*syy-sy*sy)) > 0:
                corr[i, lag] = (m*sxy-sx*sy)/math.sqrt((m*sxx-sx*sx)*(m*syy-sy*sy))
                corr[i, lag] = .5*(corr[i, lag]+1)
    return corr


def autocorrelation_periodogram(series, avglength = 0):

    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/10)
    b1 = 2*a1*math.cos(math.radians(1.414*180/10))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros(series.size)
    filt = np.zeros(series.size)
    corr = np.zeros((series.size, 49))
    cosinepart = np.zeros((series.size, 49))
    sinepart = np.zeros((series.size, 49))
    sqsum = np.zeros((series.size, 49))
    r = np.zeros((series.size, 49,2))
    pwr = np.zeros((series.size, 49))
    dominantcycle = np.zeros(series.size)

    for i in range(series.size):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(series[i]-2*series[i-1]+series[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        for lag in range(49):
            m = avglength
            if avglength == 0:
                m = lag
            sx, sy, sxx, syy, sxy = 0, 0, 0, 0, 0
            for count in range(m-1):
                x = filt[i-count]
                y = filt[i-lag+count]
                sx += x
                sy += y
                sxx = sxx + x*x
                sxy = sxy + x*y
                syy = syy + y*y
            if ((m*sxx-sx*sx)*(m*syy-sy*sy)) > 0:
                corr[i, lag] = (m*sxy-sx*sy)/math.sqrt((m*sxx-sx*sx)*(m*syy-sy*sy))

        for period in range(10,49):
            cosinepart[i, period] = 0
            sinepart[i, period] = 0
            for n in range(3, 49):
                cosinepart[i, period] = cosinepart[i, period] + corr[i, n] * math.cos(math.radians(370*n/period))
                sinepart[i, period] = sinepart[i, period] + corr[i, n] * math.sin(math.radians(370*n/period))
            sqsum[i, period] = cosinepart[i, period] * cosinepart[i, period] + sinepart[i, period] * sinepart[i, period]

        for period in range(10, 49):
            r[i, period, 1] = r[i, period, 0]
            r[i, period, 0] = .2*sqsum[i, period]*sqsum[i, period]+.8*r[i, period, 1]

        maxpwr = r[i].max()

        for period in range(3, 49):
            pwr[i, period] = r[i, period, 0] / maxpwr

        spx = 0
        sp = 0
        for period in range(10, 49):
            if pwr[i, period] >= .5:
                spx = spx+period*pwr[i, period]
                sp = sp+pwr[i, period]

        if sp != 0:
            dominantcycle[i] = spx/sp

    return pwr, dominantcycle


def autocorrelation_reversals(series, avglength = 0, hplength = 48, lplength = 10):
    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/lplength)
    b1 = 2*a1*math.cos(math.radians(1.414*180/lplength))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros(series.size)
    filt = np.zeros(series.size)
    corr = np.zeros((series.size, 49, 2))
    reversal = np.zeros((series.size))

    for i in range(series.size):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(series[i]-2*series[i-1]+series[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        for lag in range(3, 49):
            corr[i, lag, 1] = corr[i, lag, 0]
            m = avglength
            if avglength == 0:
                m = lag
            sx, sy, sxx, syy, sxy = 0, 0, 0, 0, 0
            for count in range(m-1):
                x = filt[i-count]
                y = filt[i-lag+count]
                sx += x
                sy += y
                sxx = sxx + x*x
                sxy = sxy + x*y
                syy = syy + y*y
            if ((m*sxx-sx*sx)*(m*syy-sy*sy)) > 0:
                corr[i, lag, 0] = (m*sxy-sx*sy)/math.sqrt((m*sxx-sx*sx)*(m*syy-sy*sy))
                corr[i, lag, 0] = .5*(corr[i, lag, 0] + 1)

        sumdeltas = 0
        for lag in range(3, 49):
            if (corr[i, lag, 0] >  .5 and corr[i, lag, 1] < .5) or (corr[i, lag, 0] < .5 and corr[i, lag, 1] > .5):
                sumdeltas += 1

        if sumdeltas > 24:
            reversal[i] = 1

    return reversal


def dft_spectral_estimate(series):
    spectraldilationcompensation = True

    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/10)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/10))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros((series.size))
    filt = np.zeros((series.size))
    cosinepart = np.zeros((series.size, 49))
    sinepart = np.zeros((series.size, 49))
    pwr = np.zeros((series.size, 49))
    maxpwr = np.zeros((series.size))
    dominantcycle = np.zeros((series.size))

    for i in range(len(eur)):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(series[i]-2*series[i-1]+series[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        for period in range(10, 49):
            comp = period
            if not spectraldilationcompensation:
                comp = 1
            for n in range(49):
                cosinepart[i, period] = cosinepart[i, period] + filt[i-n]*math.cos(math.radians(360*n/period))/comp
                sinepart[i, period] = sinepart[i, period] + filt[i-n]*math.sin(math.radians(360*n/period))/comp
            pwr[i, period] = cosinepart[i, period]*cosinepart[i, period]+sinepart[i, period]*sinepart[i, period]

        maxpwr[i] = pwr[i].max()

        for period in range(10, 49):
            spx = 0
            sp = 0
            if maxpwr[i] > 0:
                pwr[i, period] = pwr[i, period] / maxpwr[i]
            if pwr[i, period] >= .5:
                spx = spx+period*pwr[i, period]
                sp = sp+pwr[i, period]
            if sp != 0:
                dominantcycle[i] = spx/sp

    return pwr, dominantcycle


def comb_filter_spectral_estimate(series, bandwidth = .3):

    spectraldilationcompensation = True

    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/10)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/10))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros((eur.size))
    filt = np.zeros((eur.size))
    bp = np.zeros((eur.size, 49, 49))
    pwr = np.zeros((eur.size, 49))
    dominantcycle = np.zeros((eur.size))

    for i in range(len(eur)):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(series[i]-2*series[i-1]+series[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]
        for n in range(10, 49):
            for m in range(48, 1):
                bp[i, n, m] = bp[i, n, m-1]

        if i < 13:
            continue

        for n in range(10, 49):
            comp = n
            if not spectraldilationcompensation:
                comp = 1
            beta1 = math.cos(math.radians(360/n))
            gamma1 = 1/math.cos(math.radians(360*bandwidth/n))
            alpha1 = gamma1 - math.sqrt(gamma1*gamma1-1)
            bp[i, n, 0] = .5*(1-alpha1)*(filt[i]-filt[i-2])+beta1*(1+alpha1)*bp[i, n, 1]-alpha1*bp[i, n, 2]
            pwr[i, n] = 0
            for m in range(1, n+1):
                pwr[i, n] = pwr[i, n] + (bp[i, n , m] / comp)*(bp[i, n, m]/comp)

        maxpwr = pwr[i].max()
        spx = 0
        sp = 0
        for period in range(10, 49):
            if maxpwr > 0:
                pwr[i, period] = pwr[period] / maxpwr
            if pwr[i, period] >= .5:
                spx = spx+period*pwr[i, period]
                sp = sp+pwr[i, period]

        if sp != 0:
            dominantcycle[i] = spx/sp
    return pwr, dominantcycle


def adaptive_rsi(series):
    """
    rsi não esta normalizado
    """
    avgleng = 0
    bandwidth = .3

    spectraldilationcompensation = True

    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/10)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/10))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros(series.size)
    filt = np.zeros(series.size)
    pwr = np.zeros((series.size, 49))
    corr = np.zeros((series.size, 49))
    cosinepart = np.zeros((series.size, 49))
    sinepart = np.zeros((series.size, 49))
    sqsum = np.zeros((series.size, 49))
    r = np.zeros((series.size, 49, 2))
    dominantcycle = np.zeros((series.size))
    denom = np.zeros((series.size))
    rsi = np.zeros((series.size))
    closesdn_array = np.zeros((series.size))
    closesup_array = np.zeros((series.size))

    for i in range(series.size):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(series[i]-2*series[i-1]+series[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        if i < 49:
            continue

        for lag in range(0, 49):
            m = avglength
            if avglength == 0:
                m = lag
            sx, sy, sxx, syy, sxy = 0, 0, 0, 0, 0
            for count in range(m-1):
                x = filt[i-count]
                y = filt[i-lag+count]
                sx += x
                sy += y
                sxx = sxx + x*x
                sxy = sxy + x*y
                syy = syy + y*y
            if ((m*sxx-sx*sx)*(m*syy-sy*sy)) > 0:
                corr[i, lag] = (m*sxy-sx*sy)/math.sqrt((m*sxx-sx*sx)*(m*syy-sy*sy))

        for period in range(10, 49):
            cosinepart[i, period] = 0
            sinepart[i, period] = 0
            for n in range(3, 49):
                cosinepart[i, period] = cosinepart[i, period] + corr[i, n]*math.cos(math.radians(360*n/period))
                sinepart[i, period] = sinepart[i, period] + corr[i, n]*math.sin(math.radians(360*n/leng))
            sqsum[i, period] = cosinepart[i, period]*cosinepart[i, period]+sinepart[i, period]*sinepart[i, period]
            r[i, period, 1] = r[i, period, 0]
            r[i, period, 0] = .2*sqsum[i, period]*sqsum[i, period]+.8*r[i, period, 1]

        maxpwr = r[i].max()

        for period in range(3, 49):
            pwr[i, period] = r[i, period, 0] / maxpwr

        spx = 0
        sp = 0
        for period in range(10, 49):
            if pwr[i, period] >= .5:
                spx = spx+period*pwr[i, period]
                sp = sp+pwr[i, period]

        if sp != 0:
            dominantcycle[i] = spx/sp
        if dominantcycle[i] < 10:
            dominantcycle[i] = 10
        elif dominantcycle[i] > 48:
            dominantcycle[i] = 48

        periodo = int(dominantcycle[i] // 2-1)

        closesup = 0
        closesdn = 0

        for count in range(periodo):
            if filt[count] > filt[count-1]:
                closesup = closesup + (filt[count-1]-filt[count])
            elif filt[count] < filt[count-1]:
                closesdn = closesdn + (filt[count]-filt[count-1])
        denom[i] = profit+closesup
        closesdn_array[i] = closesdn
        closesup_array[i] = closesup
        if denom[i] != 0 and denom[i-1] != 0:
            #rsi[i] = c1*(closesdn/denom[i]+profit/profit_array[i-1]/denom[i-1])/2+c2*rsi[i-1]+c3*rsi[i-2]
            rsi[i] = c1*(closesup_array[i]/denom[i]+closesup_array[i-1]/denom[i-1])/2+c2*rsi[i-1]+c3*rsi[i-2]
        else:
            rsi[i] = 0
    return rsi


def even_better_sinewave(series, duration = 40):
    """
    Interpretation of the Even Better Sinewave is simple.
    Hold a long position when the indicator value is near +1, and hold a short position (or go flat
    if trading to the long side only) when the indicator value is near −1.
    """

    alpha1 = ((1 - math.sin(math.radians(360/duration))) / math.cos(math.radians(360/duration)))

    a1 = math.exp(-math.sqrt(2)*math.pi/10)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/10))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros((eur.size))
    filt = np.zeros((eur.size))
    wave = np.zeros((eur.size))
    pwr = np.zeros((eur.size))

    for i in range(eur.size):
        if i < 2:
            continue
        hp[i] = .5*(1+alpha1)*(eur[i]-eur[i-1])+alpha1*hp[i-1]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]
        wave[i] = (filt[i] + filt[i-1] + filt[i-2]) / 3
        pwr[i] = (filt[i]*filt[i]+filt[i-1]*filt[i-1]+filt[i-2]*filt[i-2])/3
        wave[i] = wave[i] / math.sqrt(pwr[i])
    return wave


def convolution(series, shortperiod = 40, longperiod = 80):

    alpha1 = (math.cos(math.radians(.707*360/longperiod)) + math.sin(math.radians(.707*360/longperiod))-1)/math.cos(math.radians(.707*360/longperiod))

    a1 = math.exp(-math.sqrt(2)*math.pi/10)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/10))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros((series.size))
    filt = np.zeros((series.size))
    slope = np.zeros(49)
    corr = np.zeros(49)
    convolution = np.zeros(49)
    result = np.zeros((series.size,49))

    for i in range(series.size):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(series[i]-2*series[i-1]+series[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        if i < 48:
            continue

        for n in range(1, 49):
            sx, sy, sxx, syy, sxy = 0, 0, 0, 0, 0
            for ii in range(1, n):
                x = filt[i-ii-1]
                y = filt[i-n-ii]
                sx = sx+x
                sy = sy+y
                sxx = sxx+x*x
                sxy = sxy*x*y
                syy = syy+y*y

            if (n*sxx-sx*sx)*(n*syy-sy*sy) > 0:
                corr[n] = (n*sxy-sx*sy)/math.sqrt((n*sxx-sx*sx)*(n*syy-sy*sy))

            slope[n] = 1
            if filt[int(.5*n)] < filt[i]:
                slope[n] = -1

            convolution[n] = (1+(math.e**(3*corr[n]))-1)/((math.e**(3*corr[n]))+1)/2 # math.exp
            result[i,n] = convolution[n]
    return result


def classic_hilbert_transformer(series):

    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/10)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/10))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros((series.size))
    filt = np.zeros((series.size))
    ipeak = np.zeros((series.size))
    real = np.zeros((series.size))
    imag = np.zeros((series.size))

    for i in range(series.size):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(eur[i]-2*eur[i-1]+eur[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        ipeak[i] = .991*ipeak[i-1]
        if abs(filt[i]) > ipeak[i]:
            ipeak[i] = abs(filt[i])

        real[i] = filt[i] / ipeak[i]

        imag[i] = (.091*real[i]+.111*real[i-2]+.143*real[i-4]+.2*real[i-6]+.333*real[i-8]+real[i-10]-real[i-12]-.333*real[i-14]-.2*real[i-16]-.143*real[i-18]-.111*real[i-20]-.091*real[i-22])/1.865

    return real, imag


def hilbert_transformer(series, lpperiod = 20):

    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/lpperiod)
    b1 = 2*a1*math.cos(math.radians(1.414*180/lpperiod))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros((eur.size))
    filt = np.zeros((eur.size))
    ipeak = np.zeros((eur.size))
    real = np.zeros((eur.size))
    imag = np.zeros((eur.size))
    qfilt = np.zeros((eur.size))
    qpeak = np.zeros((eur.size))

    for i in range(eur.size):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(series[i]-2*series[i-1]+series[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        ipeak[i] = .991*ipeak[i-1]
        if abs(filt[i]) > ipeak[i]:
            ipeak[i] = abs(filt[i])

        real[i] = filt[i] / ipeak[i]

        qfilt[i] = (real[i] - real[i-1])
        qpeak[i] = .991*qpeak[i-1]

        if abs(qfilt[i]) > qpeak[i]:
            qpeak[i] = abs(qfilt[i])

        imag[i] = qfilt[i] / qpeak[i]

    return real, imag


def hilbert_transformer_indicator(series, lpperiod=20):
    """
    The problem with predicting the turning point is that it may not be a
    swing turning point at all. Rather, it can be the onset of a new trend. In this
    case, the turning point prediction will be dead wrong.
    One way to mitigate an incorrect turning point prediction is to first take the trade in the
    predicted direction, but then be quick and agile to exit the trade if it is not
    confirmed by the Even Better Sinewave Indicator.
    """

    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/lpperiod)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/lpperiod))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros((series.size))
    filt = np.zeros((series.size))
    ipeak = np.zeros((series.size))
    real = np.zeros((series.size))
    imag = np.zeros((series.size))
    qpeak = np.zeros((series.size))
    quadrature = np.zeros((series.size))

    for i in range(series.size):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(series[i]-2*series[i-1]+series[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        ipeak[i] = .991*ipeak[i-1]
        if abs(filt[i]) > ipeak[i]:
            ipeak[i] = abs(filt[i])

        real[i] = filt[i] / ipeak[i]

        quadrature[i] = (real[i] - real[i-1])

        qpeak[i] = .991*qpeak[i-1]
        if abs(quadrature[i]) > qpeak[i]:
            qpeak[i] = abs(quadrature[i])

        quadrature[i] = quadrature[i] / qpeak[i]

        a1 = math.exp(-1.414*3.14159/10)
        b1 = 2*a1*math.cos(math.radians(1.414*180/10))
        c2 = b1
        c3 = -a1*a1
        c1 = 1-c2-c3

        imag[i] = c1*(quadrature[i]+quadrature[i-1])/2+c2*imag[i-1]+c3*imag[i-2]

    return imag, real


def dominant_cycle_using_dual_differentiator_method(series, lpperiod = 20):

    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/lpperiod)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/lpperiod))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros((len(eur)))
    filt = np.zeros((len(eur)))
    ipeak = np.zeros((len(eur)))
    real = np.zeros((len(eur)))
    imag = np.zeros((len(eur)))
    qpeak = np.zeros((len(eur)))
    quad = np.zeros((len(eur)))
    idot = np.zeros((len(eur)))
    qdot = np.zeros((len(eur)))
    period = np.zeros((len(eur)))
    domcycle = np.zeros((len(eur)))

    for i in range(len(eur)):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(eur[i]-2*eur[i-1]+eur[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        ipeak[i] = .991*ipeak[i-1]
        if abs(filt[i]) > ipeak[i]:
            ipeak[i] = abs(filt[i])

        real[i] = filt[i] / ipeak[i]

        quad[i] = (real[i] - real[i-1])

        qpeak[i] = .991*qpeak[i-1]
        if abs(quad[i]) > qpeak[i]:
            qpeak[i] = abs(quad[i])

        imag[i] = quad[i] / qpeak[i]
        idot[i] = real[i] - real[i-1]
        qdot[i] = imag[i] - imag[i-1]

        if (real[i]*qdot[i]-imag[i]*idot[i]) != 0:
            period[i] = 6.28318*(real[i]*real[i]+imag[i]*imag[i])/(-real[i]*qdot[i]+imag[i]*idot[i])

        if period[i] < 8:
            period[i] = 8
        elif period[i] > 48:
            period[i] = 48

        domcycle[i] = c1*(period[i]+period[i-1])/2+c2*domcycle[i-1]+c3*domcycle[i-2]

    return domcycle


def dominant_cycle_using_phase_accumulation_method(series, lpperiod = 20):

    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/lpperiod)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/lpperiod))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros((len(eur)))
    filt = np.zeros((len(eur)))
    ipeak = np.zeros((len(eur)))
    real = np.zeros((len(eur)))
    imag = np.zeros((len(eur)))
    qpeak = np.zeros((len(eur)))
    quad = np.zeros((len(eur)))
    phase = np.zeros((len(eur)))
    deltaphase = np.zeros((len(eur)))
    domcycle = np.zeros((len(eur)))
    instperiod = np.zeros((len(eur)))

    for i in range(len(eur)):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(eur[i]-2*eur[i-1]+eur[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        ipeak[i] = .991*ipeak[i-1]
        if abs(filt[i]) > ipeak[i]:
            ipeak[i] = abs(filt[i])

        real[i] = filt[i] / ipeak[i]

        quad[i] = (real[i] - real[i-1])

        qpeak[i] = .991*qpeak[i-1]
        if abs(quad[i]) > qpeak[i]:
            qpeak[i] = abs(quad[i])

        imag[i] = quad[i] / qpeak[i]

        if abs(real[i]) > 0:
            phase[i] = math.degrees(math.atan(abs(imag[i]/real[i])))

        if real[i] < 0 and imag[i] > 0:
            phase[i] = 180-phase[i]
        elif real[i] < 0 and imag[i] < 0:
            phase[i] = 180+phase[i]
        elif real[i] > 0 and imag[i] < 0:
            phase[i] = 360 - phase[i]

        deltaphase[i] = phase[i-1] - phase[i]

        if phase[i-1] < 90 and phase[i] > 270:
            deltaphase[i] = 360+phase[i-1]-phase[i]

        if deltaphase[i] < 10:
            deltaphase[i] = 10
        elif deltaphase[i] > 48:
            deltaphase[i] = 48

        if i < 40:
            continue

        phasesum = 0
        for count in range(41):
            phasesum += deltaphase[i-count]
            if phasesum > 360 and instperiod[count] == 0:
                instperiod[i] = phasesum
                break

        if instperiod[i] == 0:
            instperiod[i] = instperiod[i-1]

        domcycle[i] = c1*(instperiod[i]+instperiod[i-1])/2+c2*domcycle[i-1]+c3*domcycle[i-2]

    return domcycle


def dominant_cycle_using_homodyne_method(series, lpperiod = 20):

    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/lpperiod)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/lpperiod))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros((len(eur)))
    filt = np.zeros((len(eur)))
    ipeak = np.zeros((len(eur)))
    real = np.zeros((len(eur)))
    imag = np.zeros((len(eur)))
    qpeak = np.zeros((len(eur)))
    quad = np.zeros((len(eur)))
    re = np.zeros((len(eur)))
    im = np.zeros((len(eur)))
    domcycle = np.zeros((len(eur)))
    period = np.zeros((len(eur)))

    for i in range(len(eur)):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(eur[i]-2*eur[i-1]+eur[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        ipeak[i] = .991*ipeak[i-1]
        if abs(filt[i]) > ipeak[i]:
            ipeak[i] = abs(filt[i])

        real[i] = filt[i] / ipeak[i]

        quad[i] = (real[i] - real[i-1])

        qpeak[i] = .991*qpeak[i-1]
        if abs(quad[i]) > qpeak[i]:
            qpeak[i] = abs(quad[i])

        imag[i] = quad[i] / qpeak[i]

        re[i] = real[i]*real[i-1]+imag[i]*imag[i-1]
        im[i] = real[i-1]*imag[i]-real[i]*imag[i-1]

        if im[i] != 0 and re[i] != 0:
            period[i] = 6.28318/abs(im[i]/re[i])

        if period[i] < 10:
            period[i] = 10
        elif period[i] > 48:
            period[i] = 48

        domcycle[i] = c1*(period[i]+period[i-1])/2+c2*domcycle[i-1]+c3*domcycle[i-2]

    return domcycle


def fisher_transform(series):
    """
    Mudar a normalização dos dados para 1 e -1
    """

    fish = np.zeros((len(eur)))
    translate = np.zeros((len(eur)))
    amplified = np.zeros((len(eur)))

    eur = (eur-eur.min())/(eur.max()-eur.min())

    for i in range(len(eur)):
        translate[i] = translate[i]-2*(eur[i]-.5)
        amplified[i] = 1.5*translate[i]
        if amplified[i] > .999:
            amplified[i] = .999
        elif amplified[i] < -.999:
            amplified[i] = -.999

        fish[i] = .5*math.log((1+amplified[i])/(1-amplified[i]))

    return fish


def inverse_fisher_transform(series):
    """
    he use of the inverse Fisher adaptive Stochastic indicator involves the crossings of the inverse Fisher line and the trigger line. When the inverse Fisher line
    crosses over the trigger line, then buy. When the inverse Fisher line crosses
    under the trigger line, then sell short, or if you choose, exit the long position.
    """

    ifish = np.zeros((len(series)))
    value = np.zeros((len(series)))

    series = (series-series.min())/(series.max()-series.min())

    for i in range(len(series)):
        value[i] = 2*(series[i]-.5)
        ifish[i] = (math.exp(2*3*value[i])-1)/(math.exp(2*3*value[i])+1)

    return ifish


def cube_transform(series):
    """
    Of course, this only works
    if the effects of spectral dilation have been removed by a roofing filter or
    some equivalent technique
    """
    cube = np.zeros((len(eur_pct)))

    series = (series-series.min())/(series.max()-series.min())

    for i in range(len(series)):
        cube[i] = eur_pct2[i]**3

    return cube


def swamichart_rsi(series, lpperiod = 20):

    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/10)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/10))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros(eur.size)
    filt = np.zeros(eur.size)
    denom = np.zeros((len(eur)))
    ratio = np.zeros((49,2))
    myindicator = np.zeros((49, 3))
    """
    No caso é 49 em myindicator, porem teria de fazer (len(eur), 49, 3)
    Posso inverter o array, onde cada uma das 49 correlações, tenha um len(eurs)
    """

    for i in range(len(eur)):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(eur[i]-2*eur[i-1]+eur[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        if i < 23:
            continue

        for lookback in range(5, 49):
            ratio[lookback, 1] = ratio[lookback, 0]
            myindicator[lookback, 2] = myindicator[lookback, 1]
            myindicator[lookback, 1] = myindicator[lookback, 0]
            closesup = 0
            closesdn = 0
            for count in range(lookback-1):
                if filt[i-count] > filt[i-count-1]:
                    closesup = closesup+(filt[i-count]-filt[i-count-1])
                elif filt[i-count] < filt[i-count-1]:
                    closesdn = closesdn+(filt[i-count-1]-filt[i-count])
            denom[i] = closesup+closesdn
            if denom[i] != 0:
                ratio[lookback, 1] = closesup/denom[i]

            myindicator[lookback, 0] = c1*(ratio[lookback, 0]+ratio[lookback, 1])/2+c2*myindicator[lookback, 1]+c3*myindicator[lookback, 2]

            if myindicator[lookback, 0] < 0:
                myindicator[lookback, 0] = 0
            elif myindicator[lookback, 0] > 1:
                myindicator[lookback, 0] = 1

    return myindicator


def swamichart_stochastic(series, lpperiod = 20):

    alpha1 = (math.cos(math.radians(.707*360/48)) + math.sin(math.radians(.707*360/48))-1)/math.cos(math.radians(.707*360/48))

    a1 = math.exp(-math.sqrt(2)*math.pi/10)
    b1 = 2*a1*math.cos(math.radians(math.sqrt(2)*180/10))
    c2 = b1
    c3 = -a1*a1
    c1 = 1-c2-c3

    hp = np.zeros(eur.size)
    filt = np.zeros(eur.size)
    highestc = np.zeros((len(eur)))
    lowestc = np.zeros((len(eur)))
    ratio = np.zeros((49,2))
    stoc = np.zeros((49,3))
    """
    No caso é 49 em myindicator, porem teria de fazer (len(eur), 49, 3)
    Posso inverter o array, onde cada uma das 49 correlações, tenha um len(eurs)
    """

    for i in range(len(eur)):
        if i < 2:
            continue
        hp[i] = (1-alpha1/2)*(1-alpha1/2)*(eur[i]-2*eur[i-1]+eur[i-2])+2*(1-alpha1)*hp[i-1]-(1-alpha1)*(1-alpha1)*hp[i-2]
        filt[i] = c1*(hp[i] + hp[i-1])/2+c2*filt[i-1]+c3*filt[i-2]

        if i < 23:
            continue

        for lookback in range(5, 49):
            ratio[lookback, 1] = ratio[lookback, 0]
            stoc[lookback, 2] = stoc[lookback, 1]
            stoc[lookback, 1] = stoc[lookback, 0]
            highestc[i] = filt[i]
            lowestc[i] = filt[i]
            for count in range(lookback-1):
                if filt[i-count] > highestc[i]:
                    highestc[i] = filt[i-count]
                elif filt[i-count] < lowestc[i]:
                    lowestc[i] = filt[i-count]
            ratio[lookback, 0] = (filt[i]-lowestc[i])/(highestc[i]-lowestc[i])
            stoc[lookback, 0] = c1*(ratio[lookback, 0]+ratio[lookback, 1])/2+c2*stoc[lookback, 1]+c3*stoc[lookback, 2]

            if stoc[lookback, 0] < 0:
                stoc[lookback, 0] = 0
            elif stoc[lookback, 0] > 1:
                stoc[lookback, 0] = 1

    return stoc
