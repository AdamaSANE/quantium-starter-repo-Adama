import app


def test_header_present(dash_duo):
    dash_duo.start_server(app.app)
    header = dash_duo.wait_for_element("h1")
    assert header.is_displayed()
    assert header.text == "Pink Morsel sales by region"


def test_visualisation_present(dash_duo):
    dash_duo.start_server(app.app)
    graph = dash_duo.wait_for_element("#sales-chart")
    assert graph.is_displayed()


def test_region_picker_present(dash_duo):
    dash_duo.start_server(app.app)
    region_picker = dash_duo.wait_for_element("#region-filter")
    assert region_picker.is_displayed()