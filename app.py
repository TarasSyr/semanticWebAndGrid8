from flask import Flask, request, render_template
from rdflib import Graph, URIRef, Literal
from igraph import Graph as iGraph
import plotly.graph_objects as go

app = Flask(__name__)

# Завантаження RDF-файлу та побудова графу
rdf_file_path = "data/knowledge_base.rdf"
rdf_graph = Graph()
rdf_graph.parse(rdf_file_path, format="xml")


# Побудова iGraph
def build_igraph(rdf_graph):
    edges = []
    nodes = set()
    for subj, pred, obj in rdf_graph:
        subj_str = str(subj)
        pred_str = str(pred)
        obj_str = str(obj)
        nodes.update([subj_str, obj_str])
        edges.append((subj_str, obj_str))
    ig = iGraph(directed=True)
    ig.add_vertices(list(nodes))
    ig.add_edges(edges)
    return ig


ig = build_igraph(rdf_graph)


# Оновлення RDF-графу
def update_rdf_graph(rdf_graph, subject, predicate, object_):
    subject_uri = URIRef(f"http://example.com/{subject}")
    predicate_uri = URIRef(f"http://example.com/{predicate}")
    object_value = URIRef(f"http://example.com/{object_}") if object_.startswith("http") else Literal(object_)
    rdf_graph.add((subject_uri, predicate_uri, object_value))
    rdf_graph.serialize(destination=rdf_file_path, format="xml")


# Функція для створення графу з усією онтологією
def visualize_full_graph(ig):
    layout = ig.layout("kk")  # Камада-Кавай для гарної візуалізації
    fig = go.Figure()

    # Додавання вузлів
    x_coords = [layout[v.index][0] for v in ig.vs]
    y_coords = [layout[v.index][1] for v in ig.vs]
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers+text',
        text=ig.vs["name"],
        textposition="top center",
        marker=dict(size=10, color="blue")
    ))

    # Додавання ребер
    for edge in ig.es:
        x0, y0 = layout[edge.source]
        x1, y1 = layout[edge.target]
        fig.add_trace(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=1, color="black")
        ))

    fig.update_layout(showlegend=False)
    return fig.to_html()


@app.route("/")
def index():
    # Візуалізація повного графу
    full_graph_html = visualize_full_graph(ig)
    return render_template("index.html", graph=full_graph_html)


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    if not query:
        return "Помилка, пустий запит", 400

    # Пошук у графі
    results = []
    for subj, pred, obj in rdf_graph:
        if query.lower() in str(subj).lower() or query.lower() in str(obj).lower():
            results.append((str(subj), str(pred), str(obj)))

    if results:
        # Підготовка графу для візуалізації
        ig_subset = iGraph(directed=True)
        nodes = set()
        edges = []

        # Додати всі знайдені вершини та їх зв'язки
        for subj, pred, obj in results:
            nodes.update([subj, obj])
            edges.append((subj, obj))

        # Додати опосередковані зв'язки з оригінального графу
        for subj, obj in ig.get_edgelist():
            subj_name = ig.vs[subj]["name"]
            obj_name = ig.vs[obj]["name"]
            if subj_name in nodes and obj_name in nodes:
                edges.append((subj_name, obj_name))

        # Створити підграф
        ig_subset.add_vertices(list(nodes))
        ig_subset.add_edges(edges)

        # Візуалізація підграфу за допомогою Plotly
        layout = ig_subset.layout("kk")  # Камада-Кавай для гарної візуалізації
        fig = go.Figure()

        # Вузли
        x_coords = [layout[v.index][0] for v in ig_subset.vs]
        y_coords = [layout[v.index][1] for v in ig_subset.vs]
        fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='markers+text',
            text=ig_subset.vs["name"],
            textposition="top center",
            marker=dict(size=10, color="blue")
        ))

        # Ребра
        for edge in ig_subset.es:
            x0, y0 = layout[edge.source]
            x1, y1 = layout[edge.target]
            fig.add_trace(go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=1, color="black")
            ))

        return render_template("index.html", results=results, graph=fig.to_html())

    return render_template("index.html", results=results)



@app.route("/update", methods=["POST"])
def update_ontology():
    subject = request.form.get("subject")
    predicate = request.form.get("predicate")
    object_ = request.form.get("object")
    if not (subject and predicate and object_):
        return "Помилка, відсутні дані", 400
    update_rdf_graph(rdf_graph, subject, predicate, object_)
    return "Онтологія успішно оновлена!", 200


if __name__ == "__main__":
    app.run(debug=True)
