def plot_cluster_gbir(df_cluster, eqp_1, eqp_2):
    fig = plt.figure(figsize = (8, 8))
    ax = fig.add_subplot()

    title = ''

    x_c = []
    y_c = []

    for i, row in df_cluster.iterrows():
        eqp = row['EQP_ID']
        warp = row['6900_GBIR_AFS2']

        if eqp in [eqp_1, eqp_2]:
            weight = 'bold'
            color = 'b' if eqp == eqp_1 else 'r'
            fontsize = 15
            title += f'{eqp}: {warp:.2f}um. '
            x_c.append(row['X'])
            y_c.append(row['Y'])

        else:
            weight = None
            color = 'gray'
            fontsize = 10

        ax.text(
            x = row['X'], 
            y = row['Y'], 
            s = row['EQP_ID'], 
            color = color, 
            fontsize = fontsize, 
            ha = 'center',
            va = 'center',
            weight = weight
        )

    ax.add_patch(plt.Circle(
        xy = (np.mean(x_c), np.mean(y_c)), 
        radius = 0.15,
        fc = 'w',
        ec = '#E1002A',
        linestyle = '--',
        linewidth = 2
    ))

    ax.set_title(title.strip(), fontsize = 15)
    ax.set_xlim(-0.15, 1.15)
    ax.set_ylim(-0.15, 1.15)
    return fig
