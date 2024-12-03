# Empirical Study Based on OpenCollective

This repository contains the code and data for an empirical study examining open-source projects on the OpenCollective platform. The study analyzes various factors that influence the sustainability and funding of open-source projects, with a focus on the relationship between project activity and external sponsorship. The project is structured as follows:

## Folder Structure

### `data/`

Contains raw and processed data files used in the analysis, organized by research question (RQ).

* **`RQ1/`**
  This folder contains data for Research Question 1, focusing on early data collection and exploratory analysis (files in this folder are not specified in this structure but may contain raw data for RQ1).
* **`RQ2/`**
  This folder contains processed data related to Research Question 2, which focuses on the factors that affect project funding on OpenCollective:

  * `data.csv`: A combined dataset for analysis.
  * `oc.csv`: Raw data related to OpenCollective funding.
  * `repo.csv`: Data about repositories associated with OpenCollective projects.
  * `RQ2_data.csv`: Additional processed data for RQ2 analysis.
  * `twitter_info.csv`: Data related to Twitter account information of the projects.
* **`RQ3/`**
  This folder contains data used for Research Question 3, which involves regression analysis to understand the impact of various factors on project donations and activity:

  * **`base_info.csv`** : This is the raw data file containing general information about the projects, which is used as the basis for creating other datasets.
  * **`commit_info.csv`, `issue_info.csv`, `spend_info.csv`** : These files are extracted from `base_info.csv` and contain detailed information about commits, issues, and project spend respectively.
  * **`commit.csv`, `issue.csv`** : These datasets are filtered from `commit_info.csv` and `issue_info.csv` based on specific criteria to isolate relevant entries for further analysis.
  * **`regression_data.csv`** : The final dataset used for regression analysis, combining relevant variables from the various files.
  * **`regression_data_base.csv`** : A version of the regression dataset with additional base information, used as a reference and a foundation for generating the final regression model dataset (`regression_data.csv`).

### `src/`

Contains source code for data collection, preprocessing, and analysis.

* **`data_collect/`**
  Contains scripts for collecting data from various sources, primarily utilizing the GitHub REST API and the Open Collective Public GraphQL API to gather information related to open-source projects, including repository details, commits, issues, and sponsorship data.:
  * `add-dates.py`: Script to add date information to data.
  * `check-repo.py`: Script to check repository data.
  * `extract.py`: General data extraction script.
  * `grab-all-repo.py`: Script to gather all repository data.
  * `grab-commit.py`: Script to collect commit data.
  * `grab-detail.py`: Collects detailed project information.
  * `grab-issue.py`: Script for gathering issue data.
  * `grab-oc.py`: Collects OpenCollective-related data.
  * `statis.py`: Performs statistical analysis on the collected data.
* **`RQ2/`**
  Contains scripts for preprocessing and merging data for Research Question 2:
  * `data_preprocess.py`: Preprocesses data for RQ2 analysis.
  * `filter_twitter.py`: Filters and processes Twitter-related data for projects.
  * `merge_data.py`: Merges various datasets for RQ2 analysis.
* **`RQ3/`**
  Contains scripts for preprocessing and analysis related to Research Question 3:
  * `data_preprocess.py`: Prepares data for RQ3 analysis.
  * `generate_graph.ipynb`: Jupyter notebook for generating graphs related to RQ3.
  * `mergeSponsor.py`: Merges sponsor-related data for analysis.
  * `modifyDataForAnalysis.py`: Prepares the data for regression analysis in RQ3.

## Installation

To get started, clone the repository and install the necessary dependencies.

<pre class="!overflow-visible"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary dark:bg-gray-950"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none">bash</div><div class="sticky top-9 md:top-[5.75rem]"><div class="absolute bottom-0 right-2 flex h-9 items-center"><div class="flex items-center rounded bg-token-sidebar-surface-primary px-2 font-sans text-xs text-token-text-secondary dark:bg-token-main-surface-secondary"><span class="" data-state="closed"><button class="flex gap-1 items-center select-none py-1"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path></svg>复制代码</button></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">git clone https://github.com/your-repository-url
cd Empirical_study_based_on_Opencollective
pip install -r requirements.txt
</code></div></div></pre>

## Usage

* Run the scripts in `src/data_collect/` to collect raw data from different sources.
* Use the scripts in `src/RQ2/` and `src/RQ3/` to preprocess and analyze the data for the respective research questions.
* The data is stored in the `data/` folder, and the results are saved to CSV files.
