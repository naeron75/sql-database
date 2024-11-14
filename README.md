# Olympic Medals Analysis

## Project Overview
This project investigates whether countries perform better when they host the Olympics, examining datasets from 1920 to 2024 with a specific focus on host country medal counts. The analysis is guided by the Host Country Advantage hypothesis, which is significant in the context of future Olympic bids by countries like Germany, Spain, and the UK for the 2040 Games, as well as potential economic and sports investments by these nations.

## Hypothesis
The primary hypothesis is that host countries win more medals in the Olympic Games due to a "home-field advantage."

## Datasets
The project uses two datasets:
- [Paris 2024 Olympic Summer Games](https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games?select=medallists.csv)
- [Olympic Summer & Winter Games, 1896-2022](https://www.kaggle.com/datasets/piterfm/olympic-games-medals-19862018/data?select=olympic_athletes.csv)

Both datasets provide comprehensive information, including host locations, participating countries, athletes, event types, disciplines, and medal counts.

## Project Structure
- Data Cleaning: Code in function.py and main.py covers data cleaning steps for both datasets.
- Database Exploration: SQL queries and insights, along with an ERD, are provided to explore the database structure.
- EDA & Visualisations: Check the Jupyter Notebook for exploratory data analysis and visualisation.
- Presentation: The project slides in the slides folder summarise key insights and findings.

## Analysis Approach

#### 1. Data Cleaning
- Dropped unnecessary columns, standardised country names.
- Consolidated medal counts, distinguishing between team events and individual events to prevent bias in medal totals.
- Merged the two datasets to create a unified structure for analysis.
- Filtered data to include only the years from 1920 to 2024, focusing on a period with more reliable records.

#### 2. Exploratory Data Analysis (EDA)
- Medal Comparison: Analysed medal counts of host countries versus their performance in other years as a percentage of medals won.
- Gold Medal Trends: Focused on gold medals as an indicator of performance, using the same comparison method.
- Historical Distribution: Visualised medal distribution over time, marking years when countries hosted the Games.
- Continental Influence: Investigated whether hosting on the same continent conferred any additional advantages.
- Discipline Analysis: Examined whether certain disciplines showed stronger levarage of the host advantage than others. 

#### 3. Visualisations
- Created bar charts and line graphs to illustrate host country medal trends over time, highlighting the "home advantage" hypothesis.

## Key Findings & Implications
- Host Advantage: The data supports the hypothesis that host countries tend to perform better and win more medals. 
- Implications: Hosting the Olympics can boost the host country's professional sports and infrastructure, potentially trickling down to improve public sports engagement and national health.

## Technologies Used
- Python: For data processing, analysis, and visualisation.
- Pandas: Data manipulation and aggregation.
- Seaborn & Matplotlib: Visualisation to identify trends.
- Jupyter Notebook: Interactive analysis and reporting.
- MySQL: Database creation, SQL queries, and insights.

## Limitations
Sample Size: Limited data points available for certain countries and years, potentially affecting the generalizability of EDA findings.