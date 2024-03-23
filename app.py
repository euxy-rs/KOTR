import streamlit as st
import pandas as pd
import numpy as np
import update_map
import KOTR_update
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

team_names = ["Semen Demons", "Guthix Gooch", "Morytania Meatflaps"]

name_list = ["CIicking", "Suitabl3", "yankees fan7", "gim alone", "aged whale", "The Maher", "MIND THE WAP",
             "Cramolix", "Quinninho", "Azbirddog", "skoomadrinke", "Zalcanussy", "wimen", "Euxy", "stjonkbonk",
             "jinxtheminxx", "smallblue0", "FarmboyFrank", "Toyo Harada", "rez", "lord uhlen", "IAmDivine", "fleshrat", 
             "stinky metz", "plusblastbtw", "ThePoggest", "Jonte xu2", "TbowBundy", "ChikitiChina", "dwaggleim"]

#would be nice to get the same color formatting throughout
#but I couldn't figure out a way to use just hexcode or just RGB values sadly

team_colors = {team_names[0]: (255,255,255),
              team_names[1]: (0,255,0),
              team_names[2]: (100,0,100)}

plotly_team_colors = {team_names[0]: '#FFFFFF',
              team_names[1]: '#05FF00',
              team_names[2]: '#C000FF'}

comp_cols = ["Woodcutting EXP", "Fishing EXP", "Mining EXP", "Agility EXP", "Thieving EXP", "Slayer EXP",
                       "Farming EXP", "Runecrafting EXP", "Hunter EXP", "Abyssal Sire", 
                       "Alchemical Hydra", "Artio", "Barrows Chests", "Callisto", "Calvarion", "Cerberus", 
                       "Chambers of Xeric", "Chambers of Xeric: Challenge Mode", "Chaos Elemental", "Commander Zilyana", 
                       "Corporeal Beast", "Dagannoth Prime", "Dagannoth Rex", "Dagannoth Supreme",
                       "Duke Sucellus", "General Graardor", "Giant Mole", "Grotesque Guardians", 
                       "Kalphite Queen", "King Black Dragon", "Kraken", "Kree'Arra", "K'ril Tsutsaroth", 
                       "Nex", "Phosani's Nightmare",
                       "Phantom Muspah", "Sarachnis", "Scorpia", "Scurrius", "Spindel", "Tempoross", 
                       "The Corrupted Gauntlet", "The Leviathan","The Whisperer", "Theatre of Blood", 
                       "Theatre of Blood: Hard Mode", "Thermonuclear Smoke Devil", "Tombs of Amascut", "Tombs of Amascut: Expert Mode",
                       "TzKal-Zuk", "TzTok-Jad", "Vardorvis", "Venenatis", "Vet'ion", "Vorkath", "Wintertodt", "Zalcano", "Zulrah"]

start_df = KOTR_update.get_hiscores_data_start(name_list, comp_cols)

update_df = KOTR_update.get_hiscores_data(name_list, comp_cols)

ehp_df = pd.read_csv(f"https://raw.githubusercontent.com/euxy-rs/KOTR/main/Data/EHP.csv").set_index("Category")

ehp_df["EHP Rate"] = ehp_df["EHP Rate"].astype(float)

cols_to_add = ["Artio", "Calvarion", "Duke Sucellus", "Scurrius", "Spindel", "The Leviathan", "The Whisperer", "Vardorvis"]
for col in cols_to_add:
    if col not in start_df:
        start_df[col] = 0
        update_df[col] = 0

start_df = start_df[comp_cols].astype(float).replace(-1, 0)
update_df = update_df[comp_cols].astype(float).replace(-1, 0)
delta_df = update_df - start_df

team1 = ['stinky metz',
  'TbowBundy',
  'Azbirddog',
  'dwaggleim',
  'The Maher',
  'FarmboyFrank',
  'rez',
  'Zalcanussy',
  'plusblastbtw',
  'lord uhlen']

team2 = ['wimen',
  'stjonkbonk',
  'Euxy',
  'skoomadrinke',
  'MIND THE WAP',
  'Quinninho',
  'CIicking',
  'jinxtheminxx',
  'ChikitaChina',
  'Jonte xu2']

team3 = ['smallblue0',
  'Suitabl3',
  'IAmDivine',
  'Cramolix',
  'yankees fan7',
  'fleshrat',
  'gim alone',
  'Toyo Harada',
  'aged whale',
  'ThePoggest']

for name in start_df.index:
    if name in team1:
        delta_df.at[name, "Team"] = team_names[0]
    elif name in team2:
        delta_df.at[name, "Team"] = team_names[1]
    else:
        delta_df.at[name, "Team"] = team_names[2]

df_1 = delta_df[delta_df["Team"] == team_names[0]]
df_2 = delta_df[delta_df["Team"] == team_names[1]]
df_3 = delta_df[delta_df["Team"] == team_names[2]]

df_list = [df_1, df_2, df_3]

region_dict = {"Tirannwn": ["Woodcutting EXP", "Zulrah", "Zalcano", "The Corrupted Gauntlet"],
              "Fremennik": ["Mining EXP", "Vorkath", "Phantom Muspah", "Dagannoth Prime", "Dagannoth Rex", "Dagannoth Supreme", "Duke Sucellus"],
              "Kandarin": ["Fishing EXP", "Kraken", "Cerberus", "Thermonuclear Smoke Devil"],
              "Morytania": ["Agility EXP", "Barrows Chests", "Grotesque Guardians", "Phosani's Nightmare", "Theatre of Blood", "Theatre of Blood: Hard Mode"],
              "Karamja": ["Slayer EXP", "TzKal-Zuk", "TzTok-Jad"],
              "Wilderness": ["Callisto", "Calvarion", "Corporeal Beast", "Scorpia", "Venenatis", "Vet'ion", "King Black Dragon", "Artio", "Spindel", "Chaos Elemental"],
              "Zeah": ["Farming EXP", "Alchemical Hydra", "Chambers of Xeric", "Chambers of Xeric: Challenge Mode", "Sarachnis", "Wintertodt", "Vardorvis"],
              "Desert": ["Thieving EXP", "Kalphite Queen", "Tombs of Amascut", "Tombs of Amascut: Expert Mode", "Tempoross"],
              "Misthalin": ["Runecrafting EXP", "Abyssal Sire", "Giant Mole", "Scurrius", "The Whisperer", "The Leviathan"],
               "Asgarnia": ["Hunter EXP", "Kree'Arra", "General Graardor", "K'ril Tsutsaroth", "Nex", "Commander Zilyana"]}

individual_ehp = KOTR_update.calc_individual_ehp(delta_df, ehp_df)
individual_region_ehp = KOTR_update.calc_individual_ehp_region(delta_df, region_dict, ehp_df)
team_region_ehp = individual_region_ehp.groupby(by = "Team").sum().transpose().sort_index()
overall_score = KOTR_update.calc_overall_score(team_region_ehp)

st.set_page_config(layout = "wide")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Main", "Team Page", "Individual Stats", "Test"])

with tab1:
    st.dataframe(start_df)
    st.dataframe(update_df)
    st.dataframe(delta_df)
  
    st.header("Welcome to King of the Region!")
    st.image("https://github.com/euxy-rs/KOTR/blob/main/Data/trailblazer.png?raw=true")
    with st.container(border=True):
        st.write("Point are earned by gaining the most (or second most) combined EHB/EHP in a region - 1 point is awarded to first and 0.5 points are awarded to second, third place gets nothing. EHB/EHP rates are listed below, as well as which activity belongs to each region. Carefully make sure the content you are doing will count, if an activity is not listed it will not count for this competition! The team that obtains the most points will be considered the winner of the competition.")
        st.write("The use of any PvM or skilling services during the competition is not permitted. The person who signs up for the competition must be the person to play the account and gain experience/KC/boss drops to be eligible to contribute. Boosting of any kind is also not permitted (eg Corp boosting/Essence running). For this competition, alts are allowed in all forms and uses. 6 hour logs are not permitted before the start of the competition. All participants will need to re-log just prior to comp start. Additionally, the following are not permitted to be used during the competition: - Pre-banked experience (including, but not limited to, brimhaven agility tickets, ores stored in blast mine, exp lamps, glistening tears etc.) - Holding chest/other rewards before comp start e.g. CoX, ToB, Corrupted Gauntlet, Wintertodt crates, Tempoross reward points, - Pre-banked clue caskets where the competition awards points for clues")
        st.write("As a general rule of thumb, content that is meant to be counted for the competition must be done during the competition. Anyone breaking this rule will be disqualified.")
        st.write("This dashboard will scrape the hiscores once every hour to update players' gains and update the scoring. Once the competition begins, players CAN NOT change their name.")
        
    options = ehp_df["Region"].drop_duplicates().tolist()
    options.sort()
    with st.container(border=True):
        option = st.selectbox("Region Categories and EHP: ", (options))
        st.dataframe(ehp_df[ehp_df["Region"] == option].drop(columns = ["Region"]), use_container_width=True)
    
with tab2:
    KOTR_map = update_map.update_map("https://github.com/euxy-rs/KOTR/blob/main/Data/trailblazer.png?raw=true", team_region_ehp, team_colors)
    st.image(KOTR_map)
    
    st.header("Overall Score")
    with st.container(border=True):
        cols = st.columns(3)
        for i in range(3):
            col = cols[i]
            controlled_regions = []
            for index in team_region_ehp.index:
                if team_region_ehp.loc[index].idxmax(axis = "index") == team_region_ehp.columns[i]:
                    controlled_regions.append(index)
            with col: 
                st.metric(f"{str(overall_score.columns[i])}:", f"{overall_score.iloc[0,i]} points", ' | '.join(controlled_regions))

    st.header("Team region score: ")
    with st.container(height = 550, border=True):
        selection = "All"
        selections = team_region_ehp.index.tolist()
        selections.insert(0, "All")
        selection = st.selectbox("Which region do you want to display?", sorted(selections))

        col1, col2 = st.columns(2)
        with col1:
            if selection == "All":
                team_region_ehp.loc["Total"] = team_region_ehp.sort_index().sum()
                st.dataframe(team_region_ehp.style.background_gradient(cmap = 'Blues', axis = 1), width = 500, height = 500)
            else: 
                st.dataframe(team_region_ehp.loc[[selection],:].style.background_gradient(cmap = 'Blues', axis = 1), width = 500)

                maxes = individual_region_ehp[selection].max()
                less_than_max = individual_region_ehp[selection].where(individual_region_ehp[selection].lt(maxes, axis='rows'))
                seconds = less_than_max.max()

                st.metric(f"{selection} MVP:", f"{individual_region_ehp[selection].idxmax()} - {round(individual_region_ehp[selection].max(), 2)} EHP", f"{round(maxes - seconds, 2)} hours")
        with col2:
            fig = KOTR_update.region_score_plotly(team_region_ehp, selection, plotly_team_colors, width = 600, height = 400)
            st.plotly_chart(fig, theme = "streamlit")

with tab3:
    team_options = delta_df["Team"].drop_duplicates().tolist()
    team_options.sort()
    team_option = st.selectbox("Team: ", (team_options))
    team_score = overall_score.at["Score", team_option]

    score_t = overall_score.transpose()
    score_t = score_t.sort_values(by = "Score", ascending = False)
    position = score_t.index.get_loc(team_option) + 1

    region_summary = KOTR_update.team_tracking(team_region_ehp, team_option)

    if position == 1:
        position = "first"
    if position == 2:
        position = "second"
    if position == 3:
        position = "third"

    st.header(f"{team_option} is currently in {position} place with {team_score} points.")

    team_display = st.selectbox("Which table do you want to display?", [None, "Raw gains", "EHP gains", "Region totals", "Region leaderboard"])

    if team_display == None:
        st.markdown(":frog: ribbeth")
    if team_display == "Raw gains":
        team_delta_df = delta_df[delta_df["Team"] == team_option].drop(columns = ["Team"])
        team_delta_df = KOTR_update.add_total_row(team_delta_df)
        st.dataframe(team_delta_df, height = (len(team_delta_df) + 1) * 35 + 3)
    if team_display == "EHP gains":
        team_ind_ehp = individual_ehp[individual_ehp["Team"] == team_option].drop(columns = ["Team"])
        team_ind_ehp = KOTR_update.add_total_row(team_ind_ehp)
        st.dataframe(team_ind_ehp, height = (len(team_ind_ehp) + 1) * 35 + 3)
    if team_display == "Region totals":
        team_ind_region_ehp = individual_region_ehp[individual_region_ehp["Team"] == team_option].drop(columns = ["Team"])
        team_ind_region_ehp = KOTR_update.add_total_row(team_ind_region_ehp)
        st.dataframe(team_ind_region_ehp, height = (len(team_ind_region_ehp) + 1) * 35 + 3)
    if team_display == "Region leaderboard":
        st.dataframe(region_summary, height = (len(region_summary) + 1) * 35 + 3)
    
with tab4:
    st.text("This is the tab for individual stats.")
    with st.container(border = True):
        st.header("Region Leaderboard")
        names = delta_df.index.tolist()
        names = sorted(names, key = str.casefold)
        names.insert(0, "None")
        name_selection = st.selectbox("Which player do you want to highlight?", names)
        st.dataframe(KOTR_update.region_leaderboard(individual_region_ehp).style.map(lambda x: "background-color: blue" if x == name_selection else None))
    with st.container(border = True):
        st.header("EHP gained in each region.")
        ind_reg_ehp_total = KOTR_update.add_total_row(individual_region_ehp)
        st.dataframe(ind_reg_ehp_total)
    with st.container(border = True):
        st.header("EHP gained in each category.")
        st.dataframe(KOTR_update.add_total_row(individual_ehp))
    


    
    
