__author__ = 'alonsobarquero'
import os
import shutil
import json

from configs.config import LocustConfigs as LC


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

    def final_report(self, path, graph_info):
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
        Total requests: {}
        Total failures: {}
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
        with open("{}/final_report.html".format(path), "w") as f:
            f.write(html_template.format(graph_info["num_requests"][-1],
                                         graph_info["request_failed"][-1],
                                         graph_info["x_axis"],
                                         graph_info["num_requests"],
                                         graph_info["request_failed"],
                                         graph_info["x_axis"],
                                         graph_info["median_response_time"],
                                         graph_info["max_response_time"],
                                         graph_info["average_response_time"],
                                         graph_info["x_axis"],
                                         graph_info["request_per_second"]
                                         ))

        with open("{}/graph_info.txt".format(path), "w") as f:
            f.write(json.dumps(graph_info))
        vendor_folder = "{}/vendor".format(path)
        os.makedirs(vendor_folder)
        shutil.copyfile("result_report_mockup/Chart.js", "{}/Chart.js".format(vendor_folder))


