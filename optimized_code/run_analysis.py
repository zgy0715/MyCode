"""豆瓣Top250 数据分析与可视化入口

用法:
    python run_analysis.py              # 分析 output/ 下最新 CSV
    python run_analysis.py -f path.csv  # 指定 CSV 文件
"""

import argparse
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())

from douban_crawler.analysis import run_all_analyses


def main():
    parser = argparse.ArgumentParser(description="豆瓣Top250 数据分析与可视化")
    parser.add_argument("-f", "--file", help="指定 CSV 文件路径")
    parser.add_argument("-o", "--output", default="output", help="图表输出目录 (默认: output)")
    args = parser.parse_args()

    if args.file:
        import pandas as pd
        from douban_crawler.analysis import basic_stats, chart_score_distribution, \
            chart_year_distribution, chart_top_genres, chart_region_distribution, \
            chart_top10_movies, chart_top_rated_movies, chart_year_trend

        os.makedirs(args.output, exist_ok=True)
        df = pd.read_csv(args.file)
        basic_stats(df)
        print("\n生成可视化图表 ...")
        chart_score_distribution(df, args.output)
        chart_year_distribution(df, args.output)
        chart_top_genres(df, args.output)
        chart_region_distribution(df, args.output)
        chart_top10_movies(df, args.output)
        chart_top_rated_movies(df, args.output)
        chart_year_trend(df, args.output)
        print(f"\n所有图表已保存到 {args.output}/ 目录")
    else:
        run_all_analyses(args.output)


if __name__ == "__main__":
    main()
