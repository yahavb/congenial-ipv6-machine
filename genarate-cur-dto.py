import pandas as pd
import matplotlib.pyplot as plt
#sample data
#"dayhour","operation","instance_id","usage"
#"2024-10-24 17:00:00","InterZone-In","i-03f59dfc731715c47","0.001056687"
file_path = './cur-dto-ipv6-ipv4-usage-sample.csv'
data = pd.read_csv(file_path)

data['dayhour'] = pd.to_datetime(data['dayhour'])

grouped_usage = data.groupby(['dayhour', 'operation'])['usage'].sum().unstack()

plt.figure(figsize=(10, 6))
grouped_usage.plot(ax=plt.gca())
plt.title("Usage by dayhour and line_item_operation")
plt.xlabel("Time")
plt.ylabel("Total Usage")
plt.legend(title="Operation", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
