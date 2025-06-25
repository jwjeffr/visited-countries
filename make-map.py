import folium
import geopandas as gpd


def main():

    # List of countries you've visited (can also use ISO codes)
    visited_countries = {'US', 'MX', 'ES', 'CA', 'KY', 'BZ', 'GT', 'QA', 'VN', 'JP'}
    about_to_visit = {'JM'}

    # Load world geometries
    world = gpd.read_file("ne_10m_admin_0_map_subunits.zip")

    # Create a column to indicate visited status
    world['have visited'] = world["ISO_A2_EH"].apply(lambda x: x in visited_countries)
    world['about to visit'] = world["ISO_A2_EH"].apply(lambda x: x in about_to_visit)

    # Create the folium map
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Define colors
    def style_function(feature):
        if feature['properties']['have visited']:
            color = '#2ecc71'
        elif feature['properties']['about to visit']:
            color = '#ffbf00'
        else:
            color = '#bdc3c7'
        return {
            'fillColor': color,
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7,
        }

    # Add the GeoJSON layer
    folium.GeoJson(
        world,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=("NAME", "have visited", "about to visit"))
    ).add_to(m)

    # Save the map
    m.save("map/index.html")


if __name__ == "__main__":

    main()
