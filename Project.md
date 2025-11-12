# **Project Documentation: Multi-Task Deep Learning for Soccer Match Prediction**

**Version:** 1.1
**Date:** October 26, 2023

## 1. Executive Summary

This project aims to develop a sophisticated deep learning model for predicting the outcomes of soccer matches. The model will leverage a wide array of pre-match and in-play data, including a novel approach that treats betting odds as both continuous numerical features and discrete categorical features simultaneously.

Two distinct predictive models will be developed:
1.  **Scenario 1 (Pre-Match):** Predicts both half-time and full-time outcomes using only data available before the match begins.
2.  **Scenario 2 (In-Play):** Predicts the final match outcome using all pre-match data plus the known state of the game at halftime.

The core of the project is a **Multi-Input, Multi-Output Neural Network** that utilizes Multi-Task Learning to predict several related targets from a single, unified architecture.

## 2. Problem Statement & Objectives

Standard soccer prediction models often fail to capture the full complexity of the available data. Betting odds, in particular, contain rich information about market sentiment and expected outcomes. This project addresses the following objectives:

*   To build a model that can learn from both the *magnitude* of betting odds (e.g., 1.5 is a stronger favorite than 1.6) and the *identity* of the odds (e.g., specific odds like 2.00 may have unique market psychology).
*   To efficiently predict multiple, related outcomes (match result, goals scored, half-time state) within a single model through Multi-Task Learning.
*   To create a comprehensive feature set by engineering variables that capture team form, market uncertainty, and in-play match dynamics.
*   To produce two distinct, production-ready models for both pre-match and in-play prediction scenarios.

## 3. Methodology: Multi-Input, Multi-Output Neural Network

The chosen architecture is a Keras-based neural network using the Functional API. This design is necessary to accommodate the project's unique requirements.

*   **Multi-Input:** The model has separate input paths to process different types of data appropriately:
    1.  **Dense Input Path:** For all standard numerical and one-hot encoded categorical features. This path learns from scaled, continuous, and binary data.
    2.  **Embedding Input Path(s):** For high-cardinality categorical features like betting odds and half-time scores. An `Embedding` layer learns a dense vector representation for each unique category, capturing complex, non-linear relationships.
*   **Multi-Output:** After the input paths are merged and processed through shared hidden layers, the network branches into multiple "heads," each dedicated to a specific prediction task.
*   **Multi-Task Learning:** By training all heads simultaneously, the model is forced to learn a generalized internal representation of a soccer match that is beneficial for all prediction tasks. This often leads to better performance and regularization than training separate models for each target.

## 4. Data Schema & Variables

The following tables detail every variable used as an input (feature) or output (target) for each scenario.

### **Scenario 1: Pre-Match Prediction Model**

#### **A. Input Variables (Features)**
*(All information is known before kickoff)*

| Category | Variable Name(s) | Model Role |
| :--- | :--- | :--- |
| **1. Core Pre-Match Data** | `[Original_Numerical_Cols]`, `[Original_Categorical_Cols]` | Dense Input |
| **2. Betting Odds** | `HomeOdds`, `DrawOdds`, `AwayOdds` | Dense Input & **Embedding Input** |
| **3. Odds-Derived Signals** | `Prob_H/D/A`, `Margin`, `Entropy`, `Favorite_Odds`, `Mismatch_Ratio` | Dense Input |
| **4. Goal Market Signals** | `Prob_Over2.5`, `Prob_Under2.5`, `Margin_OU2.5`, `Market_Expected_Goals` | Dense Input |
| **5. Team Form (Rolling)** | `Avg_Goals_Scored_Last_N`, `Avg_Goals_Conceded_Last_N`, `Form_Points_Last_N` | Dense Input |
| | `Goal_Diff_Form`, `Points_Diff_Form` | Dense Input |
| **6. Advanced Team Form** | `Form_Consistency_Last_N`, `Weighted_Form_Points_Last_N`, `Clean_Sheet_Ratio_Last_N` | Dense Input |
| **7. H2H Dynamics** | `H2H_Avg_Goal_Diff`, `H2H_Recent_Win_Ratio` | Dense Input |
| **8. Market Volatility** | `Odds_Disagreement` | Dense Input |
| **9. Advanced Context** | `Elo_Difference`, `Days_Since_Last_Match` | Dense Input |

#### **B. Output Variables (Targets)**

| Variable Name | Description | Model Role |
| :--- | :--- | :--- |
| `FT_Result` | Final match result (Home Win, Draw, Away Win). | **Classification Target** |
| `FTHG`, `FTAG` | Final home/away goals. | **Regression Target** |
| `HT_Result` | Half-time result (Home Win, Draw, Away Win). | **Classification Target** |
| `HTHG`, `HTAG` | Half-time home/away goals. | **Regression Target** |

---

### **Scenario 2: In-Play (Halftime) Prediction Model**

#### **A. Input Variables (Features)**
*(Includes all pre-match features plus halftime information)*

| Category | Variable Name(s) | Model Role |
| :--- | :--- | :--- |
| **1-9. All Pre-Match Features** | *(All features from Scenario 1)* | Dense / Embedding Inputs |
| **10. In-Play (Halftime) State** | `HTHG`, `HTAG` | Dense Input |
| | `HT_Score_Encoded` | **Embedding Input** |
| | `HT_Goal_Diff`, `HT_BTTS` | Dense Input |
| | `Favorite_Status_HT` | Dense Input |
| **11. Enhanced In-Play Context** | `Comeback_Status`, `First_Goal_Timing_Bucket` | Dense Input / Embedding Input |

#### **B. Output Variables (Targets)**

| Variable Name | Description | Model Role |
| :--- | :--- | :--- |
| `FT_Result` | Final match result (Home Win, Draw, Away Win). | **Classification Target** |
| `FTHG`, `FTAG` | Final home/away goals. | **Regression Target** |

## 5. Preprocessing & Feature Engineering Pipeline

1.  **Data Loading:** Load data from the source `.xlsx` file.
2.  **Data Cleaning:** Handle missing values (e.g., drop rows).
3.  **Target Engineering:**
    *   Parse score strings (`'2 - 1'`) into `FTHG`, `FTAG`, `HTHG`, `HTAG` integer columns.
    *   Create `FT_Result` and `HT_Result` categorical columns (0=H, 1=D, 2=A).
4.  **Feature Engineering:**
    *   Generate all odds-derived, goal market, and basic team form features.
    *   **Generate advanced features:** Calculate advanced form (consistency, weighted points), H2H dynamics, market volatility, and in-play context variables as detailed in the schema tables.
5.  **Data Splitting:** Split the dataset into training and testing sets (e.g., 80/20 split).
6.  **Input Preprocessing:**
    *   **Numerical Features:** Scale using `StandardScaler`.
    *   **Categorical Features:** Encode using `OneHotEncoder`.
    *   **Embedding Features:** Encode using `LabelEncoder`.
    *   **Important:** All encoders and scalers are to be `fit` only on the training data and `transform` both training and testing data.

## 6. Model Implementation Details

*   **Framework:** TensorFlow / Keras
*   **Optimizer:** `Adam`
*   **Loss Functions:** A dictionary of losses is required for the multi-output structure:
    *   `'categorical_crossentropy'` for classification targets (`FT_Result`, `HT_Result`).
    *   `'poisson'` for regression targets (all goal counts), as it is statistically suited for count data.
*   **Loss Weights:** A dictionary of weights will be used to prioritize the model's focus during training (e.g., assign a higher weight to predicting the `FT_Result` over other targets).
*   **Evaluation Metrics:**
    *   **Classification:** Accuracy, F1-Score, ROC AUC.
    *   **Regression:** Mean Absolute Error (MAE), Root Mean Squared Error (RMSE).

## 7. Project Deliverables

1.  **Source Code:** A well-commented Python script (`.py` or Jupyter Notebook) containing the entire pipeline from data loading to model saving.
2.  **Trained Models:** Saved model files for both Scenario 1 and Scenario 2 (e.g., `pre_match_model.h5`, `in_play_model.h5`).
3.  **Preprocessing Artifacts:** Saved scaler and encoder objects (e.g., `standard_scaler.joblib`, `label_encoders.joblib`) required for making predictions on new data.
4.  **Requirements File:** A `requirements.txt` file listing all necessary Python libraries.
5.  **This Documentation.**

## 8. Future Work & Potential Improvements

*   **Hyperparameter Tuning:** Systematically tune learning rate, layer sizes, dropout, and embedding dimensions using tools like KerasTuner or Optuna.
*   **Alternative Models:** Benchmark the neural network's performance against Gradient Boosting models (especially CatBoost, which excels at handling categorical features).
*   **Expanded Data Sources:** Incorporate additional data such as player-level statistics, weather conditions, or referee data.
*   **Deployment:** Package the trained model and preprocessors into a REST API using a framework like Flask or FastAPI for real-time predictions.
