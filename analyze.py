import sqlite3
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
import os

DB_NAME = "jobs.db"
EXCEL_FILE = "job_report.xlsx"

def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()
    return df

def add_avg_salary(df):
    df['avg_salary'] = (df['min_salary'] + df['max_salary']) // 2
    return df

def city_avg_salary(df):
    return df.groupby('city')['avg_salary'].mean().sort_values(ascending=False)

def skill_analysis(df):
    all_skills = []
    for skills in df['skills'].str.split(','):
        if skills:
            all_skills.extend([s.strip() for s in skills])
    skill_series = pd.Series(all_skills).value_counts().head(10)
    return skill_series

def generate_excel_report(df, city_stats, skill_stats):
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
        # Sheet1: 原始数据
        df.to_excel(writer, sheet_name='原始数据', index=False)
        
        # Sheet2: 城市平均薪资
        city_stats.to_excel(writer, sheet_name='城市平均薪资', header=['平均薪资'])
        
        # Sheet3: 技能需求 Top10
        skill_stats.to_excel(writer, sheet_name='技能需求Top10', header=['出现次数'])
        
        # 调整列宽（可选）
        for sheet in writer.sheets.values():
            for column in sheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 30)
                sheet.column_dimensions[column_letter].width = adjusted_width

    print(f"报告已生成：{EXCEL_FILE}")

if __name__ == "__main__":
    df = load_data()
    df = add_avg_salary(df)
    
    city_avg = city_avg_salary(df)
    print("城市平均薪资（从高到低）：")
    print(city_avg)
    
    top_skills = skill_analysis(df)
    print("\n技能需求 Top10：")
    print(top_skills)
    
    generate_excel_report(df, city_avg, top_skills)
    
    print("\n分析完成！")