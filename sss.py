print(st.session_state['df_cluster_gbir'])
       EQP_ID         X         Y  6900_GBIR_AFS2
0    BPDPD100  0.342670  0.216720        0.079025
1    BPDPD101  0.516418  0.573984        0.101918
2    BPDPD102  0.650096  0.297412        0.098439
3    BPDPD103  0.702466  0.692311        0.076961
4    BPDPD104  0.245268  0.610878        0.092579
..        ...       ...       ...             ...
121   TPDSP49  0.504799  1.000000        0.200366
122   TPDSP51  0.716665  0.750337        0.152980
123   TPDSP52  0.348907  0.469353        0.197178
124   TPDSP55  0.497973  0.847248        0.170392
125    TPDSP9  0.113013  0.662466        0.302143

with col3:
    fig = plot_cluster_gbir(
        df_cluster_gbir = st.session_state['df_cluster_gbir'], 
        eqp_1 = eqp_1, 
        eqp_2 = eqp_2
    )
    st.pyplot(fig, use_container_width = True)
