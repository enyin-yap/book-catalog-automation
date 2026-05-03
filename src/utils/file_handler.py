import pandas as pd
from utils.excel_styles import get_formats
from pipeline.insights import compute_data_quality_score


def read_input_csv(path):
    
    # Read input CSV and return dataframe
    df = pd.read_csv(path, dtype={"isbn": str})

    return df


def extract_isbn_list(df):
    
    # Extract ISBN list from dataframe
    return df["isbn"].dropna().astype(str).tolist()


def update_row_metadata(row, metadata):
    
    # Update dataframe row with fetched metadata
    if metadata.get("title"):
        row["title"] = metadata["title"]

    if metadata.get("author"):
        row["author"] = metadata["author"]

    if metadata.get("pages"):
        row["pages"] = metadata["pages"]

    if metadata.get("publisher"):
        row["manufacturer"] = metadata["publisher"]

    if metadata.get("publish_date"):
        row["publisher_date"] = metadata["publish_date"]

    if metadata.get("description"):
        row["description"] = metadata["description"]

    if metadata.get("price"):
        row["price (TWD)"] = metadata["price"]
    
    return row


def save_output_excel(df, path, insights_df=None):

    df = compute_data_quality_score(df.copy())
    
    df = df.rename(columns={
    "price": "price (TWD)"
    })

    book_columns = [
        "isbn",
        "price (TWD)",
        "title",
        "author",
        "pages",
        "publisher_date",
        "manufacturer",
        "data_quality_score",
        "description"
    ]

    other_columns = [col for col in df.columns if col not in book_columns]

    # combine
    column_order = other_columns + book_columns

    df = df[column_order]

    # df.to_excel(path, index=False)

    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        
        # Books_Info Sheet
        df.to_excel(writer, index=False, sheet_name="Books_Info")
        
        workbook = writer.book 
        books_ws = writer.sheets["Books_Info"]

        formats = get_formats(workbook)
        
        books_ws.set_row(0, 30)  

        for row in range(1, len(df) + 1):
            books_ws.set_row(row, 50) 

        for col_num, col_name in enumerate(df.columns): 
            books_ws.write(0, col_num, col_name, formats["header"]) # first row

        
        for i, col in enumerate(df.columns):

            if col in ["isbn", "conditions"]:
                cell_format = formats["center"]

            elif col in ["description"]:
                cell_format = formats["wrap_top"]

            elif col in ["title", "author", "manufacturer"]:
                cell_format = formats["wrap_middle"]

            elif col == "price (TWD)":
                cell_format = formats["price"]
            
            elif col == "data_quality_score":   
                cell_format = formats["center"]

            else:
                cell_format = formats["left"]

            if col in ["description"]:
                max_len = 25

            elif col in ["title", "author", "manufacturer"]:
                max_len = 15

            elif col == "price (TWD)":
                max_len = 12

            else:
                # text_len = df[col].apply(lambda x: len(str(x)) if pd.notna(x) else 0).max()
                text_len = df[col].fillna("").astype(str).map(len).max()
                max_len = min(max(text_len, len(str(col))) + 2, 20)

            books_ws.set_column(i, i, max_len, cell_format)

        books_ws.freeze_panes(1, 1) 

        books_ws.autofilter(0, 0, df.shape[0], df.shape[1] - 1)

        # heatmap
        if "data_quality_score" in df.columns:
            score_col_idx = df.columns.get_loc("data_quality_score")

            books_ws.conditional_format(
                1, score_col_idx, df.shape[0], score_col_idx,
                {
                    "type": "3_color_scale",
                    "min_color": "#EC8081",
                    "mid_color": "#F9E998",
                    "max_color": "#7FDD98"
                }
            )

        if insights_df is not None and not insights_df.empty:

            # Insights Sheet
            insights_df.to_excel(writer, sheet_name="Insights", index=False)

            insights_ws = writer.sheets["Insights"]

            insights_ws.set_column(0, 0, 30, formats["insight_metric"])
            insights_ws.set_column(1, 1, 15, formats["insight_value"])

            for col_num, col_name in enumerate(insights_df.columns):
                insights_ws.write(0, col_num, col_name, formats["header"])

            insights_ws.set_row(0, 25)
            
            for row in range(1, len(insights_df) + 1):
                insights_ws.set_row(row, 30)

            insights_ws.freeze_panes(1, 0) 


            # create bar chart
            chart_bar = workbook.add_chart({'type': 'column'})

            missing_metrics = [
                "Missing Title %",
                "Missing Author %",
                "Missing Price %",
                "Missing Publish Date %"
            ]

            metrics = insights_df["Metric"].tolist()


            def find_row(metric_name):
                if metric_name in metrics:
                    return metrics.index(metric_name) + 1  # +1 for Excel row offset
                return None

            rows = [find_row(m) for m in missing_metrics]
            rows = [r for r in rows if r is not None]

            if rows:

                start_row = min(rows)
                end_row = max(rows)

                chart_bar.add_series({
                    'name': 'Missing Data %',
                    'categories': [
                        'Insights', start_row, 0,
                        end_row, 0
                    ],
                    'values': [
                        'Insights', start_row, 1,
                        end_row, 1
                    ],
                })

                chart_bar.set_title({'name': 'Missing Data Overview'})
                chart_bar.set_x_axis({'name': 'Fields'})
                chart_bar.set_y_axis({'name': 'Percentage (%)'})
                chart_bar.set_style(10)

                insights_ws.insert_chart('D2', chart_bar)


       # Data Issues Sheet
        issue_cols = ["title", "author", "pages", "price (TWD)", "publisher_date", "manufacturer", "description"]
        existing_issue_cols = [c for c in issue_cols if c in df.columns]

        if existing_issue_cols:

            issues_df = df[df[existing_issue_cols].isna().any(axis=1)].copy()

            if not issues_df.empty:

                def get_missing_fields(row):
                    return ", ".join([col for col in existing_issue_cols if pd.isna(row[col])])

                issues_df["missing_fields"] = issues_df.apply(get_missing_fields, axis=1)

                
                for col in existing_issue_cols:
                    issues_df[col] = issues_df[col].apply(
                        lambda x: "✗" if pd.isna(x) else "✓"
                    )

                display_cols = ["isbn"] + existing_issue_cols + ["missing_fields"]
                display_cols = [c for c in display_cols if c in issues_df.columns]

                issues_df = issues_df[display_cols]

                issues_df.to_excel(writer, sheet_name="Data_Issues", index=False, header=False)
                
                issues_ws = writer.sheets["Data_Issues"]

                # Header
                for col_num, col_name in enumerate(issues_df.columns):
                    issues_ws.write(0, col_num, col_name, formats["header"])

                issues_ws.set_row(0, 30)  
                issues_ws.freeze_panes(1, 1)

                for row in range(1, len(issues_df) + 1):
                    issues_ws.set_row(row, 25)

                for col_idx, col_name in enumerate(issues_df.columns):

                    if col_name == "missing_fields":
                        width = 20

                    elif col_name in ["isbn", "title"]:
                        width = 15

                    elif col_name in existing_issue_cols:
                        width = 15

                    else:
                        width = 15

                    if col_name == "missing_fields":
                        cell_format = formats["wrap_top"]
                    else:
                        cell_format = formats["center"]

                    issues_ws.set_column(col_idx, col_idx, width, cell_format)

                for col_idx, col_name in enumerate(issues_df.columns):
                    if col_name in existing_issue_cols:
                        issues_ws.conditional_format(
                            1, col_idx, len(issues_df), col_idx,
                            {
                                "type": "text",
                                "criteria": "containing",
                                "value": "✗",
                                "format": formats["issues_cross"]
                            }
                        )

                        issues_ws.conditional_format(
                            1, col_idx, len(issues_df), col_idx,
                            {
                                "type": "text",
                                "criteria": "containing",
                                "value": "✓",
                                "format": formats["issues_check"]
                            }
                        )


        # Top / Bottom Books Sheet
        if "data_quality_score" in df.columns:

            key_cols = [
                "isbn",
                "title",
                "author",
                "price (TWD)",
                "publisher_date",
                "data_quality_score"
            ]

            key_cols = [c for c in key_cols if c in df.columns]

            top_books = (
                df.sort_values("data_quality_score", ascending=False)
                .head(10)[key_cols]
                .copy()
            )
            top_books["category"] = "Top 10"

            bottom_books = (
                df.sort_values("data_quality_score", ascending=True)
                .head(10)[key_cols]
                .copy()
            )
            bottom_books["category"] = "Bottom 10"

            combined = pd.concat([top_books, bottom_books])

            combined.to_excel(writer, sheet_name="Quality_Ranking", index=False, header=False)

            ranking_ws = writer.sheets["Quality_Ranking"]

            for col_num, col_name in enumerate(combined.columns):
                ranking_ws.write(0, col_num, col_name, formats["header"])

            ranking_ws.set_row(0, 30)

            for row in range(1, len(combined) + 1):
                ranking_ws.set_row(row, 25)

            for col_idx, col_name in enumerate(combined.columns):

                if col_name == "isbn":
                    width = 18
                    cell_format = formats["center"]

                elif col_name in ["title", "author"]:
                    width = 25
                    cell_format = formats["wrap_middle"]

                elif col_name == "price (TWD)":
                    width = 12
                    cell_format = formats["price"]

                elif col_name == "data_quality_score":
                    width = 18
                    cell_format = formats["center"]

                elif col_name == "category":
                    width = 12
                    cell_format = formats["center"]

                else:
                    width = 18
                    cell_format = formats["center"]

                ranking_ws.set_column(col_idx, col_idx, width, cell_format)

            ranking_ws.freeze_panes(1, 0)

            # Enable filter 
            ranking_ws.autofilter(0, 0, combined.shape[0], combined.shape[1] - 1)