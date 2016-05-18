import pandas as pd
import numpy as np

DATA_DIR = './data/'
filenames = ['census_income_learn', 'census_income_test']
# Load the csv and set up the column names

cols = ['age',
       'class_of_worker',
       'industry_code',
       'occupation_code',
       'education',
       'wage_per_hour',
       'enrolled_in_edu_inst_last_wk',
       'marital_status',
       'major_industry_code',
       'major_occupation_code',
       'race',
       'hispanic_Origin',
       'sex',
       'member_of_a_labor_union',
       'reason_for_unemployment',
       'full_or_part_time_employment_stat',
       'capital_gains',
       'capital_losses',
       'divdends_from_stocks',
       'tax_filer_status',
       'region_of_previous_residence',
       'state_of_previous_residence',
       'detailed_household_and_family_stat',
       'detailed_household_summary_in_household',
       'instance_weight',
       'migration_code_change_in_msa',
       'migration_code_change_in_reg',
       'migration_code_move_within_reg',
       'live_in_this_house_1_year_ago',
       'migration_prev_res_in_sunbelt',
       'num_persons_worked_for_employer',
       'family_members_under_18',
       'country_of_birth_father',
       'country_of_birth_mother',
       'country_of_birth_self',
       'citizenship',
       'own_business_or_self_employed',
       'fill_inc_questionnaire_for_veteran_admin',
       'veterans_benefits',
       'weeks_worked_in_year',
       'year',
       'label']

drop_cols = ['occupation_code',
       'enrolled_in_edu_inst_last_wk',
       'major_industry_code',
       'member_of_a_labor_union',
       'reason_for_unemployment',
       'region_of_previous_residence',
       'state_of_previous_residence',
       'detailed_household_summary_in_household',
       'instance_weight',
       'migration_code_change_in_msa',
       'migration_code_change_in_reg',
       'migration_code_move_within_reg',
       'live_in_this_house_1_year_ago',
       'migration_prev_res_in_sunbelt',
       'family_members_under_18',
       'country_of_birth_father',
       'country_of_birth_mother',
       'country_of_birth_self',
       'citizenship',
       'own_business_or_self_employed',
       'year']

dummies_cols = {
    'industry_code': {
        'industricode_0': [0]
    },
    'class_of_worker': {
        'private_worker': [" Private"],
        'public_worker': [' Local government', ' State government', ' Federal government']
    },
    'education': {
        'no_university': [  ' Children',
                            ' 1st 2nd 3rd or 4th grade',
                            ' Less than 1st grade',
                            ' 5th or 6th grade',
                            ' 7th and 8th grade',
                            ' 9th grade',
                            ' 10th grade',
                            ' 11th grade',
                            ' 12th grade no diploma',
                            ' High schoolgraduate'
        ],
        'university_degree': [  ' Bachelors degree(BA AB BS)',
                                ' Masters degree(MA MS MEng MEd MSWMBA)',
                                ' Associates degree-occup /vocational',
                                ' Associates degree-academic program',
                                ' Doctoratedegree(PhD EdD)',
                                ' Prof school degree (MD DDS DVM LLB JD)'
        ]
    },
    'marital_status': {
        'never_maried': [' Never married'],
        'married_civilian_spouse_present': [' Married-civilian spouse present']
    },
    'major_occupation_code': {
        'well_paid_occupation': [  ' Sales',
                                    ' Professional specialty',
                                    ' Executive admin and managerial'
        ]
    },
    'sex': {
        'is_female': [' Female']
    },
    'full_or_part_time_employment_stat': {
        'not_in_labor_force_or_armed_force': [' Children or Armed Forces',' Not in labor force'],
        'full_time_schedules': [' Full-time schedules']
    },
    'tax_filer_status': {
        'tax_nonfiler': [' Nonfiler'],
        'tax_joint_both_under_65': [' Joint both under 65']
    },
    'detailed_household_and_family_stat': {
        'householders': [' Householder']
    },
    'fill_inc_questionnaire_for_veteran_admin': {
        'fill_inc_questionnaire_for_veteran_admin_yes_or_no': [' Yes', ' No']
    },
    'veterans_benefits': {
        'veterans_benefits_1_or_2': [1, 2]
    }

}
def load(filename):
    # load files and remove the ? and replance them by Nan
    df = pd.read_csv(  DATA_DIR + filename + '.csv',
                             header=None,
                             names=cols)
    df = df.drop(drop_cols, axis=1).replace(' ?', np.nan)

    # Save label to another filename_label.csv and remove the column label
    labels = [ 1 if label == ' 50000+.' else -1 for label in df.get('label') ]
    pd.DataFrame(labels, columns=['label']).to_csv(DATA_DIR + filename + '_label.csv', index = False)
    return df.drop('label', axis=1)

def generate_dummie_column(df):
    for prev_col in dummies_cols:
        for new_col in dummies_cols[prev_col]:
            df[new_col] = [int(value) for value in df[prev_col].isin(dummies_cols[prev_col][new_col])]
    return df.drop(list(dummies_cols.keys()),axis=1)

def generate_white_asian_column(df):
    df['white_asian'] = [int(value) for value in (df['race'].isin([' White', ' Asian']) & df['hispanic_Origin'].isin([' All other']))]
    return df.drop(['race','hispanic_Origin'], axis = 1)

for filename in filenames:
    df = generate_white_asian_column(generate_dummie_column(load(filename)))
    df.to_csv(DATA_DIR + filename + '_data.csv', index = False)
