# GPT-5-Probabilistic-Reasoning-Study
This repository contains all materials, data, prompts, and analysis scripts used in the project **GPT‑5 Probabilistic Reasoning**.  
It is organized to support full computational reproducibility of the GPT‑5 simulations and statistical analyses reported in the manuscript.

## Overview
This project evaluates probabilistic coherence and fallacy patterns (conjunction, disjunction, and complementarity) in GPT-5 under two experimental conditions:

- **Past-Election Condition (2020 framing; outcome historically known)**  
- **Future-Election Condition (2028 framing; outcome unresolved)**

GPT-5 was conditioned on demographic personas identical to the human participant profiles reported in Huang et al. (2025), and was asked the same probabilistic judgment questions used in that study.

## Repository Structure

```
GPT-5-Probabilistic-Reasoning/
│
├── data/                     
│   Processed datasets used in the R analysis.
│   Includes GPT-5 outputs and human data from Huang et al. (2025).
│
├── data_gpt_raw/             
│   Raw GPT-5 output files (CSV).
│
├── demographics/             
│   Persona profiles used for GPT-5 simulations.
│   These correspond to the demographic structure of the human
│   participants reported in Huang et al. (2025).
│
│   ├── demographics_T1CL_2020.txt
│   ├── demographics_T2CL_2020.txt
│   ├── demographics_T1CL_2028.txt
│   └── demographics_T2CL_2028.txt
│
├── questions/                
│   Probabilistic judgment questions administered to GPT-5.
│   These correspond to the question structure used in
│   Huang et al. (2025).
│
│   ├── questions_T1CL_2020.txt
│   ├── questions_T2CL_2020.txt
│   ├── questions_T1CL_2028.txt
│   └── questions_T2CL_2028.txt
│
├── python/                   
│   Scripts used to generate GPT-5 responses.
│
│   ├── collect_gpt_2020.py
│   └── collect_gpt_2028.py
│
├── figures/                  
│   Figures generated from the R analysis.
│
├── GPT-5-Probabilistic-Reasoning.Rmd   
│   Full R Markdown analysis pipeline.
│
├── requirements.txt          
│   Python dependencies required to run the scripts.
│
├── .env.example              
│   Template for setting up the OpenAI API key locally.
│
└── .gitignore                
│   Prevents sensitive files (e.g., API keys) from being uploaded.
```

## Running the Python Scripts

1. Install dependencies
```{r}
   pip install -r requirements.txt
```
3. Create a .env file based on .env.example and add your OpenAI API key.
4. Run the scripts
```{r}
   python python/collect_gpt_2020.py
   python python/collect_gpt_2028.py
```

## Reproducing the Statistical Analysis

1. Open the repository as an RStudio Project.
2. Restart the R session.
3. Open GPT-5-Probabilistic-Reasoning.Rmd.
4. Click Knit or Run All.

All figures and statistical outputs reported in the manuscript will be reproduced automatically.

## Use of Huang et al. (2025) Materials

This project builds upon the experimental design reported in:

Huang, J., Busemeyer, J. R., Ebelt, Z., & Pothos, E. M. (2025).  
*Bridging the gap between subjective probability and probability judgments: The quantum sequential sampler.*  
Psychological Review, 132(4), 916–955.  
https://doi.org/10.1037/rev0000489

Specifically:

- The demographic structure used for GPT-5 persona conditioning mirrors the participant demographics reported in Huang et al. (2025).
- The probabilistic judgment questions correspond to those used in Huang et al. (2025).
- Human data from Huang et al. (2025) are included for comparative analysis and are properly credited.

All credit for the original human data and experimental design belongs to Huang et al. (2025).

## Required R Packages

The analysis requires the following R packages:

- effsize  
- patchwork  
- readxl  
- ggplot2  
- dplyr  
- tidyr  
- tidyverse
- here  

If any are missing, install them using:

```r
install.packages(c(
  "effsize", "patchwork", "readxl", "ggplot2",
  "dplyr", "tidyr", "tidyverse", "here"
))
```

