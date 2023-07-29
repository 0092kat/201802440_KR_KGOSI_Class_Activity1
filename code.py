import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics
import matplotlib.pyplot as plt

df_raw = pd.read_csv("data.csv", sep=";")

df = df_raw.melt(id_vars=["H03", "H05", "H16"],
                 var_name="Date", value_name="sales")

df[["Prefix", "Month", "Year"]] = df["Date"].astype(
    "str").str.extract(r'(MO)(\d{2})(\d{4})')

df["date"] = pd.to_datetime(df["Year"].astype(
    str)+"-"+df["Month"].astype(str)+"-"+"01", format="%Y-%m-%d")

df.drop(columns=["Date", "Prefix", "Month", "Year"], inplace=True)
print(df.head())

# Convert categorical variable into dummy/indicator variables
df_encoded = pd.get_dummies(df, columns=['date', 'H03', 'H05', 'H16'])

# Splitting the data into features and target variable
X = df_encoded.drop('sales', axis=1)
y = df_encoded['sales']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0)

# Creating the RandomForestRegressor model and fitting the data
model = GradientBoostingRegressor(learning_rate=0.1, random_state=0)

model.fit(X_train, y_train)

# Predicting the target variable for the test set
y_pred = model.predict(X_test)

r2_score = metrics.r2_score(y_test, y_pred)
print("R2 Score:", r2_score)

# Writing the result to a file
with open('results.txt', 'w') as f:
    f.write(f"R2 Score: {r2_score}\n")

# Create a scatter plot of actual vs. predicted values
plt.scatter(y_test, y_pred)
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Actual vs. Predicted Values")

# Save the plot as 'actual_vs_predicted.png'
plt.savefig('actual_vs_predicted.png')

# Show the plot (optional)
plt.show()
