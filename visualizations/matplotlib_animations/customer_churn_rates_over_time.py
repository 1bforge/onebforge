import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import io

# Generate artificial data
np.random.seed(0)
months = [
    'Jan', 'Feb', 'Mar', 
    'Apr', 'May', 'Jun', 
    'Jul', 'Aug', 'Sep', 
    'Oct', 'Nov', 'Dec'
]
years = np.arange(2010, 2024)
data = np.random.rand(len(years), len(months))

# Create DataFrame
df = pd.DataFrame(data, index=years, columns=months)

# Function to update horizontal histogram
def update(frame):
    ax.clear()
    frame_data = df.iloc[frame, :]
    ax.barh(months, frame_data, color='skyblue')
    ax.set_title("Customer Churn Rates Over Time", fontdict={'fontsize': 16, 'fontweight': 'bold'})
    ax.set_xlabel(f"{df.iloc[frame, :].name}", fontdict={'fontsize': 12, 'fontweight': 'normal'})
    ax.set_ylabel("Month", fontdict={'fontsize': 12, 'fontweight': 'normal'})
    ax.set_xlim(0, 1)
    plt.tight_layout()

# Create figure and axes
fig, ax = plt.subplots(dpi=400)

# Create animated horizontal histogram
ani = FuncAnimation(
    fig, 
    update, 
    frames=len(df), 
    repeat=False
)

# Save animation frames as GIF
frames = []
for i in range(len(df)):
    update(i)
    # Convert the current figure to an image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    frames.append(Image.open(buf))
    print(f"Frame {i+1}/{len(df)} generated.")

# Save frames as GIF
frames[0].save(
    './data/output_data/customer_churn_rates_over_time_histogram.gif', 
    format='GIF', 
    append_images=frames[1:], 
    save_all=True, 
    duration=500, 
    loop=0

)
print("GIF saved successfully.")
