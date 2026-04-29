def get_formats(workbook):

    return {
        "header": workbook.add_format({
            "bold": True,
            "bg_color": "#dce6f1",
            "font_color": "black",
            "border": 1,
            "align": "center",
            "valign": "middle"
        }),

        "wrap_top": workbook.add_format({
            "text_wrap": True,
            "valign": "top"
        }),

        "wrap_middle": workbook.add_format({
            "text_wrap": True,
            "valign": "middle"
        }),

        "left": workbook.add_format({
            "align": "left",
            "valign": "middle"
        }),

        "center": workbook.add_format({
            "align": "center",
            "valign": "middle"
        }),

        "price": workbook.add_format({
            "num_format": "#0.00",
        }),

        "insight_metric": workbook.add_format({
            "valign": "middle",
        }),

        "insight_value": workbook.add_format({
            "align": "center",
            "valign": "middle",
            "num_format": "0.00"
        })
    }