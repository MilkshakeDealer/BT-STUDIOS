import matplotlib
matplotlib.use("TkAgg")
import pandas as pd
import re
import matplotlib.pyplot as plt

rows = []

with open("logg2.txt", "r") as file:
    for line in file:
        match = re.search(
            r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}).*?"
            r"Temp:\s*([\d.]+).*?"
            r"Light:\s*([\d.]+).*?"
            r"Sound:\s*([\d.]+)",
            line
        )
        if match:
            rows.append({
                "time": match.group(1),
                "temperature": float(match.group(2)),
                "light": float(match.group(3)),
                "sound": float(match.group(4))
            })

df = pd.DataFrame(rows)

df["time"] = pd.to_datetime(df["time"])
df["date"] = df["time"].dt.date
df["hour"] = df["time"].dt.hour
df["weekday"] = df["time"].dt.weekday  # 0 = Monday

# Filtrera måndag–fredag
df = df[df["weekday"] < 5]

hourly = (
    df
    .groupby(["date", "hour"])
    .mean(numeric_only=True)
    .reset_index()
)

# Medelvärde per timme
mean_hourly = hourly.groupby("hour").mean(numeric_only=True).reset_index()

# ---- Temperatur ----
plt.figure(figsize=(10,6))

for date, day_data in hourly.groupby("date"):
    plt.plot(day_data["hour"], day_data["temperature"], label=str(date))

plt.plot(mean_hourly["hour"], mean_hourly["temperature"], linewidth=3, label="Average")

plt.title("Temperature (Mon–Fri)")
plt.xlabel("Hour of Day")
plt.ylabel("Temp (°C)")
plt.xlim(0,23)
plt.legend()
plt.show()

# ---- Ljus ----
plt.figure(figsize=(10,6))

for date, day_data in hourly.groupby("date"):
    plt.plot(day_data["hour"], day_data["light"], label=str(date))

plt.plot(mean_hourly["hour"], mean_hourly["light"], linewidth=3, label="Average")

plt.title("Light (Mon–Fri)")
plt.xlabel("Hour of Day")
plt.ylabel("Light (lx)")
plt.xlim(0,23)
plt.legend()
plt.show()

# ---- Ljud ----
plt.figure(figsize=(10,6))

for date, day_data in hourly.groupby("date"):
    plt.plot(day_data["hour"], day_data["sound"], label=str(date))

plt.plot(mean_hourly["hour"], mean_hourly["sound"], linewidth=3, label="Average")

plt.title("Sound (Mon–Fri)")
plt.xlabel("Hour of Day")
plt.ylabel("Sound (dB)")
plt.xlim(0,23)
plt.legend()
plt.show()