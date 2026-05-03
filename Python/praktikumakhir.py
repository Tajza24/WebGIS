import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, r2_score

# Judul aplikasi
st.title("Aplikasi Machine Learning untuk Prediksi Kondisi Medis")

# Memuat data
data = pd.read_csv('healthcare_dataset.csv')
st.write("Data yang dimuat:")
st.dataframe(data)

# Memilih kolom target
target_column = st.selectbox("Pilih kolom target:", data.columns)

 # Memisahkan fitur dan target
X = data.drop(target_column, axis=1)
y = data[target_column]

 # Mengubah kategori menjadi numerik
X = pd.get_dummies(X, drop_first=True)

    # Pembagian data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Menyimpan hasil percobaan
results = []

    # Percobaan 1: Logistic Regression
if st.button("Latih Model Logistic Regression"):
    model1 = LogisticRegression(max_iter=1000)
    model1.fit(X_train, y_train)
    y_pred1 = model1.predict(X_test)

    accuracy1 = accuracy_score(y_test, y_pred1)
    report1 = classification_report(y_test, y_pred1, output_dict=True)
    r2_1 = r2_score(y_test, y_pred1)

    results.append({
        'Model': 'Logistic Regression',
        'Akurasi': accuracy1,
        'R² Score': r2_1,
         'Classification Report': report1
    })

    # Percobaan 2: Random Forest
if st.button("Latih Model Random Forest"):
    model2 = RandomForestClassifier(n_estimators=100)
    model2.fit(X_train, y_train)
    y_pred2 = model2.predict(X_test)

    accuracy2 = accuracy_score(y_test, y_pred2)
    report2 = classification_report(y_test, y_pred2, output_dict=True)
    r2_2 = r2_score(y_test, y_pred2)

    results.append({
        'Model': 'Random Forest',
        'Akurasi': accuracy2,
        'R² Score': r2_2,
        'Classification Report': report2
    })

    # Percobaan 3: Support Vector Machine
if st.button("Latih Model Support Vector Machine"):
    model3 = SVC()
    model3.fit(X_train, y_train)
    y_pred3 = model3.predict(X_test)

    accuracy3 = accuracy_score(y_test, y_pred3)
    report3 = classification_report(y_test, y_pred3, output_dict=True)
    r2_3 = r2_score(y_test, y_pred3)

    results.append({
        'Model': 'Support Vector Machine',
        'Akurasi': accuracy3,
        'R² Score': r2_3,
        'Classification Report': report3
    })

    # Menampilkan hasil percobaan
if results:
        st.write("### Hasil Evaluasi Model")
for result in results:
    st.write(f"*Model*: {result['Model']}")
    st.write(f"Akurasi: {result['Akurasi']:.4f}")
    st.write(f"R² Score: {result['R² Score']:.4f}")
    st.write("Classification Report:")
    st.dataframe(pd.DataFrame(result['Classification Report']).transpose())
    st.write("---")