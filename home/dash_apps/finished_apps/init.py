from home.dash_apps.finished_apps import container
from home.dash_apps.finished_apps import edit_container
from home.dash_apps.finished_apps import export_container
from home.dash_apps.finished_apps import shared_info


# initial_graphs = []
#top_shows = graphs.Graphs('top5anime', 'Top 5 Anime', 'topanime', 'topanimeslider', True, [Input('topanimeslider', 'value')])
#initial_graphs.append(top_shows)

shared_data = shared_info.Shared_Info()

container_object = container.Container('container', shared_data)
edit_page_container = edit_container.Edit_Container('edit_container', shared_data)
export_page_container = export_container.Export_Container('export_container', shared_data)
