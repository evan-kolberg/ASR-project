from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import output_file
from datetime import datetime
import sys



def make_chart(uid, average_compute_time, accuracy_percentage):

    output_file(f"accuracy_vs_performance_{uid}.html")


    # Data for the chart
    data = {
        'Average Compute Time (microseconds)': [round(average_compute_time * 1e9, -2)/1000],
        'Accuracy Percentage': [accuracy_percentage]
    }

    source = ColumnDataSource(data=data)

    # Create the figure with Datetime axis type
    p = figure(x_axis_label='Average Compute Time (microseconds)',
               y_axis_label='Accuracy Percentage',
               title='Accuracy vs. Performance',
               sizing_mode='scale_width',  # Use 'scale_width' to fit to the available width
               height=500)  # Set the height of the figure

    # Plot the data
    p.circle('Average Compute Time (microseconds)', 'Accuracy Percentage', size=10, source=source, color='blue', alpha=0.5)

    # Convert the x-axis labels to Datetime format
    p.xaxis.formatter.use_scientific = False
    p.xaxis.major_label_orientation = 45

    # Add hover tool
    hover = HoverTool()
    hover.tooltips = [('Average Compute Time', '@{Average Compute Time (microseconds)}{0.0} microseconds'),
                      ('Accuracy', '@{Accuracy Percentage}%')]
    p.add_tools(hover)

    # Show the chart
    show(p)



if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(1)

    uid, average_compute_time, accuracy_percentage = sys.argv[1:]


    make_chart(uid, float(average_compute_time), float(accuracy_percentage))

    print(f"\tGraph generated in 'accuracy_vs_performance_{uid}.html'\n")



