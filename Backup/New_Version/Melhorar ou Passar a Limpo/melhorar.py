def walk_forward_test(walk1, test1, walk2, test2, walk3, test3, walk4, test4, walk5, test5, final, data_numpy, tot_iterations, plot=False, balance=1000):

    walk = np.array([walk1, walk2, walk3, walk4, walk5])
    test = np.array([test1, test2, test3, test4, test5])

    no_tpsl, _, _ = otimizado_no_tpsl(data_numpy, balance=1000)
    if plot:
        try:
            pd.Series(no_tpsl).plot()
            plt.title(f'No TPSL', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')

    # -------------------------------------------------------------------------

    walk_columns = []

    for j in range(5):

        walk_pd = pd.DataFrame()
        test_pd = pd.DataFrame()

        for i in range(1, tot_iterations):
            walk_result, _, _ = otimizado_tpsl(walk[j], tpsl=i)
            if walk_result[-1] > balance:
                walk_pd[i] = pd.Series(walk_result)

        if plot:
            try:
                walk_pd.plot()
                plt.title(f'Teste Walk Open {j+1}', fontsize=30)
                plt.grid()
                plt.show()
            except TypeError:
                print('No data to plot.')

        for i in walk_pd.columns:
            test_result, _, _ = otimizado_tpsl(test[j], tpsl=i)
            if test_result[-1] > balance:
                test_pd[i] = pd.Series(test_result)

        if plot:
            try:
                test_pd.plot()
                plt.title(f'Teste Open {j+1}', fontsize=30)
                plt.grid()
                plt.show()
            except TypeError:
                print('No data to plot.')

        walk_columns.append(list(test_pd.columns))

    x = af.compare(walk_columns)

    test_final = pd.DataFrame()
    for i in x:
        final_result, _, _ = otimizado_tpsl(final, tpsl=i)
        test_final[i] = pd.Series(final_result)

    if plot:
        try:
            test_final.plot()
            plt.title(f'Teste Final Open', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')

    all_tpsl = pd.DataFrame()
    for i in range(1, tot_iterations):
        a, _, _ = otimizado_tpsl(data_numpy, tpsl=i)
        all_tpsl[i] = pd.Series(a)

    if plot:
        try:
            all_tpsl.plot()
            plt.title(f'All Open', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')

    bests_results_lr = []
    cut = 0.0
    for i in all_tpsl.columns:
        lr_test = pd.DataFrame()
        lr_test['x'] = pd.Series(range(len(all_tpsl[i].dropna())))
        lr_test['y'] = all_tpsl[i].dropna()
        x_v = lr_test[['x']]
        y_v = lr_test[['y']]
        model = LinearRegression()
        model.fit(x_v, y_v)
        result = model.score(x_v, y_v)
        if result > cut:
            bests_results_lr.append(i)
            cut = result

    if plot:
        try:
            all_tpsl[bests_results_lr].plot()
            plt.title(f'Linear Regression Open', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')

    # -------------------------------------------------------------------------

    walk_columns = []

    for j in range(5):

        walk_pd = pd.DataFrame()
        test_pd = pd.DataFrame()

        for i in range(1, tot_iterations):
            walk_result, _, _ = otimizado_tpsl_ohl(walk[j], tpsl=i)
            if walk_result[-1] > balance:
                walk_pd[i] = pd.Series(walk_result)

        if plot:
            try:
                walk_pd.plot()
                plt.title(f'Teste Walk OHL {j+1}', fontsize=30)
                plt.grid()
                plt.show()
            except TypeError:
                print('No data to plot.')

        for i in walk_pd.columns:
            test_result, _, _ = otimizado_tpsl_ohl(test[j], tpsl=i)
            if test_result[-1] > balance:
                test_pd[i] = pd.Series(test_result)

        if plot:
            try:
                test_pd.plot()
                plt.title(f'Teste OHL {j+1}', fontsize=30)
                plt.grid()
                plt.show()
            except TypeError:
                print('No data to plot.')

        walk_columns.append(list(test_pd.columns))

    x = af.compare(walk_columns)

    test_final = pd.DataFrame()
    for i in x:
        final_result, _, _ = otimizado_tpsl_ohl(final, tpsl=i)
        test_final[i] = pd.Series(final_result)

    if plot:
        try:
            test_final.plot()
            plt.title(f'Teste Final OHL', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')

    all_tpsl = pd.DataFrame()
    for i in range(1, tot_iterations):
        a, _, _ = otimizado_tpsl_ohl(data_numpy, tpsl=i)
        all_tpsl[i] = pd.Series(a)

    if plot:
        try:
            all_tpsl.plot()
            plt.title(f'All OHL', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')

    bests_results_lr = []
    cut = 0.0
    for i in all_tpsl.columns:
        lr_test = pd.DataFrame()
        lr_test['x'] = pd.Series(range(len(all_tpsl[i].dropna())))
        lr_test['y'] = all_tpsl[i].dropna()
        x_v = lr_test[['x']]
        y_v = lr_test[['y']]
        model = LinearRegression()
        model.fit(x_v, y_v)
        result = model.score(x_v, y_v)
        if result > cut:
            bests_results_lr.append(i)
            cut = result

    if plot:
        try:
            all_tpsl[bests_results_lr].plot()
            plt.title(f'Linear Regression OHL', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')
