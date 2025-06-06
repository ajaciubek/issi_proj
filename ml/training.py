from tensorflow import keras
from tensorflow.keras import layers
import joblib
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
import polars as pl
from settings import Settings
from dotenv import load_dotenv
import numpy as np
from sklearn.metrics import classification_report

load_dotenv(dotenv_path="./config/.ml-env")
settings = Settings()

df = pl.read_parquet("./data/pre_processed_data.parquet")
X = df.drop("Role_encoded")
y = df.select("Role_encoded")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

label_encoder = joblib.load(settings.LABEL_MODEL_PATH)
num_classes = len(label_encoder.classes_)

model = keras.Sequential(
    [
        layers.Input(shape=(384,)),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation="sigmoid"),
    ]
)

model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)


early_stop = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)

history = model.fit(
    X_train,
    y_train,
    epochs=200,
    batch_size=64,
    validation_data=(X_test, y_test),
    callbacks=[early_stop],
    verbose=1,
)

y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)

print(classification_report(y_test, y_pred_classes, digits=3))

model.save("./data/job_model.keras")
