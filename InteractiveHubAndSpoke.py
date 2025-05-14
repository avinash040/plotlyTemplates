import ipywidgets as widgets
from IPython.display import display, clear_output
import plotly.graph_objects as go
import numpy as np

# Define spoke names and descriptions
spoke_workflows = {
    "Agentic Control Loop": "Perception → Plan → Act → Reflect loop.",
    "Multi-Agent Collaboration": "Multiple agents collaborating toward a shared goal.",
    "Planning and Execution Flow": "Break down a task into subtasks and execute sequentially.",
    "Tool-Enhanced Workflow": "Agent accessing external APIs/tools to augment capabilities.",
    "Memory-Augmented Workflow": "Agent with short-term and long-term memory interacting with environment."
}

# Output widget for displaying detailed views
output = widgets.Output()

# Function to display detailed agent workflow diagram
def show_workflow_diagram(name):
    with output:
        clear_output()
        fig = go.FigureWidget()

        if name == "Agentic Control Loop":
            nodes = ["Perception", "Planning", "Action", "Reflection"]
            edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
        elif name == "Multi-Agent Collaboration":
            nodes = ["User", "Agent A", "Agent B", "Agent C", "Result"]
            edges = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)]
        elif name == "Planning and Execution Flow":
            nodes = ["Goal", "Plan Tasks", "Task 1", "Task 2", "Complete"]
            edges = [(0, 1), (1, 2), (1, 3), (2, 4), (3, 4)]
        elif name == "Tool-Enhanced Workflow":
            nodes = ["Agent", "Tool 1", "Tool 2", "Tool 3", "Output"]
            edges = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)]
        elif name == "Memory-Augmented Workflow":
            nodes = ["Agent", "Short-Term Memory", "Long-Term Memory", "Environment"]
            edges = [(0, 1), (0, 2), (0, 3), (1, 0), (2, 0)]

        num_nodes = len(nodes)
        angle = np.linspace(0, 2 * np.pi, num_nodes, endpoint=False)
        positions = np.array([(np.cos(a), np.sin(a)) for a in angle])

        # Edges
        edge_x, edge_y = [], []
        for start, end in edges:
            x0, y0 = positions[start]
            x1, y1 = positions[end]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines',
                                 line=dict(width=2, color='gray'),
                                 hoverinfo='none'))

        # Nodes with labels BELOW the node
        node_x, node_y = positions[:, 0], positions[:, 1]
        fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text',
                                 marker=dict(size=50, color='orange'),
                                 text=nodes,
                                 textposition="bottom center"))  # 👈 labels below

        fig.update_layout(
            title=name,
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
            height=700,
            width=700,
            font=dict(size=16)
        )
        display(fig)

# Create hub-and-spoke diagram
def create_hub_spoke_diagram():
    hub_name = "Orchestrator Agent"
    num_spokes = len(spoke_workflows)
    angle = np.linspace(0, 2 * np.pi, num_spokes, endpoint=False)
    radius = 2

    spoke_positions = [(radius * np.cos(a), radius * np.sin(a)) for a in angle]
    hub_position = (0, 0)

    fig = go.FigureWidget()

    # Add edges
    for x, y in spoke_positions:
        fig.add_trace(go.Scatter(
            x=[hub_position[0], x],
            y=[hub_position[1], y],
            mode='lines',
            line=dict(color='gray', width=2),
            hoverinfo='skip'
        ))

    # Add hub with label BELOW the hub
    fig.add_trace(go.Scatter(
        x=[hub_position[0]],
        y=[hub_position[1]],
        mode='markers+text',
        marker=dict(size=60, color='blue'),
        text=[hub_name],
        textposition='bottom center',   # 👈 label below hub
        hoverinfo='text'
    ))

    # Add spoke nodes with labels BELOW the nodes
    spoke_x = [pos[0] for pos in spoke_positions]
    spoke_y = [pos[1] for pos in spoke_positions]
    spoke_names = list(spoke_workflows.keys())

    fig.add_trace(go.Scatter(
        x=spoke_x,
        y=spoke_y,
        mode='markers+text',
        marker=dict(size=50, color='orange'),
        text=spoke_names,
        textposition="bottom center",   # 👈 labels below spokes
        hoverinfo='text'
    ))

    fig.update_layout(
        title="AI Agent Workflow Explorer",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        height=700,
        width=700,
        font=dict(size=16)
    )

    # Click callback
    def on_click(trace, points, selector):
        if points.point_inds:
            index = points.point_inds[0]
            if index < len(spoke_names):
                show_workflow_diagram(spoke_names[index])

    fig.data[-1].on_click(on_click)
    return fig

# Display interface
display(widgets.HTML("<h2 style='color:blue'>Agent Workflow Hub & Spoke Explorer</h2>"))
hub_fig = create_hub_spoke_diagram()
display(hub_fig)
display(output)
