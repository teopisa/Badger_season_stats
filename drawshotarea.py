from matplotlib.patches import Rectangle, Arc
from mplbasketball.utils import transform
import numpy as np


def transform_court_params(court_params, fr="hl", to="vu", origin="center", court_dims=[28.651200000000003, 15.24]):
    """
    Transforms the basketball court parameters based on the desired orientation.
    """
    
    # Transform position-based parameters (distances from edges)
    court_params["hoop_distance_from_edge"] = transform(np.array([court_params["hoop_distance_from_edge"]]), np.array([0]),
                                                         fr=fr, to=to, origin=origin, court_dims=court_dims)[0][0]

    court_params["backboard_distance_from_edge"] = transform(np.array([court_params["backboard_distance_from_edge"]]), np.array([0]),
                                                              fr=fr, to=to, origin=origin, court_dims=court_dims)[0][0]
    
    court_params["inbound_line_distance_from_edge"] = transform(np.array([court_params["inbound_line_distance_from_edge"]]), np.array([0]),
                                                                fr=fr, to=to, origin=origin, court_dims=court_dims)[0][0]
    
    court_params["outbound_line_distance_from_center"] = transform(np.array([court_params["outbound_line_distance_from_center"]]), np.array([0]),
                                                                    fr=fr, to=to, origin=origin, court_dims=court_dims)[0][0]

    # Transform size-based parameters (dimensions, radii, etc.)
    court_params["court_dims"] = transform(np.array([court_params["court_dims"][0]]), np.array([court_params["court_dims"][1]]),
                                            fr=fr, to=to, origin=origin, court_dims=court_dims)
    
    court_params["outer_paint_dims"] = transform(np.array([court_params["outer_paint_dims"][0]]), np.array([court_params["outer_paint_dims"][1]]),
                                                 fr=fr, to=to, origin=origin, court_dims=court_dims)
    
    court_params["inner_paint_dims"] = transform(np.array([court_params["inner_paint_dims"][0]]), np.array([court_params["inner_paint_dims"][1]]),
                                                 fr=fr, to=to, origin=origin, court_dims=court_dims)
    
    # Transform other parameters (radii, diameters, etc.)
    court_params["charge_circle_radius"] = transform(np.array([court_params["charge_circle_radius"]]), np.array([0]), 
                                                      fr=fr, to=to, origin=origin, court_dims=court_dims)[0][0]

    court_params["three_point_arc_diameter"] = transform(np.array([court_params["three_point_arc_diameter"]]), np.array([0]),
                                                         fr=fr, to=to, origin=origin, court_dims=court_dims)[0][0]

    court_params["three_point_line_length"] = transform(np.array([court_params["three_point_line_length"]]), np.array([0]),
                                                        fr=fr, to=to, origin=origin, court_dims=court_dims)[0][0]
    
    court_params["three_point_side_width"] = transform(np.array([court_params["three_point_side_width"]]), np.array([0]),
                                                       fr=fr, to=to, origin=origin, court_dims=court_dims)[0][0]

    # If there are additional position-based parameters like hoop height, etc., transform them similarly
    court_params["hoop_height"] = transform(np.array([court_params["hoop_height"]]), np.array([0]),
                                            fr=fr, to=to, origin=origin, court_dims=court_dims)[0][0]
    
    return court_params

def draw_shot_zones(ax, court_params):
    """
    Draws shot zones on a basketball court based on specific court dimensions.
    
    Parameters:
    - ax: The matplotlib Axes object on which to draw.
    - court_params: Dictionary of court dimensions.
    """
    
    # Extract court parameters for easy access
    court_width, court_height = court_params["court_dims"]
    hoop_distance = court_params["hoop_distance_from_edge"]
    hoop_radius = court_params["hoop_diameter"] / 2
    backboard_distance = court_params["backboard_distance_from_edge"]
    backboard_width = court_params["backboard_width"]
    charge_circle_radius = court_params["charge_circle_radius"]
    paint_width, paint_height = court_params["outer_paint_dims"]
    inner_paint_width, inner_paint_height = court_params["inner_paint_dims"]
    free_throw_circle_radius = court_params["outer_circle_diameter"] / 2
    three_point_diameter = court_params["three_point_arc_diameter"]
    three_point_line_length = court_params["three_point_line_length"]
    three_point_side_width = court_params["three_point_side_width"]

    # 1. Paint area (outer rectangle)
    ax.add_patch(Rectangle((-paint_width / 2, -court_height / 2 + hoop_distance),
                           paint_width, paint_height,
                           color="orange", alpha=0.3, zorder=1))
    
    # 2. Inner paint area
    ax.add_patch(Rectangle((-inner_paint_width / 2, -court_height / 2 + hoop_distance),
                           inner_paint_width, inner_paint_height,
                           color="orange", alpha=0.3, zorder=1))

    # 3. Free-throw circle
    ax.add_patch(Arc((0, -court_height / 2 + hoop_distance + paint_height),
                     free_throw_circle_radius * 4, free_throw_circle_radius * 4,
                     theta1=0, theta2=180, color="blue", linewidth=2, zorder=2))

    # 4. Three-point arc
    ax.add_patch(Arc((0, -court_height / 2 + hoop_distance),
                     three_point_diameter, three_point_diameter,
                     theta1=-court_params["three_point_arc_angle"],
                     theta2=180 + court_params["three_point_arc_angle"],
                     color="green", linewidth=2, zorder=3))

    # 5. Three-point side lines (left and right)
    ax.add_patch(Rectangle((paint_width + three_point_side_width, 
                            court_height + hoop_distance),
                           three_point_side_width, three_point_line_length,
                           color="green", alpha=0.3, zorder=1))
    
    ax.add_patch(Rectangle((paint_width / 2, -court_height / 2 + hoop_distance),
                           three_point_side_width, three_point_line_length,
                           color="green", alpha=0.3, zorder=1))
    
    # 6. Charge circle
    ax.add_patch(Arc((0, -court_height / 2 + hoop_distance),
                     charge_circle_radius * 2, charge_circle_radius * 2,
                     theta1=0, theta2=180, color="blue", linewidth=2, zorder=2))

    # Additional areas like mid-range zones can be added similarly using the parameters
    # For example, adding side rectangles for mid-range zones.
    # Left side
    ax.add_patch(Rectangle((-paint_width - 1, -court_height / 2 + hoop_distance + paint_height),
                           2, paint_height, color="yellow", alpha=0.3, zorder=1))
    # Right side
    ax.add_patch(Rectangle((paint_width -2.2, -court_height / 1.43 + hoop_distance + paint_height),
                           4, paint_height, color="yellow", alpha=0.3, zorder=1))
    
    # Mark the hoop location
    ax.plot(0, -court_height / 2 + hoop_distance, 'o', color='blue', markersize=hoop_radius * 50)