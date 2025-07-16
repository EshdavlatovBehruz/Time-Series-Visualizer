import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

low_percent = df["value"].quantile(0.025)
high_percent = df["value"].quantile(0.975)
df = df[(df["value"] >= low_percent) & (df["value"] <= high_percent)]

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(df.index, df["value"], color="green", linewidth=0.5)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig("line_plot.png")
    return fig

def draw_bar_plot():
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month_name()

    df_group = df_bar.groupby(["year", "month"])["value"].mean().unstack()

    fig = df_group.plot(kind="bar", figsize=(10, 8)).figure

    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    plt.tight_layout()

    fig.savefig("bar_plot.png")
    return fig

def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")
    df_box["month_num"] = df_box["date"].dt.month
    df_box = df_box.sort_values("month_num")

    fig, axes = plt.subplots(1,2, figsize=(15,6))

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxenplot(x = "month", y = "value", data=df_box, ax=axes[1],
        order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig("box_plot.png")
    return fig



result1 = draw_line_plot()
result2 = draw_bar_plot()
result3 = draw_box_plot()
plt.show()