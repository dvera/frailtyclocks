from sklearn.externals import joblib
import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns

def getresult(request):
    sampleData = pd.read_csv('media/sampleData.csv')
    controlData = sampleData[(sampleData['Group'] == 'Con')]
    mrData = sampleData[(sampleData['Group'] == 'MetR')]

    frightAge = joblib.load('media/fright_age.sav')
    afraidScore = joblib.load('media/afraid_score.sav')

    frightVariables = ['Tail_stiffening',
                    'Breathing_rate_depth',
                    'Gait_disorders',
                    'Hearing_loss',
                    'Kyphosis',
                    'Tremor',
                    'Body_condition_score',
                    'Forelimb_grip_strength',
                    '%twc',
                    'Menace_reflex',
                    'Alopecia',
                    'Tumours',
                    'Diarrhoea',
                    'Vaginal_uterine_penile_prolapse',
                    'Microphthalmia',
                    'Dermatitis',
                    'Rectal_prolapse',
                    'Distended_abdomen',
                    'Eye_discharge_swelling',
                    'Coat_condition',
                    'Body_Weight_Score']

    afraidVariables = ['Body_Weight_Score',
                    'Alopecia',
                    'Loss_of_fur_colour',
                    'Dermatitis',
                    'Loss_of_whiskers',
                    'Coat_condition',
                    'Tumours',
                    'Distended_abdomen',
                    'Kyphosis',
                    'Tail_stiffening',
                    'Gait_disorders',
                    'Tremor',
                    'Forelimb_grip_strength',
                    'Body_condition_score',
                    'Vestibular_disturbance',
                    'Hearing_loss',
                    'Cataracts',
                    'Corneal_capacity',
                    'Eye_discharge_swelling',
                    'Microphthalmia',
                    'Vision_loss',
                    'Menace_reflex',
                    'Nasal_discharge',
                    'Rectal_prolapse',
                    'Vaginal_uterine_penile_prolapse',
                    'Diarrhoea',
                    'Breathing_rate_depth',
                    'Mouse_grimace_scale',
                    'Piloerection',
                    '%twc',
                    '%rwc',
                    'Thresh_%rwc',
                    'age_days']

    print('FI SCORE')
    print('')
    print('Median')
    print('Control: ', round(np.median(controlData['FI']), 3))
    print('MetR: ', round(np.median(mrData['FI']), 3))
    print('')
    print('Mean')
    print('Control: ', round(np.mean(controlData['FI']), 3))
    print('MetR: ', round(np.mean(mrData['FI']), 3))
    print('')
    print('Standard Deviation')
    print('Control: ', round(np.std(controlData['FI']), 3))
    print('MetR: ', round(np.std(mrData['FI']), 3))
    print('')
    print("P-value")
    print(round(stats.ttest_ind(controlData['FI'], mrData['FI']).pvalue, 5))

    frightControl = frightAge.predict(controlData[frightVariables])
    frightMr = frightAge.predict(mrData[frightVariables])

    print('FRIGHT age')
    print('')
    print('Median (months)')
    print('Control: ', round(np.median(frightControl / 30.5), 3))
    print('MetR: ', round(np.median(frightMr / 30.5), 3))
    print('')
    print('Mean (months)')
    print('Control: ', round(np.mean(frightControl / 30.5), 3))
    print('MetR: ', round(np.mean(frightMr / 30.5), 3))
    print('')
    print('Standard deviation (months)')
    print('Control: ', round(np.std(frightControl / 30.5), 3))
    print('MetR: ', round(np.std(frightMr / 30.5), 3))
    print('')
    print('P-value')
    print(round(stats.ttest_ind(frightControl, frightMr).pvalue, 5))

    print('//////////frightcontrol')
    frightControlaa = list(frightControl)
    print(frightControl)
    print(frightControlaa)

    print('hhhhhhhhhhhhjjjjjFrightcontrol///')
    frightMraa = list(frightMr)
    print(frightMr)
    print(frightMraa)
    afraidControl = afraidScore.predict(controlData[afraidVariables])
    afraidMr = afraidScore.predict(mrData[afraidVariables])

    print('AFRAID clock')
    print('')
    print('Median (months)')
    print('Control: ', round(np.median(afraidControl / 30.5), 3))
    print('MetR: ', round(np.median(afraidMr / 30.5), 3))
    print('')
    print('Mean (months)')
    print('Control: ', round(np.mean(afraidControl / 30.5), 3))
    print('MetR: ', round(np.mean(afraidMr / 30.5), 3))
    print('')
    print('Standard deviation (months)')
    print('Control: ', round(np.std(afraidControl / 30.5), 3))
    print('MetR: ', round(np.std(afraidMr / 30.5), 3))
    print('')
    print('P-value')
    print(round(stats.ttest_ind(afraidControl, afraidMr).pvalue, 5))

    print('/////')

    list(afraidControl)
    print(afraidControl)

    list(afraidMr)
    print(afraidMr)
