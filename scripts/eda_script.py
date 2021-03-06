# author: A. Muhammad
# date: 2020-02-01

'''This script performs EDA on the students performance datasets
for portuguese and math students and outputs necessary tables and
figures to path provided.

Usage: eda_script.py --file_path=<file_path> --results_path=<results_path>

Example: 
    python scripts/eda_script.py --file_path=data/ --results_path=results/

Options:
--file_path=<file_path>  Path (excluding filenames) to the csv file.
--results_path=<results_path>  Path for saving plots.
'''

import pandas as pd
import numpy as np
from docopt import docopt
import altair as alt
import re
import os


opt = docopt(__doc__)

def test_function():
    """
    Tests the input and output
    file paths.
    """
    file_path_check = re.match("([A-Za-z]+[.]{1}[A-Za-z]+)", opt["--file_path"]) 
    out_path_check = re.match("([A-Za-z]+[.]{1}[A-Za-z]+)", opt["--results_path"])
    assert file_path_check == None, "you can not have extensions in path, only directories."
    assert out_path_check == None, "you can not have extensions in path, only directories."
    try:
        os.listdir(opt["--file_path"])
        os.listdir(opt["--results_path"])
    except Exception as e:
        print(e)

# test function runs here
test_function()


opt = docopt(__doc__)

def main(file_path, results_path):
    # read in data
    df_mat = pd.read_csv(file_path + "student-mat_clean.csv")
    df_por = pd.read_csv(file_path + "student-por_clean.csv")

    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    
    ## tables
    # agg table math
    df_math_agg = df_mat[["romantic", "total_grade"]].groupby("romantic").agg(['count', 'mean', 'std'])
    df_math_agg['total_grade'].reset_index().round(4).to_csv(results_path + "math_table.csv", index=False)

    # agg table por
    df_por_agg = df_por[["romantic", "total_grade"]].groupby("romantic").agg(['count', 'mean', 'std'])
    df_por_agg['total_grade'].reset_index().round(4).to_csv(results_path + "por_table.csv", index=False)

    ## print certain findings
    print("{} math students were in relationships and {} were not.".format(
        df_mat['romantic'].value_counts()['yes'], 
        df_mat['romantic'].value_counts()['no']))
    print("{} portuguese language students were in relationships and {} were not.".format(
        df_por['romantic'].value_counts()['yes'], 
        df_por['romantic'].value_counts()['no']))
    print("The average total grade for math students in relationships was: {:.2f}/60".format(
        df_mat[df_mat['romantic'] == 'yes']['total_grade'].mean()))
    print("The average total grade for math students not in relationships was: {:.2f}/60".format(
        df_mat[df_mat['romantic'] == 'no']['total_grade'].mean()))
    print("The average total grade for portuguese students in relationships was: {:.2f}/60".format(
        df_por[df_por['romantic'] == 'yes']['total_grade'].mean()))
    print("The average total grade for portuguese students not in relationships was: {:.2f}/60".format(
        df_por[df_por['romantic'] == 'no']['total_grade'].mean()))

    ## make plots
    p_1_1 = alt.Chart(df_mat[df_mat['romantic']=="yes"]).transform_density(
        'total_grade',
        as_=['total_grade', 'density'],
    ).mark_bar().encode(
        x=alt.X("total_grade:Q", title="Total grade", bin = alt.Bin(extent=[0, 60], step=5)),
        y='density:Q',
    ).properties(
        width = 300,
        height = 400,
        title = "In relationship"
    )
    p_1_2 = alt.Chart(df_mat[df_mat['romantic']=="no"]).transform_density(
        'total_grade',
        as_=['total_grade', 'density'],
    ).mark_bar(color='orange').encode(
        x=alt.X("total_grade:Q", title="Total grade", bin = alt.Bin(extent=[0, 60], step=5)),
        y='density:Q',
    ).properties(
        width = 300,
        height = 400,
        title = "Not in relationship"
    )
    P_math = p_1_1 | p_1_2
    
    P_math.configure_title(
        fontSize=14,
    )

    p_2_1 = alt.Chart(df_por[df_por['romantic']=="yes"]).transform_density(
        'total_grade',
        as_=['total_grade', 'density'],
    ).mark_bar().encode(
        x=alt.X("total_grade:Q", title="Total grade", bin = alt.Bin(extent=[0, 60], step=5)),
        y='density:Q',
    ).properties(
        width = 300,
        height = 400,
        title = "In relationship"
    )
    p_2_2 = alt.Chart(df_por[df_por['romantic']=="no"]).transform_density(
        'total_grade',
        as_=['total_grade', 'density'],
    ).mark_bar(color='orange').encode(
        x=alt.X("total_grade:Q", title="Total grade", bin = alt.Bin(extent=[0, 60], step=5)),
        y='density:Q',
    ).properties(
        width = 300,
        height = 400,
        title = "Not in relationship"
    )
    P_por = p_2_1 | p_2_2
    P_por.configure_title(
        fontSize=14,
    )

    ## save plots
    P_math.save(results_path + "figures/math_plot.png", webdriver='chrome')
    P_por.save(results_path + "figures/por_plot.png", webdriver='chrome')


def mds_special():
    """
    Applies mds_special theme to plots 
    created by
    Firas Moosvi, instructor at UBC 
    Master of Data Science program.
    """
    font = "Arial"
    axisColor = "#000000"
    gridColor = "#DEDDDD"
    return {
        
        "config": {
            "title": {
                "fontSize": 24,
                "font": font,
                "anchor": "start", # equivalent of left-aligned.
                "fontColor": "#000000"
            },
            "background": "white",
            "axisX": {
                "domain": True,
                #"domainColor": axisColor,
                "gridColor": gridColor,
                "domainWidth": 1,
                "grid": False,
                "labelFont": font,
                "labelFontSize": 12,
                "labelAngle": 0, 
                #"tickColor": axisColor,
                "tickSize": 5, # default, including it just to show you can change it
                #"titleFont": font,
                "titleFontSize": 18,
                "titlePadding": 10, # guessing, not specified in styleguide
                "title": "X Axis Title (units)", 
            },
            "axisY": {
                "domain": False,
                "grid": True,
                "gridColor": gridColor,
                "gridWidth": 1,
                "labelFont": font,
                "labelFontSize": 12,
                "labelAngle": 0, 
                #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                "titleFont": font,
                "titleFontSize": 18,
                "titlePadding": 10, # guessing, not specified in styleguide
                "title": "Y Axis Title (units)", 
                # titles are by default vertical left of axis so we need to hack this 
                #"titleAngle": 0, # horizontal
                #"titleY": -10, # move it up
                #"titleX": 18, # move it to the right so it aligns with the labels 
            },
                }
            }
    

if __name__ == "__main__":
    main(opt["--file_path"], opt["--results_path"])
