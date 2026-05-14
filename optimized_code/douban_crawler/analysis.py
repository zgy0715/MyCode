"""豆瓣电影数据分析和可视化模块"""

import os
import glob
import logging
import pandas as pd
from pyecharts.charts import Bar, Pie, Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType

logger = logging.getLogger(__name__)


def load_latest_csv(output_dir="output"):
    """加载 output 目录下最新的 CSV 文件"""
    csv_files = glob.glob(os.path.join(output_dir, "douban_top250_*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"在 {output_dir}/ 下未找到 CSV 文件，请先运行爬虫")
    latest = max(csv_files, key=os.path.getmtime)
    logger.info(f"加载数据: {latest}")
    df = pd.read_csv(latest)
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["rating_num"] = pd.to_numeric(df["rating_num"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    return df


def basic_stats(df: pd.DataFrame):
    """打印基本统计信息"""
    print("=" * 50)
    print("【基本统计】")
    print(f"总电影数: {len(df)}")
    print(f"评分范围: {df['score'].min():.1f} ~ {df['score'].max():.1f}")
    print(f"平均评分: {df['score'].mean():.2f}")
    print(f"评分中位数: {df['score'].median():.2f}")
    print(f"年代范围: {int(df['year'].min())} ~ {int(df['year'].max())}")
    print(f"评分人数最多: {df.loc[df['rating_num'].idxmax(), 'title']} "
          f"({int(df['rating_num'].max())} 人)")
    print("=" * 50)


def chart_score_distribution(df: pd.DataFrame, output_dir="output"):
    """评分分布直方图"""
    bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    labels = [f"{i}-{i+1}" for i in range(10)]
    df["score_bin"] = pd.cut(df["score"], bins=bins, labels=labels, right=False)
    dist = df["score_bin"].value_counts().sort_index()

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="900px", height="500px"))
        .add_xaxis(dist.index.tolist())
        .add_yaxis("电影数量", dist.values.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="豆瓣 Top250 评分分布"),
            xaxis_opts=opts.AxisOpts(name="评分区间"),
            yaxis_opts=opts.AxisOpts(name="电影数量"),
        )
    )
    path = os.path.join(output_dir, "score_distribution.html")
    bar.render(path)
    logger.info(f"评分分布图已保存: {path}")


def chart_year_distribution(df: pd.DataFrame, output_dir="output"):
    """电影年代分布"""
    decade = (df["year"] // 10 * 10).dropna().astype(int).value_counts().sort_index()

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="900px", height="500px"))
        .add_xaxis(decade.index.astype(str).tolist())
        .add_yaxis("电影数量", decade.values.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="豆瓣 Top250 年代分布"),
            xaxis_opts=opts.AxisOpts(name="年代"),
            yaxis_opts=opts.AxisOpts(name="电影数量"),
        )
    )
    path = os.path.join(output_dir, "year_distribution.html")
    bar.render(path)
    logger.info(f"年代分布图已保存: {path}")


def chart_top_genres(df: pd.DataFrame, output_dir="output", top_n=10):
    """电影类型统计 Top-N"""
    genres_series = df["genres"].dropna().str.split(r"[/、,，]").explode().str.strip()
    genres_series = genres_series[genres_series != ""]
    top_genres = genres_series.value_counts().head(top_n)

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="900px", height="500px"))
        .add_xaxis(top_genres.index.tolist())
        .add_yaxis("电影数量", top_genres.values.tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"豆瓣 Top250 电影类型 Top{top_n}"),
            xaxis_opts=opts.AxisOpts(name="类型", axislabel_opts=opts.LabelOpts(rotate=30)),
            yaxis_opts=opts.AxisOpts(name="电影数量"),
        )
    )
    path = os.path.join(output_dir, "top_genres.html")
    bar.render(path)
    logger.info(f"类型统计图已保存: {path}")


def chart_region_distribution(df: pd.DataFrame, output_dir="output"):
    """地区分布饼图"""
    region_counts = df["region"].value_counts()

    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="900px", height="600px"))
        .add(
            series_name="地区",
            data_pair=[list(x) for x in region_counts.items()],
            radius=["40%", "60%"],
            center=["80%", "70%"],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="豆瓣 Top250 地区分布", pos_left="70%", pos_top="30%"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="left"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    path = os.path.join(output_dir, "region_distribution.html")
    pie.render(path)
    logger.info(f"地区分布图已保存: {path}")


def chart_top10_movies(df: pd.DataFrame, output_dir="output"):
    """评分 Top10 电影"""
    top10 = df.nlargest(10, "score")[["title", "score", "year"]]

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="900px", height="500px"))
        .add_xaxis(top10["title"].tolist())
        .add_yaxis("评分", top10["score"].tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="豆瓣 Top250 评分 Top10"),
            xaxis_opts=opts.AxisOpts(
                name="电影",
                axislabel_opts=opts.LabelOpts(rotate=30, font_size=10),
            ),
            yaxis_opts=opts.AxisOpts(name="评分", max_=10),
        )
    )
    path = os.path.join(output_dir, "top10_movies.html")
    bar.render(path)
    logger.info(f"Top10 电影图已保存: {path}")


def chart_top_rated_movies(df: pd.DataFrame, output_dir="output"):
    """评分人数 Top10 电影（横向条形图）"""
    top10 = df.nlargest(10, "rating_num")[["title", "rating_num", "score"]]

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="900px", height="500px"))
        .add_xaxis(top10["title"].tolist())
        .add_yaxis("评分人数", top10["rating_num"].tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="豆瓣 Top250 评分人数 Top10"),
            xaxis_opts=opts.AxisOpts(name="评分人数"),
            yaxis_opts=opts.AxisOpts(
                name="电影",
                axislabel_opts=opts.LabelOpts(font_size=10),
            ),
        )
    )
    path = os.path.join(output_dir, "top_rated_movies.html")
    bar.render(path)
    logger.info(f"评分人数 Top10 图已保存: {path}")


def chart_year_trend(df: pd.DataFrame, output_dir="output"):
    """每年平均评分趋势"""
    yearly = df.groupby("year")["score"].mean().dropna()

    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="900px", height="500px"))
        .add_xaxis(yearly.index.astype(int).astype(str).tolist())
        .add_yaxis(
            "平均评分",
            yearly.round(2).tolist(),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最高"),
                    opts.MarkPointItem(type_="min", name="最低"),
                ]
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="每年上榜电影的平均评分趋势"),
            xaxis_opts=opts.AxisOpts(name="年份", axislabel_opts=opts.LabelOpts(rotate=45)),
            yaxis_opts=opts.AxisOpts(name="平均评分", min_=0, max_=10),
        )
    )
    path = os.path.join(output_dir, "year_trend.html")
    line.render(path)
    logger.info(f"年度评分趋势图已保存: {path}")


def run_all_analyses(output_dir="output"):
    """运行所有分析和可视化"""
    os.makedirs(output_dir, exist_ok=True)

    df = load_latest_csv(output_dir)
    basic_stats(df)

    print("\n生成可视化图表 ...")
    chart_score_distribution(df, output_dir)
    chart_year_distribution(df, output_dir)
    chart_top_genres(df, output_dir)
    chart_region_distribution(df, output_dir)
    chart_top10_movies(df, output_dir)
    chart_top_rated_movies(df, output_dir)
    chart_year_trend(df, output_dir)

    print(f"\n所有图表已保存到 {output_dir}/ 目录，用浏览器打开 .html 文件查看。")
