__author__ = 'alonsobarquero'
import os
import shutil
import json

from configs.config import LocustConfigs as LC
from configs.config import GlobalConfigs as GC


class ResultAnalysis:
    def compress_chart_dataset(self, dataset):
        size = LC.RESULTS_TS_INTERVAL
        dataset_in_groups = [dataset[i:i + size] for i in xrange(0, len(dataset), size)]
        compressed_dataset = [dataset_in_groups[0][0]]
        for x in xrange(0, len(dataset_in_groups)):
            compressed_dataset.append(dataset_in_groups[x][-1])
        return compressed_dataset

    def get_chart_x_axis(self, datasets_length):
        size = LC.RESULTS_TS_INTERVAL
        legend_split = [range(0, datasets_length)[i:i + size] for i in xrange(0, datasets_length, size)]
        legend = [legend_split[0][0]]
        for x in xrange(0, len(legend_split)):
            legend.append(legend_split[x][-1] + 1)
        return legend

    def result_report(self, path, graph_info):
        html_template = """
<!doctype html>
<html>
<head>
    <title>Line Chart</title>
    <script src="vendor/Chart.js"></script>
</head>
<body>
<div style="width:30%">
    <div>
        <h2>Execution Summary</h2>
        Total succeeded: {}
        Total failures: {}
        Total requests: {}
    </div>
</div>
<div style="width:100%">
    <div>
        <h2>Error Details</h2>
        {}
    </div>
</div>
<div style="width:30%">
    <div>
        <h2>Request / Errors Graph</h2>
        <canvas id="request_error" height="450" width="600"></canvas>
    </div>
</div>
<div style="width:30%">
    <div>
        <h2>Request Response Time</h2>
        <canvas id="request_response_time" height="450" width="600"></canvas>
    </div>
</div>
<div style="width:30%">
    <div>
        <h2>Throughput (Request Per Second)</h2>
        <canvas id="throughput_rps" height="450" width="600"></canvas>
    </div>
</div>

<script>
        var lineChartDataRequestError = {{
            labels : {},
            datasets : [
                {{
                    label: "Requests",
                    fillColor : "rgba(63, 217, 63, 0.2)",
                    strokeColor : "rgba(63, 217, 63, 1)",
                    pointColor : "rgba(63, 217, 63, 1)",
                    pointStrokeColor : "#fff",
                    pointHighlightFill : "#fff",
                    pointHighlightStroke : "rgba(63, 217, 63, 1)",
                    data : {}

                }},
                {{
                    label: "Failed Requests on Ramp-up",
                    fillColor : "rgba(242, 63, 63, 0.2)",
                    strokeColor : "rgba(242, 63, 63, 1)",
                    pointColor : "rgba(242, 63, 63, 1)",
                    pointStrokeColor : "#fff",
                    pointHighlightFill : "#fff",
                    pointHighlightStroke : "rgba(242, 63, 63, 1)",
                    data : {}
                }}
            ]

        }}

        var lineChartDataRequestResponseTime = {{
            labels : {},
            datasets : [
                {{
                    label: "Median Response Time",
                    fillColor : "rgba(0, 0, 0, 0)",
                    strokeColor: "rgba(220,220,220,1)",
                    pointColor: "rgba(220,220,220,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(220,220,220,1)",
                    data : {}
                }},
                {{
                    label: "Max Response Time",
                    fillColor : "rgba(0, 0, 0, 0)",
                    strokeColor : "rgba(242, 63, 63, 1)",
                    pointColor : "rgba(242, 63, 63, 1)",
                    pointStrokeColor : "#fff",
                    pointHighlightFill : "#fff",
                    pointHighlightStroke : "rgba(242, 63, 63, 1)",
                    data : {}
                }},

                {{
                    label: "Average Response",
                    fillColor : "rgba(0, 0, 0, 0)",
                    strokeColor: "rgba(151,187,205,1)",
                    pointColor: "rgba(151,187,205,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(151,187,205,1)",
                    data : {}
                }}
            ]

        }}

        var lineChartDataRPS = {{
            labels : {},
            datasets : [
                {{
                    label: "Throughput RPS",
                    fillColor : "rgba(242, 63, 63, 0.2)",
                    strokeColor : "rgba(242, 63, 63, 1)",
                    pointColor : "rgba(242, 63, 63, 1)",
                    pointStrokeColor : "#fff",
                    pointHighlightFill : "#fff",
                    pointHighlightStroke : "rgba(242, 63, 63, 1)",
                    data : {}
                }}
            ]

        }}
    window.onload = function(){{
        var ctx = document.getElementById("request_error").getContext("2d");
        window.myLine = new Chart(ctx).Line(lineChartDataRequestError, {{
            responsive: false
        }});

        var ctx1 = document.getElementById("request_response_time").getContext("2d");
        window.myLine1 = new Chart(ctx1).Line(lineChartDataRequestResponseTime, {{
            responsive: false
        }});

        var ctx2 = document.getElementById("throughput_rps").getContext("2d");
        window.myLine2 = new Chart(ctx2).Line(lineChartDataRPS, {{
            responsive: false
        }});

     }}

</script>

</body>
</html>
"""
        error_details = "<table>\n<tr><td>Occurrences</td><td>Description</td></tr>\n"
        for error in graph_info["errors"]:
            error_details += "<tr><td>{0}</td><td>{1}</td></tr>\n".format(error["occurences"], error["error"])
        error_details += "</table>"
        print("Creating HTML Report")
        with open("{}/result_report.html".format(path), "w") as f:
            f.write(html_template.format(graph_info["num_requests"],
                                         graph_info["request_failed"],
                                         graph_info["num_requests"] + graph_info["request_failed"],
                                         error_details,
                                         graph_info["x_axis"],
                                         graph_info["num_requests"],
                                         graph_info["request_failed"],
                                         graph_info["x_axis"],
                                         graph_info["median_response_time"],
                                         graph_info["max_response_time"],
                                         graph_info["average_response_time"],
                                         graph_info["x_axis"],
                                         graph_info["request_per_second"],
                                         ))
        print("HTML Report created successfully\n")

        print("Creating graph info file")
        with open("{}/graph_info.txt".format(path), "w") as f:
            f.write(json.dumps(graph_info))
        print("graph info file created successfully\n")

        vendor_folder = "{}/vendor".format(path)
        os.makedirs(vendor_folder)

        print("Copying Chart.js file into vendor folder")
        with open("{}/Chart.js".format(GC.CHART_JS_PATH), "r") as f:
            chart_js = f.readlines()
        with open("{}/Chart.js".format(vendor_folder), "w") as f:
            f.writelines(chart_js)
        print("Chart.js file copied as expected.")

