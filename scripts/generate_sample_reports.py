from pathlib import Path

import pandas as pd

from datareport.descriptive_report import render_report

sample_folder = Path(Path().absolute().parent, 'sample_reports', 'titanic')
sample_data = Path(Path().absolute().parent, 'data', 'titanic', 'train.csv')

df = pd.read_csv(sample_data)
output_fmt = ['html', 'txt', 'md']

for fmt in output_fmt:
    render_report(df, report_file=Path(sample_folder, f"report_titanic.{fmt}"))
