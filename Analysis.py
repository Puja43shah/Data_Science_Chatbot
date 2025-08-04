import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def process_query(query, df):
    query = query.lower()
    tokens = query.split()
    
    # Enhanced average matching with token overlap
    if "average" in query:
        numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
        matched_cols = []

        for col in numeric_cols:
            col_tokens = col.lower().replace("_", " ").split()
            if any(tok in col_tokens for tok in tokens):
                matched_cols.append(col)

        if matched_cols:
            col = matched_cols[0]
            return f"The average of {col} is {df[col].mean():.2f}"
        else:
            return "Sorry, I couldn't find a numeric column to calculate the average for."

            
    elif "columns" in query:
        return f"Columns in your dataset: {', '.join(df.columns)}"

    elif "shape" in query or "rows" in query:
        return f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns."

    elif "plot" in query:
        col_names = [col for col in df.columns if col.lower() in query] 

        if len(col_names) == 2:
            x, y = col_names
            fig, ax = plt.subplots()

            if "scatter" in query:
                sns.scatterplot(x=x, y=y, data=df, ax=ax)
                ax.set_title(f"{x} vs {y} (Scatter Plot)")

            elif "line" in query:
                sns.lineplot(x=x, y=y, data=df, ax=ax)
                ax.set_title(f"{x} vs {y} (Line Plot)")

            elif "bar" in query:
                sns.barplot(x=x, y=y, data=df, ax=ax)
                ax.set_title(f"{x} vs {y} (Bar Plot)")

            else:
                sns.scatterplot(x=x, y=y, data=df, ax=ax)
                ax.set_title(f"{x} vs {y} (Default: Scatter)")

            st.pyplot(fig)
            return f"Here is the plot of {x} vs {y}."

        elif len(col_names) == 1 and ("hist" in query or "count" in query):
            col = col_names[0]

            fig, ax = plt.subplots()
            if pd.api.types.is_numeric_dtype(df[col]) and "hist" in query:
                sns.histplot(df[col], kde=True, ax=ax)
                ax.set_title(f"Histogram of {col}")
                st.pyplot(fig)
                return f"Here is the histogram of {col}."

            elif "count" in query:
                sns.countplot(x=df[col], ax=ax)
                ax.set_title(f"Countplot of {col}")
                st.pyplot(fig)
                return f"Here is the countplot of {col}."

            else:
                return f"Column '{col}' is not suitable for histogram or countplot."

        else:
            return "Please mention one or two valid column names for plotting."

    elif "help" in query or "how" in query:
        return ("Try things like:\n"
                "- 'scatter plot age vs cholesterol'\n"
                "- 'line plot max_heart_rate vs age'\n"
                "- 'histogram of age'\n"
                "- 'countplot of chest_pain_type'\n"
                "- 'average of age'\n"
                "- 'what is the average cholesterol?'")

    else:
        return "Sorry, I didn't understand that. Try asking about plots, averages, or dataset info."
