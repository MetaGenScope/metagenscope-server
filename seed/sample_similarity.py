"""Seed data for Sample Similarity Query Result."""


from app.query_results.query_result_models import SampleSimilarityResult

# pylint: disable=invalid-name
categories = {
    "city": [
        "Montevideo",
        "Sacramento",
        "Seoul",
        "Oslo",
        "Hong_Kong",
        "Lisbon",
        "Mexico_City",
        "Shanghai"
    ]
}

# pylint: disable=invalid-name
tools = {
    "metaphlan2" : {
        "x_label" : "metaphlan2 tsne x",
        "y_label" : "metaphlan2 tsne y"
    },
    "kraken"     : {
        "x_label" : "kraken tsne x",
        "y_label" : "kraken tsne y"
    }
}

# pylint: disable=invalid-name
data_records = [
    {
        "SampleID"     : "MetaSUB_Pilot__01_cZ__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.46118640628005614,
        "metaphlan2_y" : 0.15631940943278633,
        "kraken_x"     : 0.2364852416971677,
        "kraken_y"     : 0.06210990404248502
    },
    {
        "SampleID"     : "MetaSUB_Pilot__02_CAR__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.014732822485588083,
        "metaphlan2_y" : -0.13912287306618865,
        "kraken_x"     : -0.032148799771948997,
        "kraken_y"     : -0.16322878670609745
    },
    {
        "SampleID"     : "MetaSUB_Pilot__03_PE__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.05879187412484954,
        "metaphlan2_y" : -0.2616577515447991,
        "kraken_x"     : -0.15875291473621853,
        "kraken_y"     : -0.09419948915032159
    },
    {
        "SampleID"     : "MetaSUB_Pilot__04_SC__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.07053388490577094,
        "metaphlan2_y" : -0.2409485840773251,
        "kraken_x"     : -0.06628916944784255,
        "kraken_y"     : -0.11568418556080352
    },
    {
        "SampleID"     : "MetaSUB_Pilot__06_VDE__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.5671517050261656,
        "metaphlan2_y" : -0.3732222020917796,
        "kraken_x"     : -0.18514827642925416,
        "kraken_y"     : 0.8308492192403135
    },
    {
        "SampleID"     : "MetaSUB_Pilot__07_CSC1__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.7107801177656345,
        "metaphlan2_y" : 0.2118077491782587,
        "kraken_x"     : 0.3899038321490494,
        "kraken_y"     : 0.41531229505056166
    },
    {
        "SampleID"     : "MetaSUB_Pilot__16_PICH__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : -0.14927399654041443,
        "metaphlan2_y" : -0.017085474779386888,
        "kraken_x"     : 0.03849428662393287,
        "kraken_y"     : -0.2735056777767319
    },
    {
        "SampleID"     : "MetaSUB_Pilot__17_CSC3__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : -0.05501124327833107,
        "metaphlan2_y" : -0.0408267506095948,
        "kraken_x"     : -0.5030217246225399,
        "kraken_y"     : 0.3202382464514602
    },
    {
        "SampleID"     : "MetaSUB_Pilot__18_BUC__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.31832392015756567,
        "metaphlan2_y" : 0.06433257206676846,
        "kraken_x"     : 0.10746967495666913,
        "kraken_y"     : 0.0909655196268994
    },
    {
        "SampleID"     : "MetaSUB_Pilot__19_PA__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.08432891515498618,
        "metaphlan2_y" : -0.20738229938777136,
        "kraken_x"     : -0.02759566675097594,
        "kraken_y"     : -0.1320361145356604
    },
    {
        "SampleID"     : "MetaSUB_Pilot__1A__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.4460651909158868,
        "metaphlan2_y" : -0.292078305445016,
        "kraken_x"     : -0.3269422956120058,
        "kraken_y"     : -0.5540793133977971
    },
    {
        "SampleID"     : "MetaSUB_Pilot__1B__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.5181038684158825,
        "metaphlan2_y" : -0.3162800076257146,
        "kraken_x"     : -0.38757149440075034,
        "kraken_y"     : -0.5589124560592684
    },
    {
        "SampleID"     : "MetaSUB_Pilot__1C__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.4023589539822681,
        "metaphlan2_y" : -0.24918276652209206,
        "kraken_x"     : -0.3318342551513053,
        "kraken_y"     : -0.499327368815819
    },
    {
        "SampleID"     : "MetaSUB_Pilot__20_NSC__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.8110296997621189,
        "metaphlan2_y" : 0.3907940026833274,
        "kraken_x"     : 0.2552539335739224,
        "kraken_y"     : 0.2098319292123436
    },
    {
        "SampleID"     : "MetaSUB_Pilot__21_CSC2__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.5529665790944917,
        "metaphlan2_y" : 0.1755192976085808,
        "kraken_x"     : -0.012686325663821729,
        "kraken_y"     : 0.1815181522497419
    },
    {
        "SampleID"     : "MetaSUB_Pilot__22_CN__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.5142663203480249,
        "metaphlan2_y" : 0.13461350861978638,
        "kraken_x"     : 0.20204158907484443,
        "kraken_y"     : 0.17681784137240875
    },
    {
        "SampleID"     : "MetaSUB_Pilot__23_POCB__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.5652222019965725,
        "metaphlan2_y" : -0.3665205147229157,
        "kraken_x"     : -0.18337745542393155,
        "kraken_y"     : 0.8293248539250143
    },
    {
        "SampleID"     : "MetaSUB_Pilot__24_POC__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.5669033846643622,
        "metaphlan2_y" : -0.36151899203388077,
        "kraken_x"     : -0.18333570602827637,
        "kraken_y"     : 0.829691799243115
    },
    {
        "SampleID"     : "MetaSUB_Pilot__25_cA__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.7149089290981672,
        "metaphlan2_y" : 0.2884734622148664,
        "kraken_x"     : 0.3087419569710372,
        "kraken_y"     : 0.30619414664556444
    },
    {
        "SampleID"     : "MetaSUB_Pilot__26_PN__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.032061173168285245,
        "metaphlan2_y" : -0.3598251777255198,
        "kraken_x"     : -0.209769967886508,
        "kraken_y"     : -0.06494681247086799
    },
    {
        "SampleID"     : "MetaSUB_Pilot__27_RAM__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.313057805461833,
        "metaphlan2_y" : 0.05953439438799148,
        "kraken_x"     : 0.02663925140413106,
        "kraken_y"     : 0.132345659155688
    },
    {
        "SampleID"     : "MetaSUB_Pilot__2A__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.22134634539433876,
        "metaphlan2_y" : 0.03423064485834206,
        "kraken_x"     : -0.2615146307226241,
        "kraken_y"     : -0.5099559351142051
    },
    {
        "SampleID"     : "MetaSUB_Pilot__2B__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.46785068920618034,
        "metaphlan2_y" : -0.2545596058618215,
        "kraken_x"     : -0.3066617414310878,
        "kraken_y"     : -0.45755350696242425
    },
    {
        "SampleID"     : "MetaSUB_Pilot__2C__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.43978688284547973,
        "metaphlan2_y" : -0.21745500173177218,
        "kraken_x"     : -0.25757306974068395,
        "kraken_y"     : -0.4396436252252222
    },
    {
        "SampleID"     : "MetaSUB_Pilot__3A__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.2542417786040703,
        "metaphlan2_y" : -0.07205358195526725,
        "kraken_x"     : -0.3025530151660672,
        "kraken_y"     : -0.3222337348422858
    },
    {
        "SampleID"     : "MetaSUB_Pilot__3B__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.3115625438541915,
        "metaphlan2_y" : -0.09146432762999493,
        "kraken_x"     : -0.2197103424888229,
        "kraken_y"     : -0.39290195203749567
    },
    {
        "SampleID"     : "MetaSUB_Pilot__3C__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.3419080544056137,
        "metaphlan2_y" : -0.13802240045736044,
        "kraken_x"     : -0.24567822651776106,
        "kraken_y"     : -0.30879553506646046
    },
    {
        "SampleID"     : "MetaSUB_Pilot__4A__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.23832065084741388,
        "metaphlan2_y" : -0.12724193649277565,
        "kraken_x"     : -0.38232627506589617,
        "kraken_y"     : -0.3719114720789443
    },
    {
        "SampleID"     : "MetaSUB_Pilot__4B__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.35407147773165143,
        "metaphlan2_y" : -0.12628112012948164,
        "kraken_x"     : -0.33089725870167963,
        "kraken_y"     : -0.3774782331022909
    },
    {
        "SampleID"     : "MetaSUB_Pilot__4C__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.004503642343718623,
        "metaphlan2_y" : 0.07959113724738205,
        "kraken_x"     : -0.24453419474023558,
        "kraken_y"     : -0.2191668345557638
    },
    {
        "SampleID"     : "MetaSUB_Pilot__5A__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.3233426600287013,
        "metaphlan2_y" : -0.24116103983741935,
        "kraken_x"     : -0.4556582931984793,
        "kraken_y"     : -0.48391757804343527
    },
    {
        "SampleID"     : "MetaSUB_Pilot__5B__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.2991024433252991,
        "metaphlan2_y" : -0.20019367629181908,
        "kraken_x"     : -0.4361100047448628,
        "kraken_y"     : -0.4173927966647875
    },
    {
        "SampleID"     : "MetaSUB_Pilot__5C__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.22969783595698356,
        "metaphlan2_y" : -0.18261546500714654,
        "kraken_x"     : -0.41172015814209517,
        "kraken_y"     : -0.4790238729232666
    },
    {
        "SampleID"     : "MetaSUB_Pilot__6A__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.3607901148739617,
        "metaphlan2_y" : -0.20321810058840423,
        "kraken_x"     : -0.3855628693731041,
        "kraken_y"     : -0.43971624245236085
    },
    {
        "SampleID"     : "MetaSUB_Pilot__6B__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.2813743666442504,
        "metaphlan2_y" : -0.1323683719378345,
        "kraken_x"     : -0.27525579298664565,
        "kraken_y"     : -0.3902467117399651
    },
    {
        "SampleID"     : "MetaSUB_Pilot__6C__unknown__seq1end",
        "city"         : "Sacramento",
        "metaphlan2_x" : -0.5298629546610447,
        "metaphlan2_y" : -0.21941687030619564,
        "kraken_x"     : -0.1982776160114238,
        "kraken_y"     : -0.3507031954933072
    },
    {
        "SampleID"     : "MetaSUB_Pilot__8_LC___unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.08362071891276163,
        "metaphlan2_y" : -0.2522056701490681,
        "kraken_x"     : -0.05971296766375258,
        "kraken_y"     : -0.09111756110555065
    },
    {
        "SampleID"     : "MetaSUB_Pilot__9_MAL__unknown__seq1end",
        "city"         : "Montevideo",
        "metaphlan2_x" : 0.5643324933748024,
        "metaphlan2_y" : -0.3604356516072299,
        "kraken_x"     : -0.1823736039768506,
        "kraken_y"     : 0.828182059503917
    },
    {
        "SampleID"     : "MetaSUB_Pilot__Dorimcheon_1__unknown__seq1end",
        "city"         : "Seoul",
        "metaphlan2_x" : -0.3784616657158487,
        "metaphlan2_y" : 0.12009384616685358,
        "kraken_x"     : -0.7678934753239208,
        "kraken_y"     : 0.4472651292648884
    },
    {
        "SampleID"     : "MetaSUB_Pilot__Dorimcheon_2__unknown__seq1end",
        "city"         : "Seoul",
        "metaphlan2_x" : -0.4255606155621036,
        "metaphlan2_y" : 0.23211498126269825,
        "kraken_x"     : -0.7486962971784338,
        "kraken_y"     : 0.56947482530344
    },
    {
        "SampleID"     : "MetaSUB_Pilot__Dorimcheon_3__unknown__seq1end",
        "city"         : "Seoul",
        "metaphlan2_x" : -0.6047750843470698,
        "metaphlan2_y" : 0.16485342152767296,
        "kraken_x"     : -0.825811035745412,
        "kraken_y"     : 0.3441362129867683
    },
    {
        "SampleID"     : "MetaSUB_Pilot__FFL_S01__unknown__seq1end",
        "city"         : "Oslo",
        "metaphlan2_x" : -0.7161457727419375,
        "metaphlan2_y" : 0.014654114077570867,
        "kraken_x"     : -0.16404555912244312,
        "kraken_y"     : -0.9004433374254635
    },
    {
        "SampleID"     : "MetaSUB_Pilot__FFL_S02__unknown__seq1end",
        "city"         : "Oslo",
        "metaphlan2_x" : -0.5869323867307739,
        "metaphlan2_y" : 0.054271877269091405,
        "kraken_x"     : -0.04796627415982994,
        "kraken_y"     : -0.7923336151201438
    },
    {
        "SampleID"     : "MetaSUB_Pilot__FFL_S03__unknown__seq1end",
        "city"         : "Oslo",
        "metaphlan2_x" : -0.7090427666790946,
        "metaphlan2_y" : -0.23660529428922383,
        "kraken_x"     : -0.4894459269991316,
        "kraken_y"     : -0.6981291474019089
    },
    {
        "SampleID"     : "MetaSUB_Pilot__FFL_S04__unknown__seq1end",
        "city"         : "Oslo",
        "metaphlan2_x" : -0.8264462784997162,
        "metaphlan2_y" : -0.018621323057247795,
        "kraken_x"     : -0.24481541128993423,
        "kraken_y"     : -0.8777067864699534
    },
    {
        "SampleID"     : "MetaSUB_Pilot__FFL_S05__unknown__seq1end",
        "city"         : "Oslo",
        "metaphlan2_x" : -0.6737924174337995,
        "metaphlan2_y" : 0.09690419169454907,
        "kraken_x"     : -0.12763917774868377,
        "kraken_y"     : -0.8242084282104294
    },
    {
        "SampleID"     : "MetaSUB_Pilot__FFL_S06__unknown__seq1end",
        "city"         : "Oslo",
        "metaphlan2_x" : -0.6775510437506481,
        "metaphlan2_y" : 0.06291505181436895,
        "kraken_x"     : -0.10421514386883375,
        "kraken_y"     : -0.7909578892408063
    },
    {
        "SampleID"     : "MetaSUB_Pilot__FFL_S13__unknown__seq1end",
        "city"         : "Oslo",
        "metaphlan2_x" : -0.7902479814293678,
        "metaphlan2_y" : 0.0019696225805720603,
        "kraken_x"     : -0.1970676641492646,
        "kraken_y"     : -0.879492645803585
    },
    {
        "SampleID"     : "MetaSUB_Pilot__FFL_S14__unknown__seq1end",
        "city"         : "Oslo",
        "metaphlan2_x" : -0.8439714545662441,
        "metaphlan2_y" : -0.014140338765505047,
        "kraken_x"     : -0.2733897844085359,
        "kraken_y"     : -0.8946838981443122
    },
]

sample_similarity = SampleSimilarityResult(categories=categories, tools=tools, data_records=data_records)
