from shapely.geometry import Polygon
import pygame, pytmx


def pytmx_obp_poly_to_shapely_poly_2d(pytmx_obj: pytmx.TiledObject ):
    pts = []
    poly = None
    if hasattr(pytmx_obj, 'points'):
        for point in pytmx_obj.points:
            pt = (point.x, point.y, 0)
            pts.append(pt)

    if len(pts) > 0:
        poly = Polygon(pts)

    return poly


def pygame_rect_to_shapely_poly_2D(rect: pygame.Rect):
    return Polygon([(rect.x, rect.y, 0), (rect.x+rect.width, rect.y, 0),
                    (rect.x+rect.width, rect.y + rect.height, 0), (rect.x, rect.y + rect.height, 0)])


def is_collide_spr_poly(spr: pygame.Rect, p2: Polygon):
    p1 = pygame_rect_to_shapely_poly_2D(spr)
    return p1.intersects(p2)
