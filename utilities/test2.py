graph_info = {}
graph_info["errors"] = range(10)
error_details = "<table>\n<tr><td>Occurrences</td><td>Description</td></tr>\n"
for error in graph_info["errors"]:
    error_details += "<tr><td>{0}</td><td>{0}</td></tr>\n".format(error)
error_details += "</table>"
print error_details