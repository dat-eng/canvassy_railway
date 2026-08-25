from streamlit_js_eval import streamlit_js_eval


# --------------------------------------------------
# Get GPS Location
# --------------------------------------------------

def get_gps_location(enabled):

    if not enabled:
        return None

    return streamlit_js_eval(
        js_expressions="""
            new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(
                    (pos) => resolve({
                        latitude: pos.coords.latitude,
                        longitude: pos.coords.longitude
                    }),
                    () => resolve(null)
                );
            })
        """,
        key="gps_location",
    )